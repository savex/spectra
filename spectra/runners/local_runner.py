import os
import subprocess


class LocalRunner(object):
    def __init__(self):
        self.path = os.curdir()
        self.cmd = "python"

    def prepare_runner(self):
        pass

    def query_resource(self, resource_dict):
        pass

    def get_resource_info_by_list(self, resource_list):
        # identify resource type and prepare function
        pass
