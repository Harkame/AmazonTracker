import argparse

import logging

import os

logger = logging.getLogger(__name__)


def get_arguments(arguments):
    argument_parser = argparse.ArgumentParser(
        description="Script to download mangas from JapScan",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )

    argument_parser.add_argument(
        "-c",
        "--config_file",
        help="""Set config file
Example : python japscandownloader/main.py -c /home/myconfigfile.yml""",
        type=str,
    )

    argument_parser.add_argument(
        "-e",
        "--email",
        help="""Gmail address
Example : python amazontracker/main.py -l mymailadress@gmail.com""",
        type=str,
        required=True,
    )

    argument_parser.add_argument(
        "-p",
        "--password",
        help="""Gmail password
Example : python amazontracker/main.py -p mypassword""",
        type=str,
        required=True,
    )

    argument_parser.add_argument(
        "-s",
        "--sleep",
        help="""Sleeping time between requests
Example : python amazontracker/main.py -s 3500""",
        type=float,
    )

    argument_parser.add_argument(
        "-v",
        "--verbose",
        help="""Active verbose mode, support different level
Example : python japscandownloader/main.py -vv""",
        action="count",
    )

    return argument_parser.parse_args(arguments)
