import sqlite3

from spectra.utils.config_file import DBConfig

db_config = DBConfig()


class DBStorage(object):
    _connection = None
    _profiles_name = "profiles"
    _hosts_name = "hosts"
    _checkpoints_name = "checkpoints"

    def __init__(self, autocommit=True):
        self.db_path = db_config.get_db_filename()
        self._connection = sqlite3.connect(self.db_path)
        self.autocommit = autocommit

    def _close(self):
        self._connection.close()
        self._connection = None

    def _execute_query(self, _sql):
        _res = self._connection.execute(_sql)
        if self.autocommit:
            self._connection.commit()
        return _res.fetchall()

    def _execute_ro_query(self, _sql):
        return self._connection.execute(_sql).fetchall()

    def _table_exists(self, table_name):
        _sql = "select name from sqlite_master " \
               "where type='table' and name='{}'".format(
                    table_name
                )

        _result = self._execute_ro_query(_sql)

        if len(_result) > 0:
            return True
        else:
            return False

    def create_all_tables(self, force=False):
        # create profile tables if they are not there
        # check if table exist, on force - delete it

        _profiles_sql = """create TABLE {}(
        profile_id INTEGER PRIMARY KEY,
        role TEXT,
        profile_name TEXT
        );""".format(self._profiles_name)

        _hosts_sql = """create table {}(
        profile_id INTEGER,
        host_id integer PRIMARY KEY,
        hostname TEXT,
        ip TEXT,
        user TEXT,
        password TEXT,
        keyfile TEXT,
        ssh_options text,
        FOREIGN KEY (profile_id) REFERENCES profiles(profile_id)
        );
        """.format(self._hosts_name)

        _checkpoints_sql = """
        create TABLE {}(
        host_id INTEGER,
        check_path text,
        check_timestamp TIMESTAMP,
        check_value text,
        FOREIGN KEY (host_id) REFERENCES hosts(host_id)
        );
        """.format(self._checkpoints_name)

        # check if tables exists
        # if not do create 'em
        if not self._table_exists(self._profiles_name):
            self._execute_query(_profiles_sql)

        if not self._table_exists(self._hosts_name):
            self._execute_query(_hosts_sql)

        if not self._table_exists(self._checkpoints_name):
            self._execute_query(_checkpoints_sql)

        # collected values
        pass

    def add_check(self, check_path, value):
        pass

    def get_all_profile_checkpoints(self):
        _dict = {}

        _data = self._execute_ro_query("select * from checkpoints")

        return _dict

    def list_profiles(self):
        pass

    def insert_profile(self, profile_dict):
        pass

    def get_profile(self, profile_type):
        pass
