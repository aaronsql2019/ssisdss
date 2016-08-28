"""
Command line stuff
"""

from ssis_dss.trees import AutosendTree, MoodleTree

import click
#import ssis_dss   #(see comment on line 14 for why this is commented out)
from cli.cli import CLIObject

@click.group()
@click.option('--test/--dont_test', default=False, help="Uses test information")
@click.option('--template', type=click.STRING, default=None, help="Define the template")
@click.pass_context
def ssisdss_test(ctx, test, template):
    # Doesn't do much now, but leave it as boilerplate for when there are global flags n such
    ctx.obj = CLIObject(test)
    ctx.obj.template = template

    if ctx.obj.test or template is None:
        template = "dss.templates.DefaultTemplate"
    else:
        template = "ssis_dss.templates.templates.{}".format(template)

@ssisdss_test.command("MoodleInterface")
@click.pass_obj
def ssisdss_moodleinterface(obj):
    if obj.test:
        click.echo("Doens't make sense to test with a go command, do you mean 'embed' instead?")
        return

    from ssis_dss.importers.moodle_importers import MoodleImporter
    moodle_tree = MoodleTree()
    moodle = MoodleImporter(moodle_tree, moodle_tree.students)

    from IPython import embed;embed()

@ssisdss_test.command("MoodleSchedule")
@click.pass_obj
def ssisdss_moodleschedule(obj):
    from ssis_dss.importers.moodle_importers import MoodleImporter
    moodle_tree = MoodleTree()

    moodle = MoodleImporter(moodle_tree, moodle_tree.students)
    for item in moodle.bell_schedule():
        print(item)
    from IPython import embed;embed()

@ssisdss_test.command("Pexpect")
@click.pass_obj
def ssisdss_testpexpect(obj):
    from ssis_dss.moodle.php import PHP

    p = PHP()
    here=""
    while here.strip() != "quit":
        print("Manually type the command with params")
        here = input()
        print(p.command(here.strip(), ''))

@ssisdss_test.command("output_enrollments")
@click.argument('path', type=click.File(mode='w'), default=None)
@click.pass_obj
def output_enrollments(obj, path):
    autosend = AutosendTree()
    moodle = MoodleTree()
    +autosend
    +moodle

    for action in autosend - moodle:
        if action.func_name in ['remove_enrollments_from_enrollments']:
            if not action.idnumber.endswith('PP'):
                course, group, role = action.attribute
                path.write("deenrol_user_from_course {0.idnumber} {1}\n".format(action, course))

@ssisdss_test.command("output_group_additions")
@click.pass_obj
def output_group_additions(obj):    
    autosend = AutosendTree()
    moodle = MoodleTree()
    +autosend
    +moodle

    for action in autosend - moodle:
        if action.idnumber.startswith('4813P'):
            print(action)

@ssisdss_test.command("output_deenrol_old_students_parents")
@click.argument('path', type=click.File(mode='w'), default=None)
@click.pass_obj
def output_deenrol_old_parents_students(obj, path):
    autosend = AutosendTree()
    moodle = MoodleTree()
    +autosend
    +moodle

    from ssis_dss.importers.moodle_importers import MoodleImporter
    moodledb = MoodleImporter(moodle, moodle.students)

    old_parents = moodle.parents.keys() - autosend.parents.keys()
    old_students = moodle.students.keys() - autosend.students.keys()

    old_users = old_parents.union(old_students)

    for user_idnumber, enrollment_type, course_idnumber in moodledb.get_user_enrollments():
        if user_idnumber in old_users:
            if user_idnumber.endswith('PP'):
                continue
            if enrollment_type == 'manual' and course_idnumber and not course_idnumber.startswith('OLP:'):
                path.write("deenrol_user_from_course {0} {1}\n".format(user_idnumber, course_idnumber))

@ssisdss_test.command("output_deenrol_old_students")
@click.option('--verbose', default=False, help="Output stuff")
@click.argument('path', type=click.File(mode='w'), default=None)
@click.pass_obj
def output_deenrol_old_students(obj, path, verbose):
    autosend = AutosendTree()
    moodle = MoodleTree()
    +autosend
    +moodle

    from IPython import embed;embed()

    for idnumber in moodle.students.keys() - autosend.students.keys():
        enrollment_data = moodle.enrollments.get(idnumber)
        if enrollment_data is None:
            verbose and print("No enrollment info for {}".format(idnumber))
        if enrollment_data:
            for enrollment in enrollment_data.enrollments:
                course, group, role = enrollment
                verbose and print('\t', idnumber, course)
                path.write("deenrol_user_from_course {0} {1}\n".format(idnumber, course))
        else:
            verbose and print("No enrollments {}".format(idnumber))


@ssisdss_test.command("output_remove_old_groups")
@click.argument('path', type=click.File(mode='w'), default=None)
@click.pass_obj
def output_remove_old_groups(obj, path):
    autosend = AutosendTree()
    moodle = MoodleTree()
    +autosend
    +moodle

    from IPython import embed;embed();exit()

    for idnumber in moodle.groups.keys() - autosend.groups.keys():
        if idnumber:
            group = moodle.groups.get(idnumber)
            if group and group.idnumber:
                path.write("delete_group_for_course '{0.idnumber}'\n".format(group))

@ssisdss_test.command("output_remove_old_groups")
@click.argument('path', type=click.File(mode='w'), default=None)
@click.pass_obj
def output_remove_old_groups(obj, path):
    autosend = AutosendTree()
    moodle = MoodleTree()
    +autosend
    +moodle

    for idnumber in moodle.groups.keys() - autosend.groups.keys():
        if idnumber:
            group = moodle.groups.get(idnumber)
            if group and group.idnumber:
                path.write("delete_group_for_course '{0.idnumber}'\n".format(group))

@ssisdss_test.command("output_course_mappings")
@click.argument('path', type=click.File(mode='w'), default=None)
@click.pass_obj
def output_remove_old_courses(obj, path):
    autosend = AutosendTree()
    moodle = MoodleTree()
    +autosend
    +moodle

    from ssis_dss.importers.moodle_importers import MoodleImporter
    moodle = MoodleImporter(moodle, moodle.students)
    existing_courses = []

    for course_idnumber, _, _ in moodle.get_teaching_learning_courses():
        existing_courses.append(course_idnumber)

    for course in autosend.courses.values():
        comment = "present" if course.idnumber in existing_courses else "MISSING"
        print("{comment}: {orig} -> {translated}".format(orig=course._shortcode, translated=course.moodle_shortcode, comment=comment))

@ssisdss_test.command("output_group_migration")
@click.argument('path', type=click.File(mode='w'), default=None)
@click.pass_obj
def output_group_migration(obj, path):
    autosend = AutosendTree()
    moodle = MoodleTree()
    click.echo("processing autosend...")
    +autosend
    click.echo("processing moodle...")
    +moodle

    from ssis_dss.importers.moodle_importers import MoodleImporter
    moodle_db = MoodleImporter(moodle, moodle.students)

    for group in moodle.groups.values():
        grades = set()
        for member_idnumber in group.members:
            student = autosend.students.get(member_idnumber)
            if student:
                grades.add(student._grade)

        new_group = [ag for ag in autosend.groups.values() if ag._old_group == group.idnumber]
        old_name = moodle_db.get_column_from_row('group', 'name', id=group._id)
        if not new_group:
            new_name = '[OLD] {}'.format(old_name)
            moodle_db.update_table('group', where=dict(idnumber=group.idnumber), name=new_name)
            path.write('Found OLD group, renamed: {}\n'.format(group.idnumber))
            continue

        new_group = new_group[0].idnumber
        old_name = moodle_db.get_column_from_row('group', 'name', id=group._id)

        if len(list(grades)) > 1:
            path.write("Group {} in course {} has more than one grade: {}\n".format(group.idnumber, group.course, grades))
            new_name = '[OLD] {}'.format(old_name)
            moodle_db.update_table('group', where=dict(idnumber=group.idnumber), name=new_name)
        elif len(list(grades)) == 1:
            old_name_split = old_name.split(' ')
            new_name = "{} course{} sec{}.{}".format(old_name_split[0], old_name_split[1], grades.pop(), old_name_split[2])
            path.write("Changed group idnumber from {} to {} in course {}\n".format(group.idnumber, new_group, group.course))
            moodle_db.update_table('group', where=dict(idnumber=group.idnumber), name=new_name)
            moodle_db.update_table('group', where=dict(idnumber=group.idnumber), idnumber=new_group)
        else:
            new_name = '[OLD] {}'.format(old_name)
            moodle_db.update_table('group', where=dict(idnumber=group.idnumber), name=new_name)
            path.write("Group {} with no members, cannot know grade!\n".format(group.idnumber))
