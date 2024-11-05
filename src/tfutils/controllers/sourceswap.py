# -*- coding: utf-8 -*-
import sys

from tfutils.core.base import Command
from tfutils.core.tffile import TfFile
from tfutils.core.tfpaths import TFPaths


class SourceSwapHandler(TFPaths, Command):
    name = "sourceswap"
    help = "Check if a RemoteSource was set"

    def add_arguments(self, parser):
        parser = super().add_arguments(parser)
        parser.add_argument("-s", "--silent", action="store_true", help="Prevent any log output")
        parser.add_argument("--allow-failure", action="store_true", help="If this flag was set, the module logs only all occurences but does not exit with code 1")
        return parser

    def new_decorator(self, options, block):
        file_path = block.get_tf_file().path
        if not block.id.startswith("module"):
            self.get_logger().error("The decorator @forcedremotesource can only applied to modules")
            self.get_logger().debug("Block-Type: {block_type} in file {file} at line {decorator_pos}".format(**block_info, file=file))
            sys.exit(1)

        block_content = block.content

        if not block_content.get("version"):
            self._error = True
            self.get_logger().error("Module Block had no Version Defined")
            self.get_logger().debug(f"Id: {block.id} in file {file_path}")

        if block_content.get("source")[0] == ".":
            self._error = True
            self.get_logger().error("Module Block has no Remote Source")
            self.get_logger().debug(f"Id: {block.id} in file {file_path}")


    def handle(self, options):
        self._error = False
        if options.silent:
            self.get_logger().setLevel(1000)

        result = super(TFDecorator, self).handle(options)

        tf_files = self.get_file_list(options.paths)

        parsed_files = []
        for file in tf_files:
            file = TfFile(file)

            for block in file.get_blocks_with_decorator(self.get_name()):
                self.new_decorator(self, block)

        if not options.allow_failure and self._error:
            sys.exit(1)
