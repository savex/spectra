import os
import sqlite3

from spectra.utils.config_file import DBConfig

db_config = DBConfig()


class DBStorage(object):
    _connection = None

    def __init__(self):
        self.db_path = os.path.abspath(db_config.get_db_filename())
        self._connection = sqlite3.connect(self.db_path)

        self._cursor = self._connection.cursor()

    def create_all_tables(self, force=False):
        # create profile tables if they are not there
        # check if table exist, on force - delete it

        # profiles
        # self._cursor.execute()

        # collected values
        pass

    def add_check(self, check_path, value):
        pass

    def get_all_profile_checkpoints(self):
        pass

    def list_profiles(self):
        pass

    def insert_profile(self, profile_dict):
        pass

    def get_profile(self, profile_type):
        pass
