from dss.datastore.branch import DataStoreBranches

class AbstractBranch(DataStoreBranches):
	pass

# =====	
class AutosendBranches(AbstractBranch):
	pass

class AutosendFirstrunBranches(AbstractBranch):
	pass

class MoodleBranches(AbstractBranch):
	pass

class MoodleFirstrunBranches(AbstractBranch):
	pass
# +=====


class StudentBranch:
	_branchname = 'students'

class ParentBranch:
	_branchname = 'parents'

class TeacherBranch:
	_branchname = 'staff'

class UsersBranch:
	_branchname = 'users'

class StrandedUsersTable:
	_branchname = 'strandedusers'

class CohortsBranch:
	_branchname = 'cohorts'

class CourseBranch:
	_branchname = 'courses'

class ScheduleBranch:
	_sub = False
	_branchname = 'schedule'

class GroupBranch:
	_branchname = 'groups'

class EnrollmentBranch:
	_branchname = 'enrollments'

class Incremental:
	def __init__(self):
		self.reset()
	def reset(self):
		self.o = 0
	def __call__(self):
		self.o += 1
		return self.o

inc = Incremental()
# AUTOSEND:
class AutosendStudents(AutosendBranches, StudentBranch):
	order = inc()
	_klass = 'ssis_dss.model.AutosendStudent'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendStudentsImporter'

class AutosendTeachers(AutosendBranches, TeacherBranch):
	order = inc()
	_klass = 'ssis_dss.model.AutosendTeacher'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendTeachersImporter'

class AutosendParents(AutosendBranches, ParentBranch):
	order = inc()
	_klass = 'ssis_dss.model.user_model.AutosendParent'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendParentsImporter'

class AutosendUsers(AutosendBranches, UsersBranch):
	order = inc()
	_klass = None
	_importer = 'ssis_dss.importers.hybrid_importers.UsersImporter'

class AutosendCohorts(AutosendBranches, CohortsBranch):
	order = inc()
	_klass = 'ssis_dss.model.cohort_model.AutosendCohort'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendCohortsImporter'

class AutosendCourses(AutosendBranches, CourseBranch):
	order = inc()
	_klass = 'ssis_dss.model.course_model.AutosendCourse'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendCourseImporter'

class AutosendSchedule(AutosendBranches, ScheduleBranch):
	order = inc()
	_klass = 'ssis_dss.model.schedule_model.AutosendSchedule'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendScheduleImporter'

class AutosendGroups(AutosendBranches, GroupBranch):
	order = inc()
	_klass = 'ssis_dss.model.group_model.AutosendGroup'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendGroupImporter'

class AutosendEnrollments(AutosendBranches, EnrollmentBranch):
	order = inc()
	_klass = 'ssis_dss.model.enrollment_model.AutosendEnrollment'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendEnrollmentsImporter'


# MOODLE:
inc.reset()
class MoodleStudents(MoodleBranches, StudentBranch):
	order = inc()
	_klass = 'ssis_dss.model.MoodleStudent'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleStudentsImporter'

class MoodleTeachers(MoodleBranches, TeacherBranch):
	order = inc()
	_klass = 'ssis_dss.model.MoodleTeacher'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleTeachersImporter'

class MoodleParents(MoodleBranches, ParentBranch):
	order = inc()
	_klass = 'ssis_dss.model.user_model.MoodleParent'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleParentsImporter'

class MoodleUsers(MoodleBranches, UsersBranch):
	order = inc()
	_klass = None
	_importer = 'ssis_dss.importers.hybrid_importers.UsersImporter'

class MoodleStrandedUsers(MoodleBranches, StrandedUsersTable):
	order = inc()
	_klass = None
	_importer = 'ssis_dss.importers.moodle_importers.StrandedUsersTable'

class MoodleCohorts(MoodleBranches, CohortsBranch):
	order = inc()
	_klass = 'ssis_dss.model.cohort_model.MoodleCohort'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleCohortsImporter'

class MoodleCourses(MoodleBranches, CourseBranch):
	order = inc()
	_klass = 'ssis_dss.model.course_model.MoodleCourse'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleCourseImporter'

class MoodleSchedule(MoodleBranches, ScheduleBranch):
	order = inc()
	_klass = 'ssis_dss.model.schedule_model.MoodleSchedule'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleScheduleImporter'

class MoodleGroups(MoodleBranches, GroupBranch):
	order = inc()
	_klass = 'ssis_dss.model.group_model.MoodleGroup'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleGroupImporter'

class MoodleEnrollments(MoodleBranches, EnrollmentBranch):
	order = inc()
	_klass = 'ssis_dss.model.enrollment_model.MoodleEnrollment'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleEnrollmentsImporter'

# FIRST-RUNS
inc.reset()
class AutosendFirstrunStudents(AutosendFirstrunBranches, StudentBranch):
	order = inc()
	_klass = 'ssis_dss.model.AutosendStudent'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendStudentsImporter'

class AutosendFirstrunTeachers(AutosendFirstrunBranches, TeacherBranch):
	order = inc()
	_klass = 'ssis_dss.model.AutosendTeacher'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendTeachersImporter'

class AutosendFirstrunParents(AutosendFirstrunBranches, ParentBranch):
	order = inc()
	_klass = 'ssis_dss.model.user_model.AutosendParent'
	_importer = 'ssis_dss.importers.autosend_importers.AutosendParentsImporter'

class AutosendFirstrunUsers(AutosendFirstrunBranches, UsersBranch):
	order = inc()
	_klass = None
	_importer = 'ssis_dss.importers.hybrid_importers.UsersImporter'

inc.reset()
class MoodleFirstrunStudents(MoodleFirstrunBranches, StudentBranch):
	order = inc()
	_klass = 'ssis_dss.model.MoodleStudent'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleStudentsImporter'

class MoodleFirstrunTeachers(MoodleFirstrunBranches, TeacherBranch):
	order = inc()
	_klass = 'ssis_dss.model.MoodleTeacher'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleTeachersImporter'

class MoodleFirstrunParents(MoodleFirstrunBranches, ParentBranch):
	order = inc()
	_klass = 'ssis_dss.model.user_model.MoodleParent'
	_importer = 'ssis_dss.importers.moodle_importers.MoodleParentsImporter'

class MoodleFirstrunUsers(MoodleFirstrunBranches, UsersBranch):
	order = inc()
	_klass = None
	_importer = 'ssis_dss.importers.hybrid_importers.UsersImporter'
