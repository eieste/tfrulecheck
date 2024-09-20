import sys
import argparse
import pathlib


class CommandLine:

    def __init__(self, parser=None):
        self.parser = parser
        if parser is None:
            self.parser = self.init_parser()

    def init_parser(self):
        return argparse.ArgumentParser()
    
    def init(self):
        return self.add_arguments()

    def add_arguments(self):
        self.parser.add_argument("--only", type=str, default="all", help="Path to file which should be checked")
        self.parser.add_argument("--no-fail", type=bool, default=False help="Prevent exitcode 1 when errors are exists")
        self.parser.add_argument("-f", "--file", type=pathlib.Path, help="Path to file which should be checked")
        return self.parser
    
    def handle(self):
        return self.parser.parse_args(sys.argv[1:])
    