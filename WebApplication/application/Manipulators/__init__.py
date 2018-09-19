from application.CommonDefinitions.CommonPaths import PATH_TO_MANIPULATORS
import glob
import os

__all__ =  [os.path.basename(f).replace(".py","") for f in glob.glob(PATH_TO_MANIPULATORS + "/" + "*Manipulator.py")]
