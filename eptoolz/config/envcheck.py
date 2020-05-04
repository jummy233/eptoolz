"""
Health check for EnergyPlus working environment.
"""

import sys
import os
import logging
import importlib
from functools import wraps, reduce
from typing import Callable


def report(name: str):
    def decorator(f: Callable[..., bool]):
        @wraps(f)
        def wrapper(*args, **kwargs):
            res = f(*args, **kwargs)
            if res:
                logging.info(name + " ok ...")
                return res
            msg = "problem occur with: " + name
            raise FileNotFoundError(msg)

        return wrapper
    return decorator


class EnvCheck:
    """
    Check if current system provides all dependencies.
    Checking includes:
        EnergyPlus Version (>=9.3)
        Existance of ConvertInputFormat
        Existance of idd/schema.epJson file
        Existance of pyenergyplus package shiped my native E+
    """

    def __init__(self, envpath: str):
        self.envpath = os.path.abspath(envpath)

    @report("Checking the overall health of the environment ...")
    def check_health(self) -> bool:
        """ Overall health checkig """
        checkmetods = [v(self) for k, v in type(self).__dict__.items()
                       if "check_" in k
                       and callable(v)
                       and k != "check_health"]
        res = reduce(
            lambda a, b: a and b,
            checkmetods,
            True)

        if not res:
            logging.error("Something wrong with your environment. "
                          + "Please check the EnergyPlus install folder")
            return False
        return res

    @report("path to energyplus")
    def check_path(self) -> bool:
        return os.path.exists(self.envpath)

    @report("ConvertInputFormat")
    def check_convertinputformat(self) -> bool:
        convertinputformat = os.path.join(self.envpath, "ConvertInputFormat")
        return os.path.exists(convertinputformat)

    @report("ExpandObjects")
    def check_expandobjects(self) -> bool:
        expandobj = os.path.join(self.envpath, "ExpandObjects")
        return os.path.exists(expandobj)

    @report("idd/epJson")
    def check_idd(self) -> bool:
        # use data set in current dir by default.
        cur = os.path.abspath(os.curdir)
        idd = os.path.join(cur, "Energy+.idd")
        epjson = os.path.join(cur, "Energy+.schema.epJson")
        # fall down to current
        if os.path.exists(idd) or os.path.exists(epjson):
            logging.info("found idd in current directory")
            return True

        logging.info("didn't found idd files in current directory."
                     + " Looking for idd in EnergyPlus Install directory...")
        idd = os.path.join(self.envpath, "Energy+.idd")
        epjson = os.path.join(self.envpath, "Energy+.schema.epJson")
        return os.path.exists(idd) or os.path.exists(epjson)

    @report("pyenergyplus")
    def check_pyenergyplys(self) -> bool:
        pyenergyplus = os.path.join(self.envpath, "pyenergyplus")
        print(pyenergyplus)
        if not (os.path.exists(pyenergyplus) and os.path.isdir(pyenergyplus)):
            logging.error("pyenergyplus module doesn't exists."
                          + " check your EnergyPlus install folder")
            return False
        try:
            # insert E+ installation directory in to PATHPATH
            # so we can import pyenergyplus after wards.
            print(sys.path)
            __import__('subprocess').run(["tree", sys.path[0]])
            import pyenergyplus
        except ImportError:
            logging.error("cannot import pyenergyplus"
                          + "something wrong with the PYTHONPATH\n"
                          + "check if pyenergyplus is in E+ directory?")
            return False
        return True

#     @report("E+ version >= 9.3")
#     def check_version(self):
#         import
