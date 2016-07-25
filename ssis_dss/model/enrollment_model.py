from dss.models import Base

class BaseEnrollment(Base):
    """
    """
    def __repr__(self):
        """
        Kind: 'Name' (idnumber)
        """
        return "<{}: ({})>".format('Enrollment', self.idnumber)

    @property
    def enrollments(self):
        ret = []
        assert len(self.courses) == len(self.groups)
        for i in range(len(self.courses)):
            ret.append( (self.courses[i], self.groups[i], self.roles[i]) )
        ret = list(set(ret))
        ret.sort(key=lambda x: x[0])
        return ret

    def __repr__(self):
        ret = []
        ret.append("<Total of {length} enrollments for user {user_idnumber}: ".format(user_idnumber=self.idnumber, length=len(self.enrollments)))
        for enrollment in self.enrollments:
            course, group, role = enrollment
            ret.append("\t({} {} {})".format(course, group, role))
        ret[-1] += ">"
        return "\n".join(ret)

class BaseAutosend:
    """
    """
    pass

class BaseMoodle:
    pass

class AutosendEnrollment(BaseAutosend, BaseEnrollment):
    """
    """
    pass
    # def __repr__(self):
    #     user = self._get_branch_from_attr('users/idnumber')
    #     return "<Enrollments for {kind} user {name}".format(user)

class MoodleEnrollment(BaseMoodle, BaseEnrollment):
    pass