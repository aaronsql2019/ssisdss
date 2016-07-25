from dss.datastore.branch import DataStoreBranches

class AbstractBranch(DataStoreBranches):
	pass
	
class AutosendBranches(AbstractBranch):
	""" pickup """
	pass

class MoodleBranches(AbstractBranch):
	""" pickup """
	pass

class StudentBranch:
	_branchname = 'students'

class TeacherBranch:
	_branchname = 'teachers'

class AutosendStudents(AutosendBranches, StudentBranch):
	_klass = 'ssis_dss.model.test_model.AutosendStudent'
	_importer = 'ssis_dss.importers.test_importers.AutosendStudentsImporter'

	@classmethod
	def ex(cls):
		return cls.get('67890')

class AutosendTeachers(AutosendBranches, TeacherBranch):
	_klass = 'ssis_dss.model.test_model.AutosendTeacher'
	_importer = 'ssis_dss.importers.test_importers.AutosendTeachersImporter'

class MoodleStudents(MoodleBranches, StudentBranch):
	_klass = 'ssis_dss.model.test_model.MoodleStudent'
	_importer = 'ssis_dss.importers.test_importers.MoodleStudentsImporter'

class MoodleTeachers(MoodleBranches, TeacherBranch):
	_klass = 'ssis_dss.model.test_model.MoodleTeacher'
	_importer = 'ssis_dss.importers.test_importers.MoodleTeachersImporter'