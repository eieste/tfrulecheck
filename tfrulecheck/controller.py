import hcl2
import argparse
from tofudecorator.cli import CommandLine
from tofudecorator.checker import __all__ as all_checkers
import pathlib
import logging

class TofuDecoratorController:

    def __init__(self):
        self.command = CommandLine()
        self.command.init()
        self.options = self.command.handle()
        self.log = logging.getLogger("TFRuleChecker") 
        self._has_errors = False


    def set_error_state(self):
        self._has_errors = True

    def handle(self):
        if not self.options.file.exists():
            raise argparse.ArgumentError("File does not exist")

        with self.options.file.open("r") as file:
            content = file.read()
        
        hcl_data = hcl2.loads(content, True)
        for block_type, block_list in hcl_data.items():
            for checker_cls in all_checkers:
                if checker_cls.should_used(block_type, self.options.only.split(",")):
                    checker = checker_cls(self.options, content)
                    for block_pack in block_list:
                        checker.handle(block_type, block_pack)
        if not self.options.no_fail and self._has_errors:
            exit(1)
            