from tfutils.core.base import Command
from tfutils.core.tfdecorator import TFDecorator
from tfutils.core.tfpaths import TFPaths
from tfutils.core.tffile import TfFile
import sys


class BlockDateHandler(TFDecorator, TFPaths, Command):
    block_name = None
    name = None
    help = None # "Check if a import-blocks has a date comment"

    def add_arguments(self, parser):
        parser = super().add_arguments(parser)
        parser.add_argument("-s", "--silent", action="store_true", help="Prevent any log output")
        parser.add_argument("--allow-failure", action="store_true", help="If this flag was set, the module logs only all occurences but does not exit with code 1")
        return parser

    def get_block_name(self):
        if self.block_name is None:
            raise RuntimeError("Please define block_name")
        return self.block_name

    def new_block(self, options, block):
        file_path = block.get_tf_file().path
        block_content = block.content

        dec = block.get_decorator(self.get_name())
        
        if dec is None:
            self._error = True
            self.get_logger().error(f"{self.get_block_name()} Block has no date decorator")
            self.get_logger().debug(f"Id: {block.id} in file {file_path} linenr: {block.start}")
        else:
            print("CHECK if expired")


    def handle(self, options):
        self._error = False
        results = super(BlockDateHandler, self).handle(options)

        if not options.allow_failure and self._error:
            sys.exit(1)

        tf_files = self.get_file_list(options.paths)

        parsed_files = []
        for file in tf_files:
            file = TfFile(file)

            for block in file.get_blocks_with_decorator(self.get_name()):
                if not block.id.startswith(self.get_block_name()):
                    self.new_block(self, block)

        return results


class ImportDateHandler(BlockDateHandler):
    block_name = "import"
    name = "importdate"
    help = "Check if a import-blocks has a date comment"



class MovedDateHandler(BlockDateHandler):
    block_name = "moved"
    name = "moveddate"
    help = "Check if a moved-blocks has a date comment"
