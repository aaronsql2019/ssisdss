from dss.importers import DefaultImporter
from dss.importers.csv_importer import CSVImporter
from dss.importers.db_importer import PostgresDBImporter

import ssis_dss_settings

class AutosendImporter(CSVImporter):
    """
    Don't read in the username
    """
    _settings = ssis_dss_settings['SSIS_AUTOSEND']
    reader = None

class AutosendStudentsImporter(AutosendImporter):
    def readin(self):
        yield dict(idnumber='wrongusername', lastfirst='Maiden, Flower', homeroom='10B')
        yield dict(idnumber='67890', lastfirst='Daisy, Apple', homeroom='2M')
        yield dict(idnumber='wronggrade', lastfirst='Woopsie, Daisy', homeroom='9F')
        yield dict(idnumber='wronghomeroom', lastfirst='Finally, Nothing', homeroom='10X')

class AutosendTeachersImporter(AutosendImporter):
    def readin(self):
        yield dict(idnumber='newteacherdespitefilter', lastfirst="Filtered Out, Teacher")
        yield dict(idnumber='1111', lastfirst="in Pink, Pretty")
        yield dict(idnumber='2222', lastfirst="Shmoe, Joeanne")

class MoodleImporter(PostgresDBImporter):
    _settings = ssis_dss_settings['SSIS_DB']
    reader = None

    def init(self, *args, **kwargs):
        """
        Make it nothing, don't want to actually do anything (yet)
        """
        pass

    def filter_out(self, **info):
        if info.get('idnumber') == 'newteacherdespitefilter':
            return True
        return False

class MoodleStudentsImporter(MoodleImporter):
    def readin(self):
        yield dict(idnumber='wrongusername', firstname='Flower', lastname='Maiden', homeroom='10B', grade=10, username="wrong")
        yield dict(idnumber='67890', lastname='Daisy', firstname='Apple', homeroom='2M', grade=2, username="appledaisy20")
        yield dict(idnumber='oldstudent', firstname='Goodbye', lastname='Everyone', homeroom="1A", grade=2, username="goodbyeeveryone16")
        yield dict(idnumber='wronggrade', lastname='Woopsie', firstname='Daisy', homeroom='10F', grade=2, username='daisywoopsie20')
        yield dict(idnumber='wronghomeroom', lastname='Finally', firstname='Nothing', homeroom='10Z', grade=10, username='nothingfinally20')


class MoodleTeachersImporter(MoodleImporter):
    def readin(self):
        yield dict(idnumber='newteacherdespitefilter', lastname='Filtered Out', firstname='Teacher')
        yield dict(idnumber='1111', lastname='in Pink', firstname='Pretty')
        yield dict(idnumber='2222', lastname='Shmoe', firstname="Joeanne")
        yield dict(idnumber='oldteacher', lastname='yes', firstname='no')
