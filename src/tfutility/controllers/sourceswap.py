# -*- coding: utf-8 -*-
import enum
import re
import sys

from tfutility.core.base import Command
from tfutility.core.tffile import TfFile
from tfutility.core.tfpaths import TfPaths


class SWITCH_DIRECTION(enum.Enum):
    TO_LOCAL = 1
    TO_REMOTE = 2


class SourceSwapHandler(TfPaths, Command):
    command_name = "sourceswap"
    help = "Allows to switch module Sources. Between a Local and Remote Path"

    def add_arguments(self, parser):
        parser = super().add_arguments(parser)
        parser.add_argument(
            "-s",
            "--switch-to",
            type=str,
            choices=["l", "r", "local", "remote"],
            help="Define to which reference all decorated modules should be swapped",
        )
        return parser

    def block_switch_to(self, options, block, dec, switch_to):
        file_path = block.tffile.path
        if not block.id.startswith("module"):
            self.get_logger().error(
                "The decorator @sourceswap applied to wrong blocktype in {}:{}".format(
                    file_path, block.start
                )
            )
            sys.exit(1)

        lines = block.tffile.lines
        source_line = -1
        version_line = -1
        source_indent = ""
        for li in range(block.start, block.end):
            cline = lines[li]

            tf_key = re.match(r"(\s*)(\S*)\s*\=\s*.*", cline)
            if tf_key is None:
                continue

            if tf_key.group(2) == "source":
                source_line = li
                source_indent = tf_key.group(1)
            elif tf_key.group(2) == "version":
                version_line = li

        if switch_to is SWITCH_DIRECTION.TO_REMOTE:
            remote_source = dec.parameter("remote_source")
            remote_version = dec.parameter("remote_version")

            block.tffile.lines[source_line] = re.sub(
                r"source\s*\=\s*\"(.*)\"",
                f'source = "{remote_source}"',
                block.tffile.lines[source_line],
            )

            if version_line == -1:
                block.tffile.lines.insert(
                    source_line, f'{source_indent}version = "{remote_version}"'
                )
            else:
                block.tffile.lines[source_line] = re.sub(
                    r"version\s*\=\s*\"(.*)\"",
                    f'version = "{remote_version}"',
                    block.tffile.lines[source_line],
                )

        else:
            local_source = dec.parameter("local_source")
            block.tffile.lines[source_line] = re.sub(
                r"source\s*\=\s*\"(.*)\"",
                f'source = "{local_source}"',
                block.tffile.lines[source_line],
            )

            if version_line > 0:
                del block.tffile.lines[version_line]

    def get_decorator(self, block):
        file_path = block.tffile.path
        dec = block.get_decorator(self.get_command_name())
        general_error = False
        for param_key in ["remote_source", "remote_version", "local_source"]:
            if not dec.parameter(param_key):
                self.get_logger().error(
                    "Decorator {} {}:{} requires the parameters remote_source, remote_version, local_source".format(
                        self.get_command_name(), file_path, block.start
                    )
                )
                general_error = True

        if general_error:
            sys.exit(1)
        return dec

    def handle(self, options):
        if not options.switch_to:
            self.get_logger().error(
                "Please use --switch-to argument with the keywords local or remote"
            )
            sys.exit(1)

        switch_to = SWITCH_DIRECTION.TO_REMOTE
        if options.switch_to in ["local", "l"]:
            switch_to = SWITCH_DIRECTION.TO_LOCAL

        tf_files = self.get_file_list(options.paths)

        for file in tf_files:
            file = TfFile(file)

            for block in file.get_blocks_with_decorator(self.get_command_name()):
                dec = self.get_decorator(block)
                self.block_switch_to(options, block, dec, switch_to)
            file.write_back()
