#!/usr/bin/env python3

import sys
from ui_bundle_installer import UIBundleInstaller

arguments_map = {
    'install': 'install',
    'uninstall': 'uninstall',
    'list': 'list_installed',
    'repo': 'list_repository',
}

help_message = """
Replaced UI elements are backed up and can be restored later.

Usage: ui-install <subcommand> [param ...], where <subcommand> is as follows:

    list                list installed bundles
    repo                list installable bundles in the repository

    remove [param]      remove specified bundles
                          list known removable bundles with `list`
    install [param]     install specified bundles
                          list know installable bundles with `repo`
"""


def main():
    # no arguments
    if len(sys.argv) < 2:
        print(help_message)
        return 2

    # subcommand doesn't exist
    option = arguments_map.get(sys.argv[1], None)
    if option is None:
        print(help_message)
        return 1

    # all is good, run subcommand
    UIBundleInstaller.run_command(option, sys.argv[2:])
    print('')

    return 0


if __name__ == '__main__':
    main()
