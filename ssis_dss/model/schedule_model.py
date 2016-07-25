from dss.models import Base

class BaseSchedule(Base):
    """
    """
    def __repr__(self):
        """
        Kind: 'Name' (idnumber)
        """
        return "<{}: ({})>".format('Schedule', self.idnumber)

class BaseAutosend:
    """
    """
    pass

class BaseMoodle:
    pass

class AutosendSchedule(BaseAutosend, BaseSchedule):
    """
    Not synced over, as moodle doesn't need or have a schedule
    """
    pass
    # @property
    # def group(self):
    #     staff = self._get_from_branch_attr('staff/staff_idnumber')
    #     if not staff:
    #         return "unknown"
    #     g = "{}-{}-{}".format(staff.lastname.lower(), self.course.lower(), self.section.lower())
    #     return g

class MoodleSchedule(BaseMoodle, BaseSchedule):
    """
    """
    pass