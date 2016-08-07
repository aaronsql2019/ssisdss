from dss.models import Base
import re

from ssis_dss.utils import Kind
from enum import Enum

class BaseUser(Base):
    """
    All the tracked properties should not have an underscore
    For instance properties could be a @property (can also define class properties)
    and it is up to the programmer to ensure that they are all used by the importer!
    Can define derived properties, such as this:

    user = BaseUser(firstname='Adam', lastname="Apple")
    user.name  # "Adam Apple"

    No __init__ method needed, as this is taken care of in Base
    """

    kind = Kind.undefined

    @property
    def name(self):
        return self.firstname + ' ' + self.lastname

    def _jsonencoder(self, obj):
        """
        The value for the "kind" (or any enum found in a branch)
        becomes {"kind": value}
        """
        if isinstance(obj, Enum):
            return obj.name
        elif isinstance(obj, set):
            return sorted(list(obj))

    def __repr__(self):
        """
        Kind: 'Name' (idnumber)
        """
        l = len('kind.')  # 5
        kind = str(self.kind).title()[l:]
        return "<{}: ({})>".format(kind, self.idnumber)

# Now define properties of students and teachers that apply to them all
class BaseAutosend:
    """
    """

    @property
    def lastname(self):
        return (self.lastfirst.split(',')[0]).strip(' ')

    @property
    def firstname(self):
        return (self.lastfirst.split(',')[1]).strip(' ')

class BaseMoodle:
    @property
    def lastfirst(self):
        return "{}, {}".format(self.lastname, self.firstname)

class BaseStudent(BaseUser):
    @property
    def _family_id(self):
        return self.idnumber[:4]

    @property
    def email(self):
        return '{}@{}'.format(self.username, 'student.ssis-suzhou.net')   # todo make this a setting instead

    kind = Kind.student

class BaseParent(BaseUser):
    kind = Kind.parent

    @property
    def _family_id(self):
        return self.idnumber[:4]

    def __repr__(self):
        return "<{} '{}'>".format(self.__class__.__name__, self.name)

class BaseTeacher(BaseUser):
    kind = Kind.teacher

class BaseParentChildLink(Base):
    def _jsonencoder(self, obj):
        """
        The value for the "kind" (or any enum found in a branch)
        becomes {"kind": value}
        """
        if isinstance(obj, set):
            # Sets have to be sorted lists, in order to ensure the character sequence is correct
            return sorted(list(obj))

class AutosendStudent(BaseAutosend, BaseStudent):
    """
    Students in our information system don't have a username yet, so we derive it ourselves
    And, for us, usernames are defined as:
    firstname + lastname + year of graduation
    Which is a calculation
    """
    @property
    def auth(self):
        return 'manual' if int(self._grade) >= 4 else 'nologin'

    @property
    def _cohorts(self):
        ret = {'studentsALL', 'students{}'.format(self._grade), 'students{}'.format(self.homeroom)}
        ret.add( 'students{}'.format('SEC' if int(self._grade) >=6 else 'ELEM' ) )
        if int(self._grade) in range(6,11):
            ret.add('studentsMS')
        elif int(self._grade) in range(10,13):
            ret.add('studentsHS')
        return ret

    @property
    def username(self):
        return self.idnumber
        #return (self.name + self._year_of_graduation()).lower().replace(' ', '')

    @property
    def _parents(self):
        return [self._family_id + 'P', self._family_id + 'PP']

    @property
    def _guardian_email_list(self):
        return self._guardianemails.split(',')

    @property
    def _parent1_email(self):
        l = self._guardian_email_list
        return l[0]

    @property
    def _parent2_email(self):
        l = self._guardian_email_list
        return l[1] if len(l) > 1 else l[0]

    # The following methods are not tracked:
    def _year_of_graduation(self):
        """
        Do the math, and then remove the '20' from the year
        Underscore, because this is not information we are tracking
        """
        return str((12 - int(self._grade)) + self._this_year())[:2]

    def _this_year(self):
        # Very rudimentary, better to use calendar to check the current year
        # But reminds us that an underscore is needed here because this isn't information we are tracking
        return 2016

class MoodleStudent(BaseMoodle, BaseStudent):
    # I don't think I need to declare these specifically, because they are untracked
    _passport = ''
    _dob = ''
    _department = ''
    _guardianemails = ''
    _districtentrydate = ''

    @property
    def _grade(self):
        return re.sub('[^0-9]+$', '', self.homeroom)

class AutosendParent(BaseAutosend, BaseParent):
    """
    """

    @property
    def auth(self):
        return 'manual'

class MoodleParent(BaseMoodle, BaseParent):
    """
    """
    pass

class AutosendTeacher(BaseAutosend, BaseTeacher):
    # For those that might have children associated to their teacher account
    #children = []

    @property
    def username(self):
        return self.idnumber

    @property
    def _cohorts(self):
        if self._status == '0':
            return ['supportstaffALL']
        else:
            if self._status == '111':
                return ['teachersALL', 'teachersELEM']
            elif self._status == '112':
                return ['teachersALL', 'teachersSEC']
            else:
                return ['teachersALL']

class MoodleTeacher(BaseMoodle, BaseTeacher):
    _title = ''
    _status = 0
    _active = 0
    _dunno = ''

class AutosendParentChildLink(BaseParentChildLink):
    pass

class MoodleParentChildLink(BaseParentChildLink):
    pass
