from tfutils.core.argparse import Command
from tfutils.core.tfdecorator import TFDecorator
from tfutils.core.tfpaths import TFPaths
import sys


class RemoteSourceHandler(TFDecorator, TFPaths, Command):
    name = "forcedremotesource"
    help = "Check if a RemoteSource was set"

    def add_arguments(self, parser):
        parser = super().add_arguments(parser)
        parser.add_argument("--allow-failure", action="store_true", help="If this flag was set, the module logs only all occurences but does not exit with code 1")
        return parser

    def handle(self, options):
        self._error = False
        results = super(RemoteSourceHandler, self).handle(options)

        if not options.allow_failure and self._error:
            sys.exit(1)

        return results
    

    def new_decorator(self, options, file, block_info):
        if block_info.get("block_type") != "module":
            self.get_logger().error("The decorator @forcedremotesource can only applied to modules") 
            self.get_logger().debug("Block-Type: {block_type} in file {file} at line {decorator_pos}".format(**block_info, file=file))
            sys.exit(1)

        block = block_info.get("block",{})

        module_block = list(block.values())[0]

        if not module_block.get("version"):
            self._error = True
            self.get_logger().error("Module Block had no Version Defined")
            self.get_logger().debug("Block-Type: {block_type} in file {file} at line {decorator_pos}".format(**block_info, file=file))

        if module_block.get("source")[0] == ".":
            self._error = True
            self.get_logger().error("Module Block has no Remote Source")
            self.get_logger().debug("Block-Type: {block_type} in file {file} at line {decorator_pos}".format(**block_info, file=file))
