import os

_DOT_DIR_NAME = ".CleanEmon"
DOT_DIR_PATH = os.path.expanduser(os.path.join("~", _DOT_DIR_NAME))  # Put dot-dir in user's home dir.


def init_dot_dir():
    """Creates the dot-dir"""
    if not os.path.exists(DOT_DIR_PATH):
        os.makedirs(DOT_DIR_PATH, exist_ok=True)


def get_dotfile(name, fn=None):
    """Searches for the requested file in the dot-directory and returns its absolute path. If file doesn't exist, the
    `fn` hook is invoked.

    name -- a single file, not a full path
    fn   -- this function will be invoked as hook with a single argument, if the requested file does not exist. The
            single argument of fn is the absolute path of the requested file (where the file should live). This hook can
            be used to generate on-demand the missing file
    """
    requested_path = os.path.join(DOT_DIR_PATH, name)

    if not os.path.exists(requested_path):
        if fn:
            fn(requested_path)
        else:
            print(f"Requested dot-file {requested_path} was not found!")

    return requested_path


init_dot_dir()
