import os
import subprocess

from spectra.resourse_parsers.proc import ProcessInfo

# all functions is just a sample yet.
class SSHRunner(object):
    def __init__(self, do_piped_output=True):
        self.dir = os.curdir()
        self.cmd = "python"
        self.is_piped = do_piped_output
        thread = subprocess.Popen("", executable=self.cmd)

        pass

    def run_bash_script(self, data):
        pass

    def run_python_script(self, data):
        pass

    def query_resource(self, dict):
        # TODO: parse dict
        _fn_instance = ProcessInfo.get_target_proc_info

        # do get process info on remote host
        pass

    def get_resource_info_by_list(self, list):
        pass
