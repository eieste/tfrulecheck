import argparse


class Command(object):
    name = None
    help = None


    def __init__(self, parent, parser):
        self._cmd = parent
        self.parser = parser

    def _init(self, parser: None | argparse.ArgumentParser=None) -> argparse.ArgumentParser:
        if parser is None:
            parser = self.parser
        subparsers = parser.add_subparsers(dest='command')
        return subparsers.add_parser(self.get_name(), help=self.get_help())

    def get_name(self):
        if self.__class__.name is None:
            raise NotImplementedError("Please give your Command a name arg ")
        return self.name

    def get_help(self):
        if self.__class__.help is None:
            raise NotImplementedError("Please give your Command a help arg")
        return self.help
    
    def get_logger(self):
        return self._cmd.get_logger()

    # Overwrite this method to attach Arguments to the existing parser
    def add_arguments(self, parser: argparse.ArgumentParser | None) -> argparse.ArgumentParser:
        if parser is None:
            parser = self.parser
        return parser

    def itsme(self, options: argparse.Namespace) -> bool:
        if options.command == self.get_name():
            return True
        return False

    def handle(self, options: argparse.Namespace) -> dict:
        return {}
