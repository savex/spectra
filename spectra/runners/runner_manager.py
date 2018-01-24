from spectra import const
from spectra import utils
import spectra.resourse_parsers
from spectra.runners.ssh_runner import SSHRunner
from spectra.runners.local_runner import LocalRunner


_localtargets = ['local', 'localhost']
_parsers = spectra.resourse_parsers


class RunnerManager(object):
    def __init__(self):
        self.default_ssh_runner = SSHRunner
        self.default_local_runner = LocalRunner

        self.default_runner_type = const.TYPE_RUNNER_SSH

    def prepare_runner(self, runner_type):
        if runner_type == const.TYPE_RUNNER_LOCAL:
            return self.default_local_runner
        elif runner_type == const.TYPE_RUNNER_SSH:
            return self.default_ssh_runner

        raise Exception("Runner Type not implemented: {}".format(str(type)))

    def run_script(self, target, profile):
        # TODO: parse target and prepare runner
        if target in _localtargets:
            _runner = self.prepare_runner(runner_type=const.TYPE_RUNNER_LOCAL)
        else:
            _runner = self.prepare_runner(runner_type=const.TYPE_RUNNER_SSH)

        # TODO: parse dict and get corresponding script types
        # resource is a config like file
        # keys as resource types
        # values are resource names or commands

        _group = profile._section_name

        _value = profile.get_value
        _script = "_parsers.{}({})".format(_type, _value)
        _result = _runner.query_resource(_script, target=target)

        # check result for 200, 201, 301, 404, 403
        result = _result

        return _result
