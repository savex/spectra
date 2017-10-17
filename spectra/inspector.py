import os
import sys
import argparse

from spectra.utils.config import InspectorConfigFile

pkg_dir = os.path.dirname(__file__)
pkg_dir = os.path.normpath(pkg_dir)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Error: {0}\n\n'.format(message))
        self.print_help()
        sys.exit(2)


def help_message():
    print"Please, supply this tool with a correct option:\n" \
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
    _config_file_path = os.path.join(pkg_dir, 'etc', 'inspector.conf')
    if args.config_file:
        _config_file_path = args.config_file
    config = InspectorConfigFile(_config_file_path)

    # do something for init :)

    # collect info mode

    # inspect mode

    # diff mode

    # report mode

    pass


if __name__ == '__main__':
    inspector_cli_main()
    sys.exit(0)
