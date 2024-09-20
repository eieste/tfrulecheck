import enum
import re
import logging


class HclBlock(enum.Enum):
    ALL = "all"
    MODULE = "module"
    RESOURCE = "resource"


class BaseChecker:
    
    def __init__(self, options, content, controller):
        self.options = options
        self.content = content
        self.ctrl = controller
        self.log = logging.getLogger("{}.checker[{}]".format(self.ctrl.log.name, self.get_checker_id()))

    @classmethod
    def get_name(cls):
        return cls.name

    @classmethod
    def get_name_regex(cls):
        return re.compile(".*@{}$".format(cls.get_name()))

    @classmethod
    def get_checker_id(cls):
        return cls.checker_id

    @classmethod
    def get_applied_to(cls):
        return cls.applied_to
    
    @classmethod
    def should_used(cls, block_name, only) -> bool:
        if cls.get_checker_id() in only or "all" in only and \
            HclBlock(block_name) in cls.get_applied_to() or HclBlock.ALL in cls.get_applied_to():
                return True
        return False

    @staticmethod
    def _get_block_linenr(block) -> tuple:
         if "__start_line__" in block and "__end_line__" in block:
              return block.get("__start_line__"), block.get("__end_line__")
         else:
            return BaseChecker._get_block_linenr(list(block.values())[0])

    def match_decorator(self, block) -> bool:
        top_line = self.get_line_above(block)
        if self.get_name_regex().match(top_line):
            return True
        return False
    
    def get_line_above(self, block) -> str:
        start, end = self.__class__._get_block_linenr(block)
        lines = self.content.split("\n")
        return lines[start-2]

    def handle(self, block_type, block):
        raise NotImplementedError("Please Implement this Method")
    