# -*- coding: utf-8 -*-
import sys

from tfutility.core.base import Command
from tfutility.core.tffile import TfFile
from tfutility.core.tfpaths import TfPaths


class ForcedRemoteSourceHandler(TfPaths, Command):
    command_name = "forcedremotesource"
    help = "Check if a RemoteSource was set"

    def add_arguments(self, parser):
        parser = super().add_arguments(parser)
        parser.add_argument(
            "-s", "--silent", action="store_true", help="Prevent any log output"
        )
        parser.add_argument(
            "--allow-failure",
            action="store_true",
            help="If this flag was set, the module logs only all occurences but does not exit with code 1",
        )
        return parser

    def new_decorator(self, options, block):
        file_path = block.tffile.path
        if not block.id.startswith("module"):
            self.get_logger().error(
                "The decorator @forcedremotesource can only applied to modules"
            )
            sys.exit(1)

        block_content = block.content

        if not block_content.get("version"):
            self._error = True
            self.get_logger().error(
                "Module Block had no Version Defined in {}:{}".format(
                    file_path, block.start
                )
            )

        if block_content.get("source")[0] == ".":
            self._error = True
            self.get_logger().error(
                "Module Block has no Remote Source in {}:{}".format(
                    file_path, block.start
                )
            )

    def handle(self, options):
        self._error = False
        if options.silent:
            self.get_logger().setLevel(1000)

        tf_files = self.get_file_list(options.paths)

        for file in tf_files:
            file = TfFile(file)

            for block in file.get_blocks_with_decorator(self.get_command_name()):
                self.new_decorator(self, block)

        if not options.allow_failure and self._error:
            sys.exit(1)
