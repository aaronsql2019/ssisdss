from dss.models import Base

class BaseCohort(Base):
    """
    """
    def __str__(self):
        """
        Kind: 'Name' (idnumber)
        """
        ret = ["<Total of {number} members for cohort {idnumber}:".format(idnumber=self.idnumber, number=len(self.members))]
        ret.append('\t' + ", ".join(self.members))
        return "\n".join(ret)

    def __repr__(self):
        return "<{}.{}.get('{}')>".format(self._origtreename, self._branchname, self.idnumber)

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

