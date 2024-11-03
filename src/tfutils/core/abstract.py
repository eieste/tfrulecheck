import logging
import argparse


class AbstractCommand:

    def __init__(self, parent, parser):
        self._cmd = parent
        self.parser = parser

    def _init(self):
        raise NotImplementedError("Please Implement an _init method")

    def get_logger(self):
        return self._cmd.get_logger()
    
    def add_arguments(self, parser: argparse.ArgumentParser):
        raise NotImplementedError("Please implement an add_arguments method")
    
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

    def itsme(self, options: argparse.Namespace) -> bool:
        if options.command == self.get_name():
            return True
        return False
        
    def handle(self, option):
        raise NotImplementedError("Please implement this method in {self.__class__}")