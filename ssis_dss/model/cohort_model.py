from dss.models import Base

class BaseCohort(Base):
    """
    """
    def __repr__(self):
        """
        Kind: 'Name' (idnumber)
        """
        ret = ["<Total of {number} members for cohort {idnumber}:".format(idnumber=self.idnumber, number=len(self.members))]
        ret.append('\t' + ", ".join(self.members))
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

