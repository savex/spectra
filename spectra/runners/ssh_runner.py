import subprocess
import textwrap
import tempfile
import os
from spectra import utils


# all functions is just a sample yet.
class SSHRunner(object):
    proc = None
    subprocess_output = None

    def __init__(self, host, file_, do_piped_output=True):
        self.dir = os.curdir()
        self.cmd = "python"
        self.is_piped = do_piped_output
        thread = subprocess.Popen("", executable=self.cmd)
        # TODO: savex please refactor code below
        self.file_ = file_
        self.host = host
        # TODO: implement method get_configuration in utils
        # or use existibg config file which stores private key path and user
        self._config = utils.get_configuration(__file__)
        self.priv_key = self._config['priv_key_path']
        self.user = self._config['user']

    def __enter__(self):
        self.subprocess_output = tempfile.TemporaryFile()
        cmd = self._make_ssh_command()
        proc_args = {'stderr': self.subprocess_output}
        proc_args = self._subprocess_add_args(proc_args)
        self.proc = subprocess.Popen(cmd, **proc_args)
        try:
            self._validate_remote_exec()
            # TODO: need to add exception exactly about validation failed
        except Exception as e:
            self._grab_subprocess_output()
        return self

    def _make_ssh_command(self):
        cmd = ['ssh']
        cmd = self._ssh_command_add_auth_arguments(cmd)
        cmd = self._ssh_command_add_extra_arguments(cmd)
        cmd = self._ssh_command_add_destination(cmd)
        cmd = self._ssh_command_add_command(cmd)
        return cmd

    def _ssh_command_add_auth_arguments(self, cmd):
        return cmd + ['-i', self.priv_key]

    def _ssh_command_add_extra_arguments(self, cmd):
        return cmd + [
            '-v',
            '-o', 'BatchMode=yes',
            '-o', 'RequestTTY=no',
            '-o', 'ClearAllForwardings=yes',
            '-o', 'ExitOnForwardFailure=yes',
            '-o', 'StrictHostKeyChecking=no']

    def _ssh_command_add_destination(self, cmd):
        return cmd + ['@'.join((self.user, self.host))]

    def _ssh_command_add_command(self, cmd):
        # TODO: python value hardcoded. Need to add shell parser from file name or another logic
        cmd += ['python']
        return cmd

    def _subprocess_add_args(self, args):
        args['stdin'] = subprocess.PIPE
        args['stdout'] = subprocess.PIPE
        return args

    def _validate_remote_exec(self):
        validate_snippet = textwrap.dedent("""
        import platform

        print platform.platform()
        """).lstrip()

        self.proc.stdin.write(validate_snippet)
        self.proc.stdin.close()

        stdout = self.proc.stdout.fileno()

        print(self.proc.stdout.read())  # it will print script output

    def _grab_subprocess_output(self):
        output = 'There is no any output from SSH process'
        if self.subprocess_output.tell():
            self.subprocess_output.seek(os.SEEK_SET)
            output = self.subprocess_output.read()
        return output
# END

    def run_bash_script(self, data):
        pass

    def run_python_script(self, data):
        pass

    def query_resource(self, target, fn_instance):
        # TODO: parse dict

        # do get process info on remote host
        pass

    def get_resource_info_by_list(self, resource_list):
        pass
