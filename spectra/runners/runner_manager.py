from spectra import const
from spectra.runners.ssh_runner import SSHRunner
from spectra.runners.local_runner import LocalRunner


class RunnerManager(object):
    def __init__(self):
        self.default_ssh_runner = SSHRunner()
        self.default_local_runner = LocalRunner()

        self.default_runner_type = const.TYPE_REMOTE_SSH

    def prepare_runner(self, runner_type=const.TYPE_REMOTE_SSH):
        if runner_type == const.TYPE_LOCAL:
            return self.default_local_runner
        elif runner_type == const.TYPE_REMOTE_SSH:
            return self.default_ssh_runner

        raise Exception("Runner Type not implemented: {}".format(str(type)))

    def run_script(self, target, fn):
        _runner = self.prepare_runner()

        _result = _runner.query_resource()
        return _result
