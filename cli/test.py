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
    for item in moodle.import_students_with_links():
        print(item)
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


