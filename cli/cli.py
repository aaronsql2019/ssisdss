from dss.settings import setup_settings
import pickle
import click

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

        if readfromdisk or writetodisk:
            import ssis_dss_settings
            path = ssis_dss_settings.get("DEFAULT", "path_to_cache")
            if not path:
                path = '/tmp/default.cache'
        else:
            path = None

        if readfromdisk:
            # Read the store from disk
            try:
                with open(path, 'rb') as _f:
                    data = pickle.load(_f)

                self.source._metastore._store = data

                if writetodisk:
                    # We just read in, don't need to write it out again
                    writetodisk = False
            except FileNotFoundError:
                click.echo(click.style("Not found, reading in manually", fg='red'))
                +self.source
                +self.dest
        else:
            click.echo(click.style("Reading in autosend", fg='green'))
            +self.source
            click.echo(click.style("Reading in moodle", fg='green'))
            +self.dest

        self.dest.set_template(template)

        if writetodisk:
            # Write the store to disk
            data = self.source._metastore._store
            import sys
            click.echo(click.style("Attemping to write {}mb of data to file".format(sys.getsizeof(data)), fg='yellow'))
            with open(path, 'wb') as _f:
                pickle.dump(data, _f)

    def init_pspfsyncer(self):
        self.source = self.autosend_csv
        self.dest = self.postfix

