import file
import config_file
import logger

file_utils = file
configs = config_file

logger = logger


def get_configuration(file):
    # TODO: select config based on filename
    return configs.SSHConfig()
