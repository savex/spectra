import os
import sys
import argparse

from spectra.utils.config_file import InspectorConfig
from spectra.runners.runner_manager import RunnerManager
from spectra.db.sqlite import DBStorage

pkg_dir = os.path.dirname(__file__)
pkg_dir = os.path.normpath(pkg_dir)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Error: {0}\n\n'.format(message))
        self.print_help()
        sys.exit(2)


def help_message():
    print"Please, execute this tool with a correct option:\n" \
         " 'collect' option to gather all info to be looked after \n" \
         " 'inspect' option to test current situation and timestamp it \n" \
         " 'diff' option to see what has changed since last '-nX' times \n" \
         " 'report' option to generate fancy trend report \n"

    return


# main
def inspector_cli_main():
    parser = MyParser(prog="Spectra:Inspector CLI Util")

    # arguments

    args = parser.parse_args()

    # Init Config
    config = InspectorConfig()

    # load checkpoints from DB that was collected so far
    _storage = DBStorage()
    all_checks = _storage.get_all_profile_checkpoints()

    # collect info mode

    # inspect mode
    run_manager = RunnerManager()
    for check in all_checks:
        _result = run_manager.run_script("127.0.0.1", check)
        _storage.add_check(check['check_path'], _result)

    # diff mode

    # report mode

    pass


if __name__ == '__main__':
    inspector_cli_main()
    sys.exit(0)
