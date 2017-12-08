import file
import config_file
import logger

file_utils = file
configs = config_file

logger = logger

logger.setup_loggers(log_fname=configs.inspector_config.get_logfile_path())


def get_configuration(file):
    # TODO: select config based on filename
    return configs.SSHConfig()
