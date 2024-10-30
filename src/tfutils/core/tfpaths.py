import pathlib
import argparse
import hcl2
import logging
import re


class TFPaths:
    SEARCH_GLOB="**/*.tf"

    def add_arguments(self, parser):
        parser = super(TFPaths, self).add_arguments(parser)
        parser.add_argument("paths", nargs="+", type=pathlib.Path, help="Path to one or more TF-Files. Its also Possible to set a folder. It searches only *.tf files")
        return parser


    def _get_files_from_path(self, path):
        if not path.exists():
            raise ValueError("Path does not exist")
        if path.is_dir():
            return list(path.glob(self.__class__.SEARCH_GLOB))
        return [path]
    
    def get_file_list(self, paths):
        file_list = []
        for p in paths:
            file_list += self._get_files_from_path(p)
        return file_list

    def handle(self, options):
        result = super(TFPaths, self).handle(options)
        result.update({"tf_paths_file_list": self.get_file_list(options.paths)})
        return result