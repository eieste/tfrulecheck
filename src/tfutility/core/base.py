# -*- coding: utf-8 -*-
import argparse

from tfutility.core.abstract import AbstractCommand


class Command(AbstractCommand):
    name = None
    help = None

    def _init(
        self,
        parser: None | argparse.ArgumentParser = None,
        subparser: None | argparse.ArgumentParser = None,
    ) -> argparse.ArgumentParser:
        if parser is None:
            parser = self.parser
        return subparser.add_parser(self.get_command_name(), help=self.get_help())

    # Overwrite this method to attach Arguments to the existing parser
    def add_arguments(
        self, parser: argparse.ArgumentParser | None
    ) -> argparse.ArgumentParser:
        if parser is None:
            parser = self.parser
        return parser

    def handle(self, options: argparse.Namespace) -> dict:
        return {}
