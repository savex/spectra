import os

from utils.config_file import ConfigFileBase

pkg_dir = os.path.dirname(__file__)
pkg_dir = os.path.normpath(pkg_dir)
pkg_dir = os.path.abspath(pkg_dir)

_default_config_path = os.path.join(pkg_dir, 'etc')
_inspector_default_config_name = 'janitor.conf'

_default_config = os.path.join(
    _default_config_path,
    _inspector_default_config_name
)

print _default_config


class SweeperConfig(ConfigFileBase):
    def __init__(self, filename):
        super(SweeperConfig, self).__init__(
            "SweeperConfig",
            filepath=filename
        )

    def get_logfile_path(self):
        _path = self.get_value('logfile')
        return self._ensure_abs_path(_path)

sweeper_config = SweeperConfig(_default_config)
