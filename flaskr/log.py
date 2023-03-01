import logging
import logging.handlers
from os.path import abspath, dirname, join


def _log(logfn=__file__, levelname="DEBUG", take_path=__file__, add_folder="", logfilesize=1, **kwargs):
    log = logging.getLogger(logfn)

    _take_path = dirname(abspath(take_path))
    if add_folder:
        add_folder = add_folder.strip('/') if '/' in add_folder else add_folder
        add_folder = add_folder.strip('\\') if '\\' in add_folder else add_folder
        _take_path = join(_take_path, add_folder)

    _LOGFILENAME = "%s.log" % logfn if logfn else "log"
    _LOG = join(_take_path, _LOGFILENAME)

    _LOGFILESZ = 1024 * 1024 * logfilesize  # 1mb

    level = logging.getLevelName(levelname)
    fmt = kwargs.get('fmt', '%(asctime)s %(levelname)-9s %(message)s')
    formatter = logging.Formatter(fmt)

    handler = logging.FileHandler(_LOG, encoding='UTF-8')
    handler.suffix = "__%Y-%m-%d"

    handler.setLevel(level)
    handler.setFormatter(formatter)

    log.addHandler(handler)  # add handler

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    log.addHandler(handler)  # add handler

    return log


log = _log(
    "parking_service",
    "DEBUG",
    take_path=__file__,
    add_folder='logs',
    logfilesize=20,
    fmt='%(asctime)s %(levelname)-10s %(funcName)-30s %(message)s'
)
