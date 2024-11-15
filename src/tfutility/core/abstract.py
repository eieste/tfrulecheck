# -*- coding: utf-8 -*-

import argparse
import logging

import tfutility


class AbstractCommand:
    """
    An abstract class definition for custom CLI Commands
    """

    def __init__(
        self, parent: "tfutility.main.TfUtility", parser: argparse.ArgumentParser
    ):
        """Serves a abstract class for Commands. Used as Base for every controller

        :param parent: The TfUtility main Class which manages the CLI
        :type parent: TfUtility
        :param parser: The argparser Object
        :type parser: argparse.ArgumentParser
        """
        self._cmd = parent
        self.parser = parser

    def _init(self):
        """
        Intialize an subparser for this command
        normaly it has the name of this command
        """
        raise NotImplementedError("Please Implement an _init method")

    def get_logger(self) -> logging.Logger:
        """
        Get the Logger from the main class

        :return: The logger from the main class
        :rtype: logging.Logger
        """
        return self._cmd.get_logger()

    def add_arguments(self, parser: argparse.ArgumentParser):
        """Attach arguments to parser

        :param parser: The command parser
        :type parser: argparse.ArgumentParser
        :raises NotImplementedError: Triggerd when this method is not ovewritten
        """
        raise NotImplementedError("Please implement an add_arguments method")

    def get_command_name(self):
        """Return the command_name

        :raises NotImplementedError: Triggerd when this method is not ovewritten
        :return: The name of this command
        :rtype: str
        """
        if self.__class__.command_name is None:
            raise NotImplementedError("Please give your Command a name arg ")
        return self.command_name

    def get_help(self):
        if self.__class__.help is None:
            raise NotImplementedError("Please give your Command a help arg")
        return self.help

    def itsme(self, options: argparse.Namespace) -> bool:
        if options.command == self.get_command_name():
            return True
        return False

    def handle(self, option):
        raise NotImplementedError("Please implement this method in {self.__class__}")
