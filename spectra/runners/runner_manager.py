from spectra import const
from spectra.resourse_parsers.proc import ProcessInfo
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

    @staticmethod
    def prepare_script(resource_type):
        # TODO: parse resource type, hardcoded proc so far
        _fn_instance = ProcessInfo.get_target_proc_info
        return _fn_instance

    def run_script(self, target, resource_list):
        # TODO: parse target and prepare runner
        _runner = self.prepare_runner()

        # TODO: parse dict and get corresponding script types
        _script = self.prepare_script(const.TYPE_RESOURCE_PROCESS)

        _result = _runner.query_resource(_script)

        # check result for 200, 201, 301, 404, 403
        result = _result

        return _result
