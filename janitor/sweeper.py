import re

from subprocess import Popen, PIPE

from common import logger
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

        sweep_items_list = self._config.sections()
        sweep_items_list.remove(section_name)
        for sweep_item in sweep_items_list:
            _item = {}
            _list_action_cmd = self._config.get(
                sweep_item,
                _list_action_label
            )
            _sweep_action_cmd = self._config.get(
                sweep_item,
                _sweep_action_label
            )

            _item[_list_action_label] = {}
            _item[_sweep_action_label] = {}

            _item[_list_action_label]["cmd"] = _list_action_cmd
            _item[_list_action_label]['output'] = None
            _item[_list_action_label]['error'] = None
            _item[_list_action_label]['return_code'] = None

            _item['data'] = None

            _item[_sweep_action_label]["cmd"] = _sweep_action_cmd
            _item[_sweep_action_label]["pool"] = {}

            self.sweep_items[sweep_item] = _item

    @property
    def sections_list(self):
        _keys = self.sweep_items.keys()
        _keys.sort()
        return _keys

    @property
    def list_actions(self):
        return ([self.sweep_items[key][_list_action_label]] for key in
                self.sweep_items.keys())

    @property
    def sweep_actions(self):
        return ([self.sweep_items[key][_sweep_action_label]] for key in
                self.sweep_items.keys())

    def get_section_data(self, section):
        return self.sweep_items[section]["data"]

    @staticmethod
    def _action_process(cmd):
        logger.debug("...cmd: '{}'".format(cmd))
        _cmd = cmd.split()
        sweep_process = Popen(_cmd, stdout=PIPE, stderr=PIPE)
        _output, _err = sweep_process.communicate()
        _rc = sweep_process.returncode

        # log it
        logger.debug(
            "process [{}] '{}' returned\n"
            "--- start output ---\n{}\n--- end output ---\n"
            "Error: '{}'\n"
            "Return code: {}".format(
                sweep_process.pid,
                cmd,
                _output,
                _err,
                _rc
            )
        )
        return _output, _err, _rc

    def _do_list_action(self, section):
        # execute the list action

        _out, _err, _rc = self._action_process(
            self.sweep_items[section][_list_action_label]["cmd"]
        )

        # save it
        self.sweep_items[section][_list_action_label]["output"] = _out
        self.sweep_items[section][_list_action_label]["error"] = _err
        self.sweep_items[section][_list_action_label]["return_code"] = _rc

        # Handle result
        _data = _out.splitlines()
        self.sweep_items[section]["data"] = _data

        return _rc

    def _do_sweep_action(self, section):
        # execute the list action
        return self._action_process(
            self.sweep_items[section][_sweep_action_label]
        )

    def _do_filter_action(self, section):
        # filter data set
        _data = []
        _raw_data = self.sweep_items[section]["data"]
        for data_item in _raw_data:
            logger.debug("About to apply filter for '{}'".format(
                data_item
            ))
            _filtered_data_item = self.common_filter.match(data_item)
            if _filtered_data_item is not None:
                logger.debug("..matched value '{}'".format(
                    _filtered_data_item.string
                ))
                _data.append(_filtered_data_item.string)

        self.sweep_items[section]["data"] = _data

        return

    def do_action(self, action, section=None):
        if section is None:
            # Do all actions in order
            _sections = self.sweep_items.keys()
            _sections.sort()
            logger.info("...{} sections total".format(_sections.__len__()))

            # TODO: use gevent to generate subprocess
            for index in range(len(_sections)):
                _section = _sections[index]
                logger.debug("...running action '{}' for section '{}'".format(
                    str(action.__name__),
                    _section
                ))
                action(_section)

            logger.info("...done")
        else:
            logger.info("--> {}".format(section))
            action(section)

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

    def filter_action(self, section=None):
        # Do filter action according to selected filter
        logger.info("Filter action started")
        self.do_action(self._do_filter_action, section=section)

        return
