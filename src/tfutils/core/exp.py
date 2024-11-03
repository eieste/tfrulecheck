
class TFUtilException(Exception):
    pass



class PathIsNotValid(TFUtilException, OSError):
    pass