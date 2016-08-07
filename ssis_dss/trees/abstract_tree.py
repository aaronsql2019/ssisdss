from dss.datastore.tree import DataStoreTree

class AbstractTree(DataStoreTree):

    def __call__(self, idnumber, compare=False):
        if len(idnumber) == 4:
            users = self.users.find_many_with_callback(lambda u: u.idnumber.startswith(idnumber))
            if not users:
                print("No family info found")
            else:
                users.sort(key=lambda u: 10 * len([1 for c in u.idnumber if c == 'P']))
                for user in users:
                    self(user.idnumber)
                    print('\n********\n')

        else:
            user = self.users.get(idnumber)
            if user is None:
                print("No such user {}".format(idnumber))
            else:
                print('User {0.kind} "{0.name}" [{0.idnumber}] {1}'.format(user, "({})".format(user.homeroom) if hasattr(user, 'homeroom') else ''))
                links = self.parentchildlink.get(user.idnumber).links
                link_output = []
                for link in links:
                    lobj = self.users.get(link)
                    link_output.append( "\t=> Linked to {0.kind} {0.name} ({0.idnumber})".format(lobj) )
                print("\n".join(link_output))
                # if hasattr(user, 'parents'):
                #     parent_output = []
                #     for parent in user.parents:
                #         pobj = self.parents.get(parent)
                #         parent_output.append( "Parent: \"{0.name}\": {0.idnumber}".format(pobj) )
                #     print("\n".join(parent_output))

                cohorts = self.cohorts.get(idnumber)
                if cohorts is None:
                    print('<not enrolled in any cohorts')
                else:
                    print("Cohorts {}".format(len(cohorts.cohorts)))
                    print('\t' + ", ".join(cohorts.cohorts))

                enrollments = self.enrollments.get(idnumber)
                if enrollments is None:
                    print('<no enrollments>')
                else:
                    print('Enrollments {}:'.format(len(enrollments.enrollments)))
                    for enrollment in enrollments.enrollments:
                        c, g, r = enrollment
                        course = self.courses.get(c)
                        if course is None:
                            print('\t', '"{}" does not have stored course'.format(c))
                            continue
                        group = self.groups.get(g)
                        if group is None:
                            print('\t', 'Group {} does not have stored group'.format(g))
                            continue
                        teachers = [self.staff.get(t) for t in group.teachers]
                        # if teacher is None:
                        #   print('\t', 'Teacher {} does not have accompanying teachers'.format(group.teachers))
                        #   continue
                        print('\t', "\"{0.name}\" ({5}{0.moodle_shortcode}) [{2.section}] taught by '{1}' in group '{2.idnumber}' (and {3} others) as {4}".format(course, ",".join([t.name for t in teachers if t]), group, len(group.students), r, course._shortcode + '->' if course._shortcode else ''))

    def diff(self, other, idnumber):
        self(idnumber)
        print('\n-----\n')
        other(idnumber)
        this = self.users.get(idnumber)
        that = self.users.get(idnumber)
        print("\n---DIFFS---\n")
        for item in self - other:
            if item.idnumber == idnumber:
                print(item.message)
        print('===============')

    def report(self, other):
        """
        Seeks out how many are unique:
        """
        same = 0
        different = 0
        for my_branch, other_branch in [ (self.students, other.students), (self.staff, other.staff), (self.parents, other.parents)]:
            for user in my_branch.get_objects():
                other_user = other_branch.get(user.idnumber)
                if user is other_user:
                    same += 1
                else:
                    different += 1

        print("Same: {}".format(same))
        print("Different: {}".format(different))

    def go_filter(self, other, filter_={}):
        other.set_filter(filter_)
        self >> other