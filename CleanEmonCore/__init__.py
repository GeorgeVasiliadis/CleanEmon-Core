import os

from .dotfiles import get_dotfile
from .dotfiles import _CONFIG_FILENAME

PACKAGE_DIR = os.path.dirname(__file__)

# Check if config-file lies in directory of execution
# If not, consider working with the global one
if os.path.exists(_CONFIG_FILENAME):
    CONFIG_FILE = os.path.abspath(_CONFIG_FILENAME)
else:
    # Retrieve the config file from the dot-dir or generate a new one
    from .setup_scripts import generate_config
    CONFIG_FILE = get_dotfile(_CONFIG_FILENAME, generate_config)
