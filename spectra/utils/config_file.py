import ConfigParser
import os

import spectra

pkg_dir = os.path.dirname(__file__)
pkg_dir = os.path.join(pkg_dir, os.path.pardir, os.path.pardir)
pkg_dir = os.path.normpath(pkg_dir)

_default_config_path = os.path.join(pkg_dir, 'etc', 'inspector.conf')


class ConfigFileBase(object):
    _truth = ['true', '1', 't', 'y', 'yes', 'yeah', 'yup',
              'certainly', 'uh-huh']
    _config = None
    _section_name = None

    def __init__(self, section_name, filepath=None):
        self._section_name = section_name
        self._config = ConfigParser.ConfigParser()
        if filepath is not None:
            self._config.read(self._ensure_abs_path(filepath))
        else:
            self._config.read(_default_config_path)

    def force_reload_config(self, path):
        _path = self._ensure_abs_path(path)
        self._config.read(_path)

    @staticmethod
    def _ensure_abs_path(path):
        if path.startswith('~'):
            path = os.path.expanduser(path)
        else:
            path = path

        # make sure it is absolute
        if not os.path.isabs(path):
            return os.path.join(pkg_dir, path)
        else:
            return path

    def _ensure_boolean(self, _value):
        if _value.lower() in self._truth:
            return True
        else:
            return False

    def get_value(self, key):
        return self._config.get(self._section_name, key)


class InspectorConfig(ConfigFileBase):
    def __init__(self):
        spectra.utils.configs.ConfigFileBase.__init__(self, "InspectorConfig")

    def get_default_host_origin(self):
        # get path
        return self.get_value('default_hosts_origin')

    def get_default_inspection_set(self):
        return self.get_value('default_inspection_set')


class ResourceParsersConfig(ConfigFileBase):
    def __init__(self):
        super(ResourceParsersConfig, self).__init__("ResourceParsers")

    def get_proc_parser_filename(self):
        return self.get_value("proc")

    def get_config_parser_filename(self):
        return self.get_value("config")

    def get_file_parser_filename(self):
        return self.get_value("file")


class DBConfig(ConfigFileBase):
    def __init__(self):
        super(DBConfig, self).__init__("db")

    def get_db_filename(self):
        _file = self.get_value("db_file")
        return self._ensure_abs_path(_file)


class SSHConfig(ConfigFileBase):
    def __init__(self):
        super(SSHConfig, self).__init__("ssh")

    def get_options(self):
        return self.get_value("default_options")
