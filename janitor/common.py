import utils
from sweeper_config import sweeper_config

utils = utils
logger, logger_api = utils.logger.setup_loggers(
    "janitor",
    log_fname=sweeper_config.get_logfile_path()
)
