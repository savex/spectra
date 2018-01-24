import os
import sys
import argparse

import janitor

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
    parser = MyParser(prog=_title)

    log = janitor.utils.logger.shell_logger
    log.info(_title)

    # arguments
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
        'profile',
        help="Cleaning profile to execute"
    )

    args = parser.parse_args()

    # Load profile

    # Collect all data

    # Log collected data stats

    # Do clean actions

    return

# Entry
if __name__ == '__main__':
    sweeper_cli()
    sys.exit(0)
