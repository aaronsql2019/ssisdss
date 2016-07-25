from dss.models import Base

class BaseCourse(Base):
    """
    """
    def __repr__(self):
        """
        Kind: 'Name' (idnumber)
        """
        return "<{}: ({})>".format('Course', self.idnumber)

class BaseAutosend:
    """
    """
    _db_id = 0

class BaseMoodle:
    pass

class AutosendCourse(BaseAutosend, BaseCourse):
    """
    """
    pass
    
class MoodleCourse(BaseMoodle, BaseCourse):
    _shortcode = ""

