# -*- coding: utf-8 -*-
class TFUtilException(Exception):
    pass


class PathIsNotValid(TFUtilException, OSError):
    pass
