# -*- coding: utf-8 -*-
import argparse
import logging
from collections import namedtuple

from tfutils.controllers.blockdate import ImportDateHandler, MovedDateHandler
from tfutils.controllers.forcedremotesource import ForcedRemoteSourceHandler
from tfutils.controllers.sourceswap import SourceSwapHandler

HandlerInfo = namedtuple("HandlerInfo", ("handler_cls", "handler_obj", "init_parser"))

log = logging.getLogger("tfutils")


class TfUtils:
    """
    TfUtils Initial class. This class initializes all CLI arguments
    """

    # List of all Available CLI Handlers
    handlers = [
        ForcedRemoteSourceHandler,
        ImportDateHandler,
        MovedDateHandler,
        SourceSwapHandler,
    ]

    def __init__(self):
        self.commands = {}

    def _init_handlers(self, parser: argparse.ArgumentParser):
        """
        initialize all cli argparse commands

        :type parser: argparse.ArgumentParser
        :param parser: the main argparser
        """
        subparser = parser.add_subparsers(dest="command")

        for handler_cls in self.__class__.handlers:
            handler = handler_cls(self, parser)
            cmd_parser = handler._init(parser, subparser)
            handler.add_arguments(cmd_parser)
            self.commands[handler.get_name()] = HandlerInfo(
                handler_cls, handler, cmd_parser
            )

    def get_logger(self) -> logging.Logger:
        """
        get logger instance

        :return: the logger instance
        :rtype: logging.Logger
        """
        return log

    def add_arguments(self, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Add global arguments to the parser

        :param parser: the main argparser
        :type parser: argparse.ArgumentParser
        :return: the main argparser with attached global arguments
        """
        parser.add_argument("--verbose", "-v", action="count", default=1)
        return parser

    def _handle(self, options: argparse.Namespace):
        """
        handle the cli arguments

        :param options: the parsed cli arguments
        :type options: argparse.Namespace
        """

        # set default loglevel to Info
        options.verbose = 40 - (10 * options.verbose) if options.verbose > 0 else 0
        logging.basicConfig(
            level=options.verbose,
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # find command which is used by user
        for name, handler in self.commands.items():
            if handler.handler_obj.itsme(options):
                handler.handler_obj.handle(options)

    def _init_parser(self) -> argparse.ArgumentParser:
        """
        Create the main Parser with all subparsers arguments
        """
        parser = argparse.ArgumentParser()
        parser = self.add_arguments(parser)
        self._init_handlers(parser)
        return parser

    def do(self):
        """
        Execute command execution
        """
        parser = self._init_parser()
        options = parser.parse_args()
        self._handle(options)


def _get_parser_only() -> argparse.ArgumentParser:
    """
    returns only the initialized parser
    """
    app = TfUtils()
    return app._init_parser()


def main():
    app = TfUtils()
    app.do()


if __name__ == "__main__":
    main()
