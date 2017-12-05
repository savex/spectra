import file
import config_file

file_utils = file
configs = config_file


def get_configuration(file):
    # TODO: select config based on filename
    return configs.SSHConfig()
