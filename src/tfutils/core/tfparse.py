import pathlib
import argparse
import hcl2
import logging
import re

# \#\s?\@([a-z]+)(\((.*)\))?
  
DECORATOR_REGEX = re.compile(r'#\s?\@([a-z]+)(\((.*)\))?',)
PARAM_REGEX = re.compile(r'(\b\w+)(?:=((?:\"[^\"\\]*(?:\\.[^\"\\]*)*\"|\w+)))?')


class TFParse:
    
    @staticmethod
    def _get_block_linenr(block) -> tuple:
         if "__start_line__" in block and "__end_line__" in block:
              return block.get("__start_line__"), block.get("__end_line__")
         else:
            return TFParse._get_block_linenr(list(block.values())[0])

    def parse_block(self, options, file, block_type, block, lines):
        start_line_nr, end_line_nr = self.__class__._get_block_linenr(block)
        line_nr = start_line_nr-2
        param = {}
        while lines[line_nr].strip().startswith("#"):
            found_decorator = lines[line_nr].strip()
            result = DECORATOR_REGEX.fullmatch(found_decorator)

            # if result.group(1) == self.get_name():
            #     for key, value, *_ in PARAM_REGEX.findall(result.group(0)):
            #         param[key.strip().lower()] = value.strip("\"")
            #     return {
            #         start_line_nr: {
            #             "block_type": block_type,
            #             "block": block,
            #             "start_line_nr": start_line_nr,
            #             "end_line_nr": end_line_nr,
            #             "decorator_pos": line_nr,
            #             "param": param
            #         }
            #     }
            line_nr = line_nr-1
        return {}

    def handle_file(self, options, result, file):
        with file.open("r+") as fobj:
            lines = [line.rstrip() for line in fobj]
            fobj.seek(0)
            file_data = hcl2.load(fobj, with_meta=True)

        all_occurences = {}
        for block_type, blocks in file_data.items():
            for block in blocks:
                all_occurences.update(self.parse_block(options, file, block_type, block, lines))
        
        
    def handle_files(self, options, result):
        for file in result["tf_paths_file_list"]:
            self.handle_file(options, result, file)

    def handle(self, options):
        result = super(TFParse, self).handle(options)
        
        if "tf_paths_file_list" not in result:
            raise RuntimeError("This TFParse requires the TFPath class")

        self.handle_files(options, result)

        return result