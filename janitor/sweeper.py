import re

from subprocess import Popen, PIPE

from common import logger, logger_cli
from utils.config import ConfigFileBase

_list_action_label = "list_action"
_sweep_action_label = "sweep_action"


class Sweeper(ConfigFileBase):
    def __init__(
            self,
            filter_regex,
            filepath,
            section_name="sweeper",
    ):
        super(Sweeper, self).__init__(section_name, filepath=filepath)

        # load default values
        self.preserve_order = self.get_value("preserve_order")

        if filter_regex is not None:
            self.common_filter = re.compile(filter_regex)
        else:
            self.common_filter = re.compile(self.get_value("common_filter"))

        self.retry_count = self.get_value("retry")
        self.action_concurrency = self.get_value("concurrency")

        # initialize all sections
        self.sweep_items = {}

        _item = {}
        sweep_items_list = self._config.sections()
        for sweep_item in sweep_items_list:
            _item[_list_action_label] = self._config.get(
                sweep_item,
                _list_action_label
            )
            _item[_sweep_action_label] = self._config.get(
                sweep_item,
                _sweep_action_label
            )
            _item['output'] = None
            _item['error'] = None
            _item['return_code'] = None

            self.sweep_items[sweep_item] = _item

    @property
    def sections_list(self):
        return self.sweep_items.keys().sort()

    @property
    def list_actions(self):
        return ([self.sweep_items[key][_list_action_label]] for key in
                self.sweep_items.keys())

    @property
    def sweep_actions(self):
        return ([self.sweep_items[key][_sweep_action_label]] for key in
                self.sweep_items.keys())

    def list_sections(self):
        _list = self.sweep_items.keys()
        _list.sort()
        return list(_list)

    @staticmethod
    def _action_process(cmd):
        logger.debug("Running process: '{}'".format(cmd))
        sweep_process = Popen(cmd, stdout=PIPE, stderr=PIPE)
        _output, _err = sweep_process.communicate()
        _rc = sweep_process.returncode

        # log it
        logger_api.debug(
            "Output: {}\n"
            "Error: {}\n"
            "Return code: {}".format(
                _output,
                _err,
                _rc
            )
        )
        return _output, _err, _rc

    def _do_list_action(self, section):
        # execute the list action
        return self._action_process(
            self.sweep_items[section][_list_action_label]
        )

    def _do_sweep_action(self, section):
        # execute the list action
        return self._action_process(
            self.sweep_items[section][_sweep_action_label]
        )

    def _do_filter_action(self, section):
        # filter data set
        _data = self.sweep_items[section]["output"]
        for data_item in _data:
            logger.debug("About to apply filter for '{}'".format(
                data_item
            ))
            _filtered_data_item = self.common_filter.match(data_item)
            logger.debug("..filtered value '{}'".format(
                _filtered_data_item
            ))
            data_item = _filtered_data_item

        return

    def do_action(self, action, section=None):
        if section is None:
            # Do all actions in order
            _sections = self.sweep_items.keys()
            _sections.sort()
            logger.info("...{} sections total".format(_sections.__len__()))

            # use gevent to generate subprocess
            pass

            logger.info("...done")
        else:
            logger.info("--> {}".format(section))
            _out, _err, _rc = action(section)

            # save it
            self.sweep_items[section]["output"] = _out
            self.sweep_items[section]["error"] = _err
            self.sweep_items[section]["return_code"] = _rc

    def list_action(self, section=None):
        # get data lists for section
        logger.info("List action started")
        self.do_action(self._do_list_action, section=section)

        # parse output
        pass

        return

    def sweep_action(self, section=None):
        logger.info("Sweep action started")
        self.do_action(self._do_sweep_action, section=section)

        # process return codes
        pass

        return

    def filter_action(self, section=None, filter_regex=None):
        # Do filter action according to selected filter
        logger.info("Filter action started")
        self.do_action(self._do_filter_action, section=section)

        return
