import os
import sys
import argparse

from common import logger, logger_api
from sweeper import Sweeper

pkg_dir = os.path.dirname(__file__)
pkg_dir = os.path.normpath(pkg_dir)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Error: {0}\n\n'.format(message))
        self.print_help()
        sys.exit(2)


def help_message():
    print"Please, execute this tool with a correct option:\n" \
         " 'stat' show count of objects about to clean \n" \
         " 'clean' do the cleaning \n"

    return


# Main
def sweeper_cli():
    _title = "Janitor:Sweeper CLI util"
    _cmd = "sweeper"
    parser = MyParser(prog=_cmd)

    logger.info(_title)

    # arguments
    parser.add_argument(
        "-l",
        "--list-sections",
        action="store_true", default=True,
        help="List sections from the profile, preserve order of execution"
    )

    parser.add_argument(
        "-s",
        "--stat-only",
        action="store_true", default=True,
        help="List objects only, show counts next to each script entry"
    )

    parser.add_argument(
        "--sweep",
        action="store_true", default=False,
        help="Do sweep action of all objects listed"
    )

    parser.add_argument(
        "-f",
        "--filter-regex",
        default=None, help="Overide profile default filter"
    )

    parser.add_argument(
        'profile',
        help="Cleaning profile to execute"
    )

    args = parser.parse_args()

    # Load profile
    sweep = Sweeper(args.filter_regex, args.profile)

    if args.list_sections:
        # only list sections
        log.info("Sections available in profile '{}'".format(args.profile))
        for section in sweep.sections_list:
            log.info("# {}".format(section))
        return

    # TODO: add per-section execution parameter and handler
    # Collect all data
    sweep.list_action()

    # Filter data, override if corresponding parameter is set
    sweep.filter_action()

    # Log collected data stats

    # Do clean actions

    return

# Entry
if __name__ == '__main__':
    sweeper_cli()
    sys.exit(0)
