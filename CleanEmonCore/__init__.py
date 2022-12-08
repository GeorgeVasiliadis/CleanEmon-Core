import os

from .dotfiles import get_dotfile
from .dotfiles import _CONFIG_FILENAME
from .dotfiles import _DEVICES_FILENAME

PACKAGE_DIR = os.path.dirname(__file__)

# Check if config-file lies in directory of execution
# If not, consider working with the global one
if os.path.exists(_CONFIG_FILENAME):
    CONFIG_FILE = os.path.abspath(_CONFIG_FILENAME)
else:
    # Retrieve the config file from the dot-dir or generate a new one
    CONFIG_FILE = get_dotfile(_CONFIG_FILENAME)

if os.path.exists(_DEVICES_FILENAME):
    DEVICES_FILE = os.path.abspath(_DEVICES_FILENAME)
else:
    # Retrieve the config file from the dot-dir or generate a new one
    DEVICES_FILE = get_dotfile(_DEVICES_FILENAME)
    