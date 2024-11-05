# -*- coding: utf-8 -*-
import argparse
import logging
from collections import namedtuple

from tfutils.controllers.blockdate import ImportDateHandler, MovedDateHandler
from tfutils.controllers.forcedremotesource import ForcedRemoteSourceHandler
from tfutils.controllers.sourceswap import SourceSwapHandler

HandlerInfo = namedtuple("HandlerInfo", ("handler_cls", "handler_obj", "init_parser"))

log = logging.getLogger("tfutils")


class TFUtils:
    handlers = [
        ForcedRemoteSourceHandler,
        ImportDateHandler,
        MovedDateHandler,
        SourceSwapHandler,
    ]

    def __init__(self):
        self.commands = {}

    def _init_handlers(self, parser):
        subparser = parser.add_subparsers(dest="command")

        for handler_cls in self.__class__.handlers:
            handler = handler_cls(self, parser)
            cmd_parser = handler._init(parser, subparser)
            handler.add_arguments(cmd_parser)
            self.commands[handler.get_name()] = HandlerInfo(
                handler_cls, handler, cmd_parser
            )

    def get_logger(self):
        return log

    def add_arguments(self, parser):
        parser.add_argument("--verbose", "-v", action="count", default=1)
        return parser

    def _handle(self, options):
        options.verbose = 40 - (10 * options.verbose) if options.verbose > 0 else 0
        logging.basicConfig(
            level=options.verbose,
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        for name, handler in self.commands.items():
            if handler.handler_obj.itsme(options):
                handler.handler_obj.handle(options)

    def do(self):
        parser = argparse.ArgumentParser()
        parser = self.add_arguments(parser)
        self._init_handlers(parser)
        options = parser.parse_args()
        self._handle(options)


def main():
    app = TFUtils()
    app.do()


if __name__ == "__main__":
    main()
