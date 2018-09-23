from os import system as SYS_CALL
from sys import platform as SYSTEM_PLATFORM
from sys import version_info as VERSION_ARRAY
from sys import exit as END_PROCESS

MAJOR_VERSION_INDEX = 0
PYTHON_VERSION = 3

WINDOWS = "win32"
OSX = "darwin"
LINUX = "linux"

WINDOWS_PYTHON = "python"
OSX_PYTHON = "python3"
LINUX_PYTHON = "python3"

GENERIC_PYTHON = ""

thisOperatingSystem = ""

# Size of the following arrays must match
listOfLibraries = ["Flask", "numpy", "SQLAlchemy", "flask-wtf", "flask-login"]
versionsOfLibraries = ["1.0.2", "1.15.1", "1.2.11", "0.14.2"]

# Make sure python3.X is running
if not (VERSION_ARRAY[MAJOR_VERSION_INDEX] == PYTHON_VERSION):
	print("Not running python 3!")
	END_PROCESS()

# Compensate for OS
thisOperatingSystem = SYSTEM_PLATFORM.lower()

if thisOperatingSystem == WINDOWS:
	GENERIC_PYTHON = WINDOWS_PYTHON
	
elif thisOperatingSystem == OSX:
	GENERIC_PYTHON = OSX_PYTHON
	
elif thisOperatingSystem == LINUX:
	GENERIC_PYTHON = LINUX_PYTHON
	
else:
	print("Not on windows or osx!")
	END_PROCESS()
	
# Upgrade pip
SYS_CALL(GENERIC_PYTHON + " -m pip install --upgrade pip")

# Install libraries with correct version
for library, version in zip(listOfLibraries, versionsOfLibraries):
	SYS_CALL(GENERIC_PYTHON + " -m pip install " + library + "==" + version)

print("\nDONE INSTALLING PACKAGES")
