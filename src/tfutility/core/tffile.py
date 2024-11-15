# -*- coding: utf-8 -*-
import pathlib
import re
from collections import namedtuple

import hcl2

from tfutility.contrib.deprecation import deprecated

OpendTfFile = namedtuple("OpendTfFile", ("path", "lines", "parsed"))


class TfUtilityDecorator:
    """
    Represents a tfutility decorator used in tf files above blocks
    """

    # Parses key="value", parameters ( used inside the decorator braces )
    PARAM_REGEX = re.compile(r"(\b\w+)(?:=((?:\"[^\"\\]*(?:\\.[^\"\\]*)*\"|\w+)))?")

    def __init__(self, blockref, name: str, data):
        """Initializes a Decorator of an TfBlock

        :param blockref: Reference to the TfBlock which is decorated
        :type blockref: TfBlock
        :param name: Name of the Decorator ( the word after the @ sign )
        :type name: str
        :param data: Content form inside the braces of the Decorator
        :type data: str
        """
        self._blockref = blockref
        self._name = name
        self._data = data
        self._parameter = None

    def parameter(self, key: str, default=None):
        """
        Returns the value of a given parameter or the default value if the parameter is not set

        :param key: The name of the parameter
        :param default: The default value to return if the parameter is not set
        :return: The value of the parameter or the default value if the parameter is not set
        """
        if self._parameter is None:
            self._parameter = self._parse(self._data)
        return self._parameter.get(key, default)

    @deprecated
    def get_name(self):
        return self._name

    @property
    def name(self):
        return self._name

    def _parse(self, data: str):
        """
        Parses the given data string and returns a dictionary of key-value pairs

        :param data: The data string to parse
        :return: A dictionary of key-value pairs
        """
        result = {}
        for regfind in TfUtilityDecorator.PARAM_REGEX.findall(data):
            result[regfind[0]] = regfind[1].strip('"')
        return result


class TfBlock:
    """
    Represents a block in a terraform file
    """

    # Parses an tfutility decorator inside terraform files
    DECORATOR_REGEX = re.compile(
        r"#\s?\@([a-z]+)(\((.*)\))?",
    )

    def __init__(self, fileref, id: str, block_data: dict):
        """
        Initializes a new instance of the TfBlock class

        :param fileref: The reference to TfFile which contains this block
        :param id: The id of the block. usaly tfblocktype.blocktype.blockname
        :param block_data: The data of the block as parsed by hcl2
        """
        self._fileref = fileref
        self._id = id
        self._decorators = None
        self._content = block_data
        self._start_line = block_data["__start_line__"]
        self._end_line = block_data["__end_line__"]

    @property
    def start(self):
        """
        Start linenumber of the block

        :return: The start linenumber of the block
        :rtype: int
        """
        return self._start_line

    @property
    def end(self):
        """
        End linenumber of the block

        :return: The end linenumber of the block
        :rtype: int
        """
        return self._end_line

    def __str__(self):
        return self._id

    def __repr__(self):
        return f"<BlockWrapper id={self._id}>"

    def __eq__(self, value: object) -> bool:
        self._start_line == value._start_line

    def __lt__(self, other):
        return self.start < other.start

    def __le__(self, other):
        return self.start >= other.start

    def __ne__(self, other):
        return self.start != other.start

    def __gt__(self, other):
        return self.start > other.start

    def __ge__(self, other):
        return self.start >= other.start

    @property
    def id(self):
        """
        id of the block. usually tfblocktype.blocktype.blockname

        :return: The id of the block
        :rtype: str
        """
        return self._id

    @deprecated
    def get_tfile(self):
        return self._fileref.tffile

    @property
    def tffile(self):
        return self._fileref.tffile

    @property
    def content(self):
        return self._content

    def get_decorator(self, name: str) -> TfUtilityDecorator | None:
        """
        find a decorator with the given name above the current block

        :param name: The name of the decorator to find
        :type name: str
        :return: The decorator with the given name or None if not found
        :rtype: TfUtilDecorator
        """
        for dec in self.decorators:
            if dec.name == name:
                return dec

    @property
    def decorators(self):
        if self._decorators is None:
            self._decorators = self._find_decorators()
        return self._decorators

    def has_decorator(self, name: str) -> bool:
        """
        Check if this block has a decorator with the given name

        :param name: The name of the decorator to check for
        :type name: str
        :return: True if the block has a decorator with the given name, False otherwise
        :rtype: bool
        """
        if self._decorators is None:
            self._decorators = self._find_decorators()
        for dec in self._decorators:
            if dec.name == name:
                return True
        return False

    def _find_decorators(self):
        """
        search in the file for decorators above this block

        :return: A list of decorators found above this block
        :rtype: list[TfUtilDecorator]
        """
        line_nr = self._start_line - 2
        decorator_list = []
        while self.tffile.lines[line_nr].strip().startswith("# @"):
            found_decorator = self.tffile.lines[line_nr].strip()
            result = TfBlock.DECORATOR_REGEX.fullmatch(found_decorator)
            decorator_list.append(
                TfUtilityDecorator(self, result.group(1), result.group(2))
            )
            line_nr = -1

        return decorator_list


class TfFile:
    def __init__(self, path: pathlib.Path, autoparse=True):
        self.path = path
        self._blocks = None
        self._tf_file = self.read_tf(path)
        if autoparse:
            self.parse()

    def __repr__(self):
        return f"<TfFile path={self.path.absolute()} >"

    @property
    def tffile(self):
        return self._tf_file

    @deprecated
    def get_tffile(self):
        return self._tf_file

    def read_tf(self, path: pathlib.Path):
        with path.open("r") as fobj:
            lines = [line.rstrip() for line in fobj]
            fobj.seek(0)
            return OpendTfFile(path, lines, hcl2.load(fobj, with_meta=True))

    @staticmethod
    def _extend_name(previous_name: str, part: str):
        return ".".join([key for key in previous_name.split(".") + [part] if key])

    @property
    def blocks(self):
        if self._blocks is None:
            self.parse()
        return self._blocks

    def parse(self):
        self._blocks = []
        for block_type, blocks in self._tf_file.parsed.items():
            for block in blocks:
                self._extract_blocks(block, block_type)

    def _extract_blocks(self, blockdata: dict, name: str):
        if isinstance(blockdata, dict) and any(
            [key.startswith("__") for key in blockdata.keys()]
        ):
            elem_names = [key for key in blockdata.keys() if not key.startswith("__")]

            if len(elem_names) > 1:
                new_name = ""
            else:
                new_name = elem_names[0]

            self._blocks.append(
                TfBlock(self, self._extend_name(name, new_name), blockdata)
            )
        else:
            if isinstance(blockdata, list):
                for blockdata in blockdata:
                    self._extract_blocks(blockdata, name)
            else:
                for key, value in blockdata.items():
                    self._extract_blocks(value, self._extend_name(name, key))

    def get_blocks_with_decorator(self, name: str):
        result = []
        for block in self.blocks:
            if block.has_decorator(name):
                result.append(block)
        return result

    def write_back(self):
        with self.path.open("r+") as fobj:
            fobj.truncate()
            for line in self.tffile.lines:
                fobj.write(f"{line}\n")
