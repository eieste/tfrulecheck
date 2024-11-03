import pathlib
import argparse
import hcl2
import logging
import re
from tfutils.core.abstract import AbstractCommand
from tfutils.core.tfpaths import TFPaths
# \#\s?\@([a-z]+)(\((.*)\))?
  
DECORATOR_REGEX = re.compile(r'#\s?\@([a-z]+)(\((.*)\))?',)


class TFDecorator(TFPaths, AbstractCommand):

    def new_decorator(self, *args, **kwargs):
        raise NotImplementedError("Please implement a new decorator method")

    def parse_block(self, options, file, block_type, block, lines):
            start_line_nr, end_line_nr = self.__class__._get_block_linenr(block)
            line_nr = start_line_nr-2
            param = {}
            while lines[line_nr].strip().startswith("#"):
                found_decorator = lines[line_nr].strip()
                result = DECORATOR_REGEX.fullmatch(found_decorator)

                if result.group(1) == self.get_name():
                    for key, value, *_ in PARAM_REGEX.findall(result.group(0)):
                        param[key.strip().lower()] = value.strip("\"")
                    return {
                        start_line_nr: {
                            "block_type": block_type,
                            "block": block,
                            "start_line_nr": start_line_nr,
                            "end_line_nr": end_line_nr,
                            "decorator_pos": line_nr,
                            "param": param
                        }
                    }
                line_nr = line_nr-1
            return {}

    def handle(self, options):
        result = super(TFDecorator, self).handle(options)
        
        if "tf_parse_file" not in result:
            raise RuntimeError("This TFDecorator requires the TFPath class")
        self.parse_block(options, **result["tf_parse_file"])
        return result