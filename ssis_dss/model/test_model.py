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
    kind = Kind.student

class BaseTeacher(BaseUser):
    kind = Kind.teacher

class AutosendStudent(BaseAutosend, BaseStudent):
    """
    Students in our information system don't have a username yet, so we derive it ourselves
    And, for us, usernames are defined as:
    firstname + lastname + year of graduation
    Which is a calculation
    """

    @property
    def username(self):
        return (self.name + self._year_of_graduation()).lower().replace(' ', '')

    @property
    def grade(self):
        return int(re.sub('[^0-9]$', '', self.homeroom))

    # The following methods are not tracked:
    def _year_of_graduation(self):
        """
        Do the math, and then remove the '20' from the year
        Underscore, because this is not information we are tracking
        """
        return str((12 - int(self.grade)) + self._this_year())[:2]

    def _this_year(self):
        # Very rudimentary, better to use calendar to check the current year
        # But reminds us that an underscore is needed here because this isn't information we are tracking
        return 2016


class MoodleStudent(BaseMoodle, BaseStudent):
    pass

class AutosendTeacher(BaseAutosend, BaseTeacher):
    pass

class MoodleTeacher(BaseMoodle, BaseTeacher):
    pass