import os


class ProcessInfo(object):
    def __init__(self):
        pass

    @staticmethod
    def get_target_proc_info(proc_name_re):

        print("Hello from this thread executed by '{}'.".format(os.getlogin()))

        return
