# __init__.py
# Command Line Interface package
# for the entire Cryptography Toolkit

# Provides the complete terminal-based
# interface for interacting with the toolkit

# Contains interactive menus, command
# registration and execution, argument
# parsing, user prompts, and help systems


# Modules
# menu - Interactive menu system
# parser - Command-line argument parser
# commands - CLI command handlers
# prompts - User input and confirmation prompts
# help - Command-line help and documentation


# Menu System
from .menu import *


# Command Parser
from .parser import *


# Command System
from .commands import *


# User Prompts
from .prompts import *


# Help System
from .help import *


# Public Package API
__all__ = [
    # Menu
    "menu",

    # Parser
    "parser",

    # Commands
    "commands",

    # Prompts
    "prompts",

    # Help
    "help",
] 

