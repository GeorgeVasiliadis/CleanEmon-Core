import argparse
from .dotfiles import store_external_configfile

parser = argparse.ArgumentParser(prog="CleanEmonCore", description="The CLI for CleanEmon-Core")
subparsers = parser.add_subparsers(dest="command", help="commands")

# Register Config File
register_config_parser = subparsers.add_parser("register-config", help="Register the specified configuration file to "
                                                                       "CleanEmon")
register_config_parser.add_argument("config_file", help="path to the config file that will be used")

args = parser.parse_args()

if args.command == "register-config":
    store_external_configfile(args.config_file)
