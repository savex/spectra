import os
import platform
import subprocess


def get_target_proc_info(proc_name_re):

    _command = "ps -ax -opid,start,state,rss,command | " \
               "grep -e {} | grep -v grep".format(proc_name_re)
    _ps = subprocess.Popen(
        _command.split(),
        stdout=subprocess.PIPE
    ).communicate()[0].decode()

    # TODO: add parsing for process values later

    return _ps

user = os.getlogin()
cpu_name = platform.processor()
