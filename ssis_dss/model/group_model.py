from dss.models import Base

class BaseGroup(Base):
    """
    """
    def __repr__(self):
        """
        Kind: 'Name' (idnumber)
        """
        return "<{}: ({})>".format('Group', self.idnumber)

    def _jsonencoder(self, obj):
        """
        We use sets (so useful, maybe make this a default?)
        """
        if isinstance(obj, set):
            return list(obj)


class BaseAutosend:
    """
    """
    pass

class BaseMoodle:
    pass

class AutosendGroup(BaseAutosend, BaseGroup):
    """
    """
    pass

class MoodleGroup(BaseMoodle, BaseGroup):
    pass

