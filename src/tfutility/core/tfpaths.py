# -*- coding: utf-8 -*-
import argparse
import pathlib

from tfutility.core.abstract import AbstractCommand
from tfutility.core.exp import PathIsNotValid


class TfPaths(AbstractCommand):
    """Add an CLI argument to the command to Found .tf files"""

    SEARCH_GLOB = "**/*.tf"

    def add_arguments(self, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """Add argument that consumes multiple filesystem paths.

        :param parser: A ArgumentParser object. if it is None the default one (for the whole application) will be used.
        :type parser: argparse.ArgumentParser
        :return: Tthe argument parser enriched with arguments
        :rtype: argparse.ArgumentParser
        """
        parser = super(TfPaths, self).add_arguments(parser)
        parser.add_argument(
            "paths",
            nargs="+",
            type=pathlib.Path,
            help="Path to one or more TF-Files. Its also Possible to set a folder. It searches only *.tf files",
        )
        return parser

    def _get_files_from_path(self, path: pathlib.Path):
        """Resolves a given Path to a list of all matched files in it

        :param path: Path Object of target folder or file on the filesystem
        :type path: pathlib.Path
        :raises PathIsNotValid: when the Path does not exist
        :return: list
        :rtype: list[pathlib.Path]
        """
        if not path.exists():
            raise PathIsNotValid("Path does not exist")
        if path.is_dir():
            return list(path.glob(self.__class__.SEARCH_GLOB))
        return [path]

    def get_file_list(self, paths: pathlib.Path) -> list[pathlib.Path]:
        """Resolve all given cli nargs. If a given path has no file matching it logs a warning

        :param paths: list[pathlib.Path]
        :type paths: pathlib.Path
        :return: List of all found Files
        :rtype: list[pathlib.Path]
        """
        file_list = []
        for p in paths:
            file_list += self._get_files_from_path(p)

        if len(file_list) <= 0:
            self.get_logger().warning(
                "The Search-Methoud found Zero files that can be used by tfutility "
            )
        return file_list
