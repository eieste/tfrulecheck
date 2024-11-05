import pathlib
import argparse
import hcl2
import logging
import re
from collections import namedtuple
from tfutils.core.abstract import AbstractCommand
from collections.abc import Iterable

# \#\s?\@([a-z]+)(\((.*)\))?

OpendTfFile = namedtuple("OpendTfFile", ("path", "lines", "parsed"))


class TfUtilDecorator:

    PARAM_REGEX = re.compile(r'(\b\w+)(?:=((?:\"[^\"\\]*(?:\\.[^\"\\]*)*\"|\w+)))?')

    def __init__(self, blockref, name, data):
        self._blockref = blockref
        self._name = name
        self._data = data
        self._parameter = None

    def get_parameter(self, key, default=None):
        if self._parameter is None:
            self._parameter = self._parse(self._data)
        return self._parameter.get(key, default)

    def get_name(self):
        return self._name

    def _parse(self, data):
        result = {}
        for regfind in TfUtilDecorator.PARAM_REGEX.findall(data):
            result[regfind[0]] = regfind[1].strip("\"")
        return result


class TfBlock:
    DECORATOR_REGEX = re.compile(r'#\s?\@([a-z]+)(\((.*)\))?',)

    def __init__(self, fileref, id, block_data):
        self._fileref = fileref
        self._id = id
        self._decorators = None
        self._content = block_data
        self._start_line = block_data["__start_line__"]
        self._end_line = block_data["__end_line__"]

    @property
    def start(self):
        return self._start_line

    @property
    def end(self):
        return self._end_line

    def __str__(self):
        return self._id
    
    def __repr__(self):
        return f"<BlockWrapper id={self._id}>"

    @property
    def id(self):
        return self._id

    def get_tf_file(self):
        return self._fileref.get_tf_file()

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
    def content(self):
        return self._content

    def get_decorator(self, name):
        for dec in self.decorators:
            if dec.get_name() == name:
                return dec

    @property
    def decorators(self):
        if self._decorators is None:
            self._decorators = self._find_decorators()
        return self._decorators

    def has_decorator(self, name):
        if self._decorators is None:
            self._decorators = self._find_decorators()
        for dec in self._decorators:
            if dec.get_name() == name:
                return True

    def _find_decorators(self):
        line_nr = self._start_line-2
        decorator_list = []
        while self.get_tf_file().lines[line_nr].strip().startswith("# @"):
            found_decorator = self.get_tf_file().lines[line_nr].strip()
            result = TfBlock.DECORATOR_REGEX.fullmatch(found_decorator)
            decorator_list.append(TfUtilDecorator(self, result.group(1), result.group(2)))
            line_nr =- 1
             
        return decorator_list


class TfFile:

    def __init__(self, path: pathlib.Path, autoparse=True):
        self.path = path
        self._blocks = None
        self._tf_file = self.read_tf(path)
        if autoparse:
            self.parse()

    def get_tf_file(self):
        return self._tf_file

    def read_tf(self, path):
        with path.open("r") as fobj:
            lines = [line.rstrip() for line in fobj]
            fobj.seek(0)
            return OpendTfFile(path, lines, hcl2.load(fobj, with_meta=True))

    @staticmethod
    def _extend_name(previous_name, part):
        return ".".join( [ key for key in  previous_name.split(".") + [part] if key ] )

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

    def _extract_blocks(self, blockdata, name):
        if isinstance(blockdata, dict) and any( [ key.startswith("__") for key in blockdata.keys() ]):

            elem_names = [ key for key in blockdata.keys() if not key.startswith("__")]

            if len(elem_names) > 1:
                new_name = ""
            else:
                new_name = elem_names[0]

            self._blocks.append(TfBlock(self, self._extend_name(name, new_name), blockdata))
        else:

            if isinstance(blockdata, list):
                for blockdata in blockdata:
                    self._extract_blocks(blockdata, name)
            else:
                for key, value in blockdata.items():
                    self._extract_blocks(value, self._extend_name(name, key))

    def get_blocks_with_decorator(self, name):
        result = []
        for block in self.blocks:
            if block.has_decorator(name):
                result.append(block)
        return result
