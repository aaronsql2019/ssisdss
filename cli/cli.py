from dss.settings import setup_settings
import pickle

class CLIObject:
    """
    Interface with datastoresync with the requisite info
    """
    def __init__(self, test=False):
        import ssis_dss          # import it here to get the desired behaviour, otherwise it is a click.Group?       
                                    # not sure why, but must be something to do with incompatibility with the click package
                                    # since removing 'import click' statement above fixes it too
        setup_settings(ssis_dss)
        self.test = test
        if self.test:
            from ssis_dss.trees.test_trees import AutosendTree, MoodleTree
        else:
            from ssis_dss.trees import AutosendTree, MoodleTree

        self.autosend_csv = AutosendTree
        self.moodle_db = MoodleTree

        self.postfix = None  # TODO... name change?

    def init_psmdlsyncer(self, template, readfromdisk, writetodisk):
        self.source = self.autosend_csv(read_from_disk=readfromdisk, write_to_disk=writetodisk)
        self.dest = self.moodle_db(read_from_disk=readfromdisk, write_to_disk=writetodisk)
        # if not readfromdisk:
        #     +self.source
        #     +self.dest
        # else:
        #     data = pickle.load(readfromdisk)
        #     self.source = data['source']
        #     self.dest = data['dest']

        self.dest.set_template(template)

        # if writetodisk:
        #     from IPython import embed;embed()
        #     data = {'source': self.source, 'dest': self.dest}
        #     pickle.dump(data, writetodisk)

    def init_pspfsyncer(self):
        self.source = self.autosend_csv
        self.dest = self.postfix

