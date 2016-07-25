from dss.importers.db_importer import PostgresDBImporter
from ssis_dss.moodle.MoodleInterface import MoodleInterface

from dss.templates.default_template import DefaultTemplate

from ssis_dss.utils import Kind
from ssis_dss.moodle.php import PHP

import ssis_dss_settings

class MoodleDB(PostgresDBImporter, MoodleInterface):
	_settings = ssis_dss_settings['SSIS_DB']

	def __init__(self):
		"""
		We don't need branch and/or tree, so override this to compensate.
		(Also doesn't do check for cohorts)
		FIXME: Refactor to make more sense!
		"""
		self.init()

class MoodleTemplates(DefaultTemplate):
	def __init__(self):
		self.moodledb = MoodleDB()
		self.php = PHP()

class MoodleFirstRunTemplate(MoodleTemplates):
	"""
	Implements initial account creations and creates groups as needed
	Seperated out this way so that in the consecutive run we can ensure that we everything is already set up properly for enrollments
	"""
	def new_users(self, action):
		if not action.idnumber.strip():
			return {'result': False, 'message': 'No idnumber?'}
		else:
			user = action.source
			result = self.php.create_account(user.username, user.email, user.firstname, user.lastname, user.idnumber)
			if not result['result'] is not True:
				return result
			else:
				# FIXME: Theses results are lost! Use handle into template ...
				for cohort_idnumber in user.cohorts:
					self.php.add_user_to_cohort(user.idnumber, cohort_idnumber)
			return result
	def new_parents(self, action):
		return self.new_users(action)
	def new_staff(self, action):
		return self.new_users(action)
	def new_students(self, action):
		return self.new_users(action)

	def new_courses(self, action):
		course = action.source
		return self.php.create_new_course(course.idnumber, course.name)

	def new_groups(self, action):
		group = action.source
		course = action.source._tree.courses.get(group.course)
		if course is None:
			return {'result': False, 'message': "Not adding group {0.idnumber} because no corresponding course {0.course} in moodle".format(group)}

	def new_cohorts(self, action):
		cohort = action.source
		return self.php.new_cohort(cohort.idnumber, cohort.idnumber)

	def add_parents_to_students(self, action):
		parent = action.source._tree.parents.get(action.attribute)
		child = action.dest
		return self.php.associate_child_to_parent(parent.idnumber, child.idnumber)

class MoodleSecondRunTemplate(MoodleTemplates):

	def add_enrollments_to_students(self, action):
		user = action.dest.idnumber
		course = action.attribute
		return self.php_command('enrol_student_into_course', user, course, group) # just pass the whole schedule object itself

	def update_user_profile(self, action, column):
		who = action.dest
		to_ = getattr(action.source, column)
		kwargs = {}
		kwargs[column] = to_
		return self.moodledb.update_table('users', where={'idnumber':who.idnumber}, **kwargs)
	def update_auth(self, action):
		return self.update_user_profile(action, 'auth')
	def update_username(self, action):
		# First check to see to ensure that there is no one else with that username
		user = self.moodledb.get_user_from_username(action.source.username)
		if user:
			return {'result': False, 'message': 'There is already a user with the username of {}'.format(action.source.username)}
		return self.update_user_profile(action, 'username')
	def update_firstname(self, action):
		return self.update_user_profile(action, 'firstname')
	def update_lastname(self, action):
		return self.update_user_profile(action, 'lastname')
