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
                    # from IPython import embed;embed();exit()
                    for c in parentlink.links:
                        child = self._tree.students.get(c)
                        cohorts.update({c.replace('students', 'parents') for c in child._cohorts})
                elif user.kind == Kind.teacher:
                    cohort = user._cohorts
                elif user.kind == Kind.administrator:
                    pass

                for cohort in cohorts:
                    yield {
                        'idnumber': user_id,
                        'cohorts': [cohort]
                    }

class ShortcodeFilterOuter(AutosendImporter):
    def kwargs_preprocessor(self, kwargs):
        """
        Translate the course shortcode
        """
        short, _ = convert_short_long(kwargs['course'], "")
        kwargs['course'] = short
        # No need to lookup the course...
        #course = self._tree.courses.get(short)
        staff = self._tree.staff.get(kwargs['staff_idnumber'])
        if not staff:
            print("Staff member {} in schedule but not in staff info?".format(kwargs['staff_idnumber']))
            staff = type('Staff', (), {'lastname':'unknownstaff'})
        kwargs['group'] = "{}-{}-{}".format(staff.lastname.lower(), short.lower(), kwargs['section'].lower())
        return kwargs

    def filter_out(self, **kwargs):
        return kwargs['course'].startswith('X')

class IdnumberFilterOuter(AutosendImporter):
    def kwargs_preprocessor(self, kwargs):
        """
        Translate the course shortcode
        """
        short, long_ = convert_short_long(kwargs['idnumber'], kwargs['name'])
        kwargs['_shortcode'] = kwargs['idnumber']
        kwargs['moodle_shortcode'] = short
        kwargs['name'] = long_
        kwargs['idnumber'] = short
        return kwargs

    def filter_out(self, **kwargs):
        return kwargs['idnumber'].startswith('X')

class AutosendCourseImporter(TranslatedCSVImporter):
    klass = IdnumberFilterOuter
    translate = {'ssis_dist': ['ssis_elem', 'ssis_sec']}

class AutosendScheduleImporter(TranslatedCSVImporter):
    klass = ShortcodeFilterOuter
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
            group = item.group
            section = item.section

            sobj = self._tree.students.get(student)

            yield {
                'idnumber': group,
                'course': course,
                'section': section,
                'students': set([student]),
                'teachers': set([teacher]),
                'parents': self._tree.parentchildlink.get(student).links
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

            for parent in self._tree.parentchildlink.get(student).links:
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

