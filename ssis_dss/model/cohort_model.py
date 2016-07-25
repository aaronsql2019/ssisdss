from dss.models import Base

class BaseCohort(Base):
    """
    """
    def __repr__(self):
        """
        Kind: 'Name' (idnumber)
        """
        ret = ["<Total of {length} cohorts for user {user_idnumber}:".format(user_idnumber=self.idnumber, length=len(self.cohorts))]
        ret.append('\t' + ", ".join(self.cohorts))
        return "\n".join(ret)

class BaseAutosend:
    """
    """
    pass

class BaseMoodle:
    pass

class AutosendCohort(BaseAutosend, BaseCohort):
    """
    """
    pass
    
class MoodleCohort(BaseMoodle, BaseCohort):
    pass

