# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta

from tfutility.core.base import Command
from tfutility.core.tffile import TfFile
from tfutility.core.tfpaths import TFPaths


class BlockDateHandler(TFPaths, Command):
    block_name = None
    name = None
    help = None  # "Check if a import-blocks has a date comment"

    def add_arguments(self, parser):
        parser = super().add_arguments(parser)

        parser.add_argument(
            "--expire-after",
            type=int,
            help="Returns all blocks that are older than the specified time period. The time span in days",
        )
        parser.add_argument(
            "-s", "--silent", action="store_true", help="Prevent any log output"
        )
        parser.add_argument(
            "--allow-failure",
            action="store_true",
            help="If this flag was set, the module logs only all occurences but does not exit with code 1",
        )
        return parser

    def get_block_name(self):
        if self.block_name is None:
            raise RuntimeError("Please define block_name")
        return self.block_name

    def new_block(self, options, block):
        file_path = block.tffile.path

        dec = block.get_decorator(self.get_name())

        if dec is None:
            self._error = True
            self.get_logger().error(
                f"Missing moveddate Decorator at block '{self.get_block_name()}' in file {file_path} Line {block.start}"
            )
        else:
            now = datetime.now()
            dec_date_create = datetime.strptime(dec.get_parameter("create"), "%d-%m-%Y")

            if not options.expire_after:
                if dec.get_parameter("expire"):
                    dec_date_expire = datetime.strptime(
                        dec.get_parameter("expire"), "%d-%m-%Y"
                    )
                    if now > dec_date_expire:
                        self._error = True
                        self.get_logger().error(
                            f"Moved Block expired in file: {file_path} Line {block.start}"
                        )
            else:
                if now > dec_date_create + timedelta(days=options.expire_after):
                    self._error = True
                    self.get_logger().error(
                        f"Moved Block expired in file: {file_path} Line {block.start}"
                    )

    def handle(self, options):
        self._error = False
        results = super(BlockDateHandler, self).handle(options)

        if not options.allow_failure and self._error:
            sys.exit(1)

        tf_files = self.get_file_list(options.paths)

        for file in tf_files:
            file = TfFile(file)

            for block in file.blocks:
                if block.id.startswith(self.get_block_name()):
                    self.new_block(options, block)

        return results


class ImportDateHandler(BlockDateHandler):
    block_name = "import"
    name = "importdate"
    help = "Check if a import-blocks has a date comment"


class MovedDateHandler(BlockDateHandler):
    block_name = "moved"
    name = "moveddate"
    help = "Check if a moved-blocks has a date comment"
