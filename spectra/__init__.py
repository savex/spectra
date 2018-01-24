import resourse_parsers
import utils

utils = utils
parsers = resourse_parsers
logger, logger_api = utils.logger.setup_loggers(
    "spectra",
    log_fname=utils.configs.inspector_config.get_logfile_path()
)
