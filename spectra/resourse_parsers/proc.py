import os


class ProcessInfo(object):
    def __init__(self):
        pass

    @staticmethod
    def get_target_proc_info():

        print("Hello from this thread executed by '{}'.".format(os.getlogin()))

        return
