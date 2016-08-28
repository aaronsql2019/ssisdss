import os

from dss.importers.default_importer import DefaultImporter
from dss.importers.csv_importer import CSVImporter, TranslatedCSVImporter
from dss.importers.db_importer import PostgresDBImporter
from dss.importers.default_importer import DefaultImporter
from contextlib import contextmanager

from ssis_dss.converter import convert_short_long
from ssis_dss.utils import Kind

import ssis_dss_settings

verbose = False

class AutosendImporter(CSVImporter):
    """
    Don't read in the username
    """
    _settings = ssis_dss_settings['SSIS_AUTOSEND']

    def get_path(self):
        """
        Add version capabilities
        """
        path = self.get_setting('path')
        parent_dir, file_name = os.path.split(path)
        if hasattr(self, 'file_hook'):
            file_name = self.file_hook(file_name)
        starting_name = file_name.format(branch_name=self._branch.name)
        files = []
        for file_ in os.listdir(parent_dir):
            if file_.startswith(starting_name):
                version = float(file_[len(starting_name):])
                obj = {'file_':file_, 'version':version}
                files.append(obj)
        files.sort(key=lambda o: o['version'])
        if len(files) == 0:
            print("No candidates found for {}".format(starting_name))
            exit()
        winner = files[-1]
        verbose and print("-> Using {}".format(winner))
        return os.path.join(parent_dir, winner['file_'])

class AutosendStudentsImporter(AutosendImporter):
    pass

class AutosendTeachersImporter(AutosendImporter):
    def filter_out(self, **kwargs):
        return kwargs['_active'] != '1' or kwargs['email'] == "" or not kwargs['idnumber'].isdigit()

class AutosendParentsImporter(DefaultImporter):
    """
    Just go through the students branch and derive the parents as necessary
    """

    def readin(self):
        branch = self._tree.students
        for student in branch.get_objects():
            parent1 = student._family_id + 'P'
            parent1_email = student._parent1_email
            parent2 = student._family_id + 'PP'
            parent2_email = student._parent2_email
            yield {
                'idnumber': parent1,
                'email': parent1_email,
                'lastfirst': parent1_email + ', Parent',
                'username': parent1,
            }
            yield {
                'idnumber': parent2,
                'email': parent2_email,
                'username': parent2,
                'lastfirst': parent2_email + ', Parent',
            }

class AutosendParentChildLinkImporter(DefaultImporter):
    def readin(self):
        branch = self._tree.students
        for student in branch.get_objects():
            for parent in student._parents:
                yield {
                    'idnumber': student.idnumber,
                    'links': set([parent])
                }
                yield {
                    'idnumber': parent,
                    'links': set([student.idnumber])
                }

class AutosendCohortsImporter(DefaultImporter):
    def readin(self):
        for b in ['students', 'parents', 'staff']:
            branch = getattr(self._tree, b)
            for user_id in branch.keys():
                user = branch.get(user_id)
                if user.kind == Kind.student:
                    cohorts = user._cohorts
                elif user.kind == Kind.parent:
                    cohorts = set()
                    parent = self._tree.parents.get(user.idnumber)
                    parentlink = self._tree.parentchildlink.get(parent.idnumber)
                    for c in parentlink.links:
                        child = self._tree.students.get(c)
                        cohorts.update({c.replace('students', 'parents') for c in child._cohorts})
                elif user.kind == Kind.teacher:
                    cohort = user._cohorts
                elif user.kind == Kind.administrator:
                    pass

                for cohort in cohorts:
                    yield {
                        'idnumber': cohort,
                        'members': [user_id]
                    }

class ScheduleImporter(AutosendImporter):
    def kwargs_preprocessor(self, kwargs):
        """
        Translate the course shortcode
        """
        short, _ = convert_short_long(kwargs['course'], "")
        kwargs['course'] = short

        staff = self._tree.staff.get(kwargs['staff_idnumber'])
        student = self._tree.students.get(kwargs['student_idnumber'])
        if not staff or not student:
            return None
        grade = student._grade
        kwargs['grade'] = grade
        kwargs['_old_group'] = "{}-{}-{}".format(staff.lastname.lower(), short.lower(), kwargs['section'].lower())
        kwargs['group'] = "{}-{}-{}-{}".format(staff.lastname.lower(), short.lower(), grade, kwargs['section'].lower())
        return kwargs

    def filter_out(self, **kwargs):
        student = self._tree.students.get(kwargs['student_idnumber'])
        staff = self._tree.staff.get(kwargs['staff_idnumber'])
        return student is None or kwargs['course'].startswith('X')

class CourseImporter(AutosendImporter):
    def kwargs_preprocessor(self, kwargs):
        """
        Translate the course shortcode
        """
        shortcode = kwargs['idnumber']
        short, long_ = convert_short_long(shortcode, kwargs['name'])
        kwargs['_shortcode'] = shortcode
        kwargs['moodle_shortcode'] = short
        kwargs['name'] = long_
        kwargs['idnumber'] = short
        return kwargs

    def filter_out(self, **kwargs):
        return kwargs['idnumber'].startswith('X')

class AutosendCourseImporter(TranslatedCSVImporter):
    klass = CourseImporter
    translate = {'ssis_dist': ['ssis_elem', 'ssis_sec']}

class AutosendScheduleImporter(TranslatedCSVImporter):
    klass = ScheduleImporter
    translate = {'ssis_dist': ['ssis_elem', 'ssis_sec']}

class AutosendGroupImporter(DefaultImporter):
    def readin(self):
        branch = self._tree.schedule
        for key in branch.keys():
            item = branch.get(key)
            id_ = item.idnumber
            student = item.student_idnumber
            teacher = item.staff_idnumber
            course = item.course
            _old_group = item._old_group
            group = item.group
            grade = item.grade
            section = item.section

            sobj = self._tree.students.get(student)
            if not sobj:
                # TODO: raiseerror instead?
                # This can happen when student is in the schedule but not in info
                continue
            members = [student, teacher]
            members.extend(sobj._parents)

            yield {
                'idnumber': group,
                '_old_group': _old_group,
                'course': course,
                'grade': grade,
                'section': section,
                'members': set(members),
            }

class AutosendEnrollmentsImporter(DefaultImporter):

    def readin(self):
        branch = self._tree.schedule
        for key in branch.keys():
            item = branch.get(key)
            id_ = item.idnumber
            student = item.student_idnumber
            teacher = item.staff_idnumber
            course = item.course
            group = item.group

            yield {
                'idnumber': student,
                'courses': [course],
                'groups': [group],
                'roles': ['student']
            }

            sobj = self._tree.students.get(student)
            if not sobj:
                print('Student in schedule but not in district info: {}'.format(student))
                continue

            for parent in sobj._parents:
                yield {
                    'idnumber': parent,
                    'courses': [course],
                    'groups': [group],
                    'roles': ['parent']
                }

            yield {
                'idnumber': teacher,
                'courses': [course],
                'groups': [group],
                'roles': ['editingteacher']
            }

