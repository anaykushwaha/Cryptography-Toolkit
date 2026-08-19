# parser.py

# Command-line argument parsing utilities for the
# Cryptography Toolkit

# Provides command definitions, argument validation,
# parser construction, and parsed argument handling


from __future__ import annotations

import argparse

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    Any,
    Sequence,
)


# Parser Exceptions


class ParserError(Exception):
    # Base exception for CLI parser errors

    pass


class InvalidCommandError(ParserError):
    # Raised when an unknown command is supplied

    pass


class InvalidArgumentError(ParserError):
    # Raised when an argument is invalid

    pass


class MissingArgumentError(ParserError):
    # Raised when a required argument is missing

    pass


# Parsed Command Model


@dataclass
class ParsedCommand:
    # Stores a parsed CLI command

    command: str
    arguments: dict[str, Any] = field(
        default_factory=dict
    )
    options: dict[str, Any] = field(
        default_factory=dict
    )

    def get(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        # Returns an argument or option

        if name in self.arguments:
            return self.arguments[name]

        return self.options.get(
            name,
            default,
        )

    def has(
        self,
        name: str,
    ) -> bool:
        # Checks whether a value exists

        return (
            name in self.arguments
            or name in self.options
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        # Converts the parsed command to a dictionary

        return {
            "command": self.command,
            "arguments": dict(
                self.arguments
            ),
            "options": dict(
                self.options
            ),
        }


# Command Definition


@dataclass
class CommandDefinition:
    # Defines a CLI command

    name: str
    description: str
    aliases: list[str] = field(
        default_factory=list
    )
    arguments: list[dict[str, Any]] = field(
        default_factory=list
    )
    options: list[dict[str, Any]] = field(
        default_factory=list
    )

    def all_names(
        self,
    ) -> list[str]:
        # Returns the command name and aliases

        return [
            self.name,
            *self.aliases,
        ]


# Parser Configuration


PROGRAM_NAME = "caesar-toolkit"

PROGRAM_DESCRIPTION = (
    "Cryptography Toolkit for Caesar "
    "Cipher encryption, decryption, "
    "analysis, and cryptanalysis."
)

PROGRAM_VERSION = "1.0.0"


# Command Names


COMMAND_ENCRYPT = "encrypt"
COMMAND_DECRYPT = "decrypt"
COMMAND_ANALYZE = "analyze"
COMMAND_BRUTE_FORCE = "bruteforce"
COMMAND_FREQUENCY = "frequency"
COMMAND_ENTROPY = "entropy"
COMMAND_IOC = "ioc"
COMMAND_NGRAMS = "ngrams"
COMMAND_HISTORY = "history"
COMMAND_EXPORT = "export"
COMMAND_BACKUP = "backup"
COMMAND_VERSION = "version"


SUPPORTED_COMMANDS = [
    COMMAND_ENCRYPT,
    COMMAND_DECRYPT,
    COMMAND_ANALYZE,
    COMMAND_BRUTE_FORCE,
    COMMAND_FREQUENCY,
    COMMAND_ENTROPY,
    COMMAND_IOC,
    COMMAND_NGRAMS,
    COMMAND_HISTORY,
    COMMAND_EXPORT,
    COMMAND_BACKUP,
    COMMAND_VERSION,
]


# Parser Helpers


def normalize_command(
    command: str,
) -> str:
    # Normalizes a command name

    if not isinstance(
        command,
        str,
    ):
        raise InvalidCommandError(
            "Command must be a string."
        )

    normalized = (
        command.strip()
        .lower()
        .replace(
            "_",
            "-",
        )
    )

    if not normalized:
        raise InvalidCommandError(
            "Command cannot be empty."
        )

    return normalized


def is_valid_command(
    command: str,
) -> bool:
    # Checks whether a command is supported

    try:
        normalized = normalize_command(
            command
        )

    except InvalidCommandError:
        return False

    return normalized in SUPPORTED_COMMANDS


def validate_command(
    command: str,
) -> str:
    # Validates and returns a normalized command

    normalized = normalize_command(
        command
    )

    if normalized not in SUPPORTED_COMMANDS:
        raise InvalidCommandError(
            f"Unknown command: {command}"
        )

    return normalized


# Argument Conversion


def convert_argument(
    value: Any,
    argument_type: type | None = None,
) -> Any:
    # Converts a parser value to the requested type

    if argument_type is None:
        return value

    if value is None:
        return None

    try:
        return argument_type(
            value
        )

    except (
        TypeError,
        ValueError,
    ) as error:
        raise InvalidArgumentError(
            f"Unable to convert argument "
            f"value: {value}"
        ) from error


def positive_integer(
    value: str,
) -> int:
    # Converts a value into a positive integer

    try:
        number = int(
            value
        )

    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "Value must be an integer."
        ) from error

    if number < 1:
        raise argparse.ArgumentTypeError(
            "Value must be greater than zero."
        )

    return number


def non_negative_integer(
    value: str,
) -> int:
    # Converts a value into a non-negative integer

    try:
        number = int(
            value
        )

    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "Value must be an integer."
        ) from error

    if number < 0:
        raise argparse.ArgumentTypeError(
            "Value cannot be negative."
        )

    return number


# Parser Construction


class ToolkitParser:
    # Main command-line parser for the toolkit

    def __init__(
        self,
        *,
        program_name: str = PROGRAM_NAME,
        description: str = PROGRAM_DESCRIPTION,
        version: str = PROGRAM_VERSION,
    ) -> None:
        # Initializes the parser

        self.program_name = program_name
        self.description = description
        self.version = version

        self.parser = self._create_parser()

        self.subparsers = (
            self.parser.add_subparsers(
                dest="command"
            )
        )

        self._register_commands()

    # Base Parser

    def _create_parser(
        self,
    ) -> argparse.ArgumentParser:
        # Creates the root argument parser

        return argparse.ArgumentParser(
            prog=self.program_name,
            description=self.description,
            formatter_class=(
                argparse.ArgumentDefaultsHelpFormatter
            ),
        )

    # Command Registration

    def _register_commands(
        self,
    ) -> None:
        # Registers all supported commands

        self._register_encrypt()
        self._register_decrypt()
        self._register_analyze()
        self._register_bruteforce()
        self._register_frequency()
        self._register_entropy()
        self._register_ioc()
        self._register_ngrams()
        self._register_history()
        self._register_export()
        self._register_backup()
        self._register_version()

    # Encryption Command

    def _register_encrypt(
        self,
    ) -> None:
        # Registers the encrypt command

        parser = self.subparsers.add_parser(
            COMMAND_ENCRYPT,
            aliases=["enc"],
            help="Encrypt text or a file.",
        )

        parser.add_argument(
            "input",
            help="Input text or input file.",
        )

        parser.add_argument(
            "-k",
            "--key",
            type=int,
            required=True,
            help="Caesar cipher shift.",
        )

        parser.add_argument(
            "-o",
            "--output",
            help="Output file.",
        )

        parser.add_argument(
            "-a",
            "--alphabet",
            help="Alphabet to use.",
        )

        parser.add_argument(
            "--preserve-case",
            action="store_true",
            help="Preserve character casing.",
        )

        parser.add_argument(
            "--preserve-nonalpha",
            action="store_true",
            help=(
                "Preserve non-alphabetic characters."
            ),
        )

    # Decryption Command

    def _register_decrypt(
        self,
    ) -> None:
        # Registers the decrypt command

        parser = self.subparsers.add_parser(
            COMMAND_DECRYPT,
            aliases=["dec"],
            help="Decrypt text or a file.",
        )

        parser.add_argument(
            "input",
            help="Encrypted text or input file.",
        )

        parser.add_argument(
            "-k",
            "--key",
            type=int,
            required=True,
            help="Caesar cipher shift.",
        )

        parser.add_argument(
            "-o",
            "--output",
            help="Output file.",
        )

        parser.add_argument(
            "-a",
            "--alphabet",
            help="Alphabet to use.",
        )

        parser.add_argument(
            "--preserve-case",
            action="store_true",
            help="Preserve character casing.",
        )

        parser.add_argument(
            "--preserve-nonalpha",
            action="store_true",
            help=(
                "Preserve non-alphabetic characters."
            ),
        )

    # Analysis Command

    def _register_analyze(
        self,
    ) -> None:
        # Registers the general analyze command

        parser = self.subparsers.add_parser(
            COMMAND_ANALYZE,
            aliases=["analysis"],
            help="Analyze encrypted or plain text.",
        )

        parser.add_argument(
            "input",
            help="Input text or input file.",
        )

        parser.add_argument(
            "-o",
            "--output",
            help="Optional output file.",
        )

        parser.add_argument(
            "--frequency",
            action="store_true",
            help="Run frequency analysis.",
        )

        parser.add_argument(
            "--entropy",
            action="store_true",
            help="Calculate Shannon entropy.",
        )

        parser.add_argument(
            "--ioc",
            action="store_true",
            help="Calculate Index of Coincidence.",
        )

        parser.add_argument(
            "--ngrams",
            action="store_true",
            help="Run n-gram analysis.",
        )

    # Brute Force Command

    def _register_bruteforce(
        self,
    ) -> None:
        # Registers the brute-force command

        parser = self.subparsers.add_parser(
            COMMAND_BRUTE_FORCE,
            aliases=["brute", "crack"],
            help="Brute-force a Caesar cipher.",
        )

        parser.add_argument(
            "input",
            help="Encrypted text or input file.",
        )

        parser.add_argument(
            "--min-key",
            type=int,
            default=0,
            help="Minimum key to test.",
        )

        parser.add_argument(
            "--max-key",
            type=int,
            default=25,
            help="Maximum key to test.",
        )

        parser.add_argument(
            "-n",
            "--top",
            type=positive_integer,
            default=5,
            help="Number of candidates to display.",
        )

        parser.add_argument(
            "-o",
            "--output",
            help="Optional output file.",
        )

        parser.add_argument(
            "--show-all",
            action="store_true",
            help="Show every tested candidate.",
        )

        # Frequency Command

    def _register_frequency(
        self,
    ) -> None:
        # Registers the frequency analysis command

        parser = self.subparsers.add_parser(
            COMMAND_FREQUENCY,
            aliases=["freq"],
            help="Analyze character frequencies.",
        )

        parser.add_argument(
            "input",
            help="Input text or input file.",
        )

        parser.add_argument(
            "-n",
            "--top",
            type=positive_integer,
            default=10,
            help="Number of results to display.",
        )

        parser.add_argument(
            "--letters-only",
            action="store_true",
            help="Analyze alphabetic characters only.",
        )

        parser.add_argument(
            "--case-sensitive",
            action="store_true",
            help="Treat uppercase and lowercase separately.",
        )

        parser.add_argument(
            "-o",
            "--output",
            help="Optional output file.",
        )

    # Entropy Command

    def _register_entropy(
        self,
    ) -> None:
        # Registers the entropy analysis command

        parser = self.subparsers.add_parser(
            COMMAND_ENTROPY,
            aliases=["ent"],
            help="Calculate Shannon entropy.",
        )

        parser.add_argument(
            "input",
            help="Input text or input file.",
        )

        parser.add_argument(
            "--base",
            type=positive_integer,
            default=2,
            help="Logarithm base for entropy calculation.",
        )

        parser.add_argument(
            "--normalized",
            action="store_true",
            help="Display normalized entropy.",
        )

        parser.add_argument(
            "-o",
            "--output",
            help="Optional output file.",
        )

    # Index of Coincidence Command

    def _register_ioc(
        self,
    ) -> None:
        # Registers the Index of Coincidence command

        parser = self.subparsers.add_parser(
            COMMAND_IOC,
            aliases=["index"],
            help="Calculate Index of Coincidence.",
        )

        parser.add_argument(
            "input",
            help="Input text or input file.",
        )

        parser.add_argument(
            "--letters-only",
            action="store_true",
            help="Use alphabetic characters only.",
        )

        parser.add_argument(
            "--case-sensitive",
            action="store_true",
            help="Treat uppercase and lowercase separately.",
        )

        parser.add_argument(
            "-o",
            "--output",
            help="Optional output file.",
        )

    # N-Gram Command

    def _register_ngrams(
        self,
    ) -> None:
        # Registers the n-gram analysis command

        parser = self.subparsers.add_parser(
            COMMAND_NGRAMS,
            aliases=["ngram"],
            help="Analyze repeated n-grams.",
        )

        parser.add_argument(
            "input",
            help="Input text or input file.",
        )

        parser.add_argument(
            "-n",
            type=positive_integer,
            default=2,
            help="N-gram size.",
        )

        parser.add_argument(
            "--top",
            type=positive_integer,
            default=20,
            help="Number of n-grams to display.",
        )

        parser.add_argument(
            "--overlapping",
            action="store_true",
            default=True,
            help="Include overlapping n-grams.",
        )

        parser.add_argument(
            "-o",
            "--output",
            help="Optional output file.",
        )

    # History Command

    def _register_history(
        self,
    ) -> None:
        # Registers the history command

        parser = self.subparsers.add_parser(
            COMMAND_HISTORY,
            aliases=["hist"],
            help="Manage operation history.",
        )

        history_subparsers = (
            parser.add_subparsers(
                dest="history_action"
            )
        )

        history_subparsers.add_parser(
            "list",
            help="List recorded operations.",
        )

        history_subparsers.add_parser(
            "latest",
            help="Show the latest operation.",
        )

        history_subparsers.add_parser(
            "clear",
            help="Clear operation history.",
        )

        search_parser = history_subparsers.add_parser(
            "search",
            help="Search operation history.",
        )

        search_parser.add_argument(
            "query",
            help="Search query.",
        )

        history_subparsers.add_parser(
            "summary",
            help="Show history statistics.",
        )

        export_parser = history_subparsers.add_parser(
            "export",
            help="Export operation history.",
        )

        export_parser.add_argument(
            "output",
            help="Destination file.",
        )

        export_parser.add_argument(
            "--format",
            dest="format_name",
            choices=[
                "txt",
                "json",
                "csv",
            ],
            help="Export format.",
        )

    # Export Command

    def _register_export(
        self,
    ) -> None:
        # Registers the export command

        parser = self.subparsers.add_parser(
            COMMAND_EXPORT,
            aliases=["save"],
            help="Export toolkit data.",
        )

        parser.add_argument(
            "input",
            help="Input file containing data.",
        )

        parser.add_argument(
            "output",
            help="Destination output file.",
        )

        parser.add_argument(
            "--format",
            dest="format_name",
            choices=[
                "txt",
                "json",
                "csv",
            ],
            help="Export format.",
        )

        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Allow overwriting an existing file.",
        )

    # Backup Command

    def _register_backup(
        self,
    ) -> None:
        # Registers the backup command

        parser = self.subparsers.add_parser(
            COMMAND_BACKUP,
            aliases=["backups"],
            help="Manage file backups.",
        )

        backup_subparsers = (
            parser.add_subparsers(
                dest="backup_action"
            )
        )

        create_parser = backup_subparsers.add_parser(
            "create",
            help="Create a file backup.",
        )

        create_parser.add_argument(
            "source",
            help="File to back up.",
        )

        create_parser.add_argument(
            "--name",
            help="Backup name.",
        )

        create_parser.add_argument(
            "--description",
            default="",
            help="Backup description.",
        )

        create_parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite an existing backup.",
        )

        restore_parser = backup_subparsers.add_parser(
            "restore",
            help="Restore a backup.",
        )

        restore_parser.add_argument(
            "name",
            help="Backup name.",
        )

        restore_parser.add_argument(
            "destination",
            help="Restore destination.",
        )

        restore_parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite the destination file.",
        )

        delete_parser = backup_subparsers.add_parser(
            "delete",
            help="Delete a backup.",
        )

        delete_parser.add_argument(
            "name",
            help="Backup name.",
        )

        backup_subparsers.add_parser(
            "list",
            help="List available backups.",
        )

        backup_subparsers.add_parser(
            "summary",
            help="Show backup statistics.",
        )

    # Version Command

    def _register_version(
        self,
    ) -> None:
        # Registers the version command

        self.subparsers.add_parser(
            COMMAND_VERSION,
            aliases=["v"],
            help="Display toolkit version.",
        )

    # Parsing


    def parse(
        self,
        args: Sequence[str] | None = None,
    ) -> ParsedCommand:
        # Parses command-line arguments

        namespace = self.parser.parse_args(
            args
        )

        data = vars(
            namespace
        )

        command = data.pop(
            "command",
            None,
        )

        if command is None:
            raise MissingArgumentError(
                "A command is required."
            )

        command = normalize_command(
            command
        )

        if command not in SUPPORTED_COMMANDS:
            raise InvalidCommandError(
                f"Unknown command: {command}"
            )

        arguments: dict[str, Any] = {}
        options: dict[str, Any] = {}

        positional_names = {
            "input",
            "output",
            "source",
            "destination",
            "name",
            "query",
            "history_action",
            "backup_action",
        }

        for key, value in data.items():
            if key in positional_names:
                arguments[key] = value
            else:
                options[key] = value

        return ParsedCommand(
            command=command,
            arguments=arguments,
            options=options,
        )

    def parse_known(
        self,
        args: Sequence[str] | None = None,
    ) -> tuple[
        ParsedCommand,
        list[str],
    ]:
        # Parses known arguments while preserving
        # arguments that are not recognized

        namespace, unknown = (
            self.parser.parse_known_args(
                args
            )
        )

        data = vars(
            namespace
        )

        command = data.pop(
            "command",
            None,
        )

        if command is None:
            raise MissingArgumentError(
                "A command is required."
            )

        command = normalize_command(
            command
        )

        arguments: dict[str, Any] = {}
        options: dict[str, Any] = {}

        positional_names = {
            "input",
            "output",
            "source",
            "destination",
            "name",
            "query",
            "history_action",
            "backup_action",
        }

        for key, value in data.items():
            if key in positional_names:
                arguments[key] = value
            else:
                options[key] = value

        return (
            ParsedCommand(
                command=command,
                arguments=arguments,
                options=options,
            ),
            unknown,
        )

    # Namespace Parsing


    def parse_namespace(
        self,
        namespace: argparse.Namespace,
    ) -> ParsedCommand:
        # Converts an argparse Namespace into
        # a ParsedCommand object

        if not isinstance(
            namespace,
            argparse.Namespace,
        ):
            raise TypeError(
                "namespace must be an argparse.Namespace."
            )

        data = vars(
            namespace
        ).copy()

        command = data.pop(
            "command",
            None,
        )

        if command is None:
            raise MissingArgumentError(
                "A command is required."
            )

        command = normalize_command(
            command
        )

        arguments: dict[str, Any] = {}
        options: dict[str, Any] = {}

        positional_names = {
            "input",
            "output",
            "source",
            "destination",
            "name",
            "query",
            "history_action",
            "backup_action",
        }

        for key, value in data.items():
            if key in positional_names:
                arguments[key] = value
            else:
                options[key] = value

        return ParsedCommand(
            command=command,
            arguments=arguments,
            options=options,
        )

    # Parser Information


    def get_parser(
        self,
    ) -> argparse.ArgumentParser:
        # Returns the underlying argparse parser

        return self.parser

    def print_help(
        self,
    ) -> None:
        # Displays the root parser help

        self.parser.print_help()

    def format_help(
        self,
    ) -> str:
        # Returns formatted parser help text

        return self.parser.format_help()

    def command_help(
        self,
        command: str,
    ) -> str:
        # Returns help text for a specific command

        normalized = validate_command(
            command
        )

        for action in self.subparsers.choices.values():
            if action.prog.endswith(
                normalized
            ):
                return action.format_help()

        raise InvalidCommandError(
            f"Unable to find command: {command}"
        )

        # Command Information

    def commands(
        self,
    ) -> list[str]:
        # Returns all registered command names

        return list(
            SUPPORTED_COMMANDS
        )

    def has_command(
        self,
        command: str,
    ) -> bool:
        # Checks whether a command is registered

        try:
            normalized = normalize_command(
                command
            )
        except InvalidCommandError:
            return False

        return normalized in SUPPORTED_COMMANDS

    def aliases(
        self,
        command: str,
    ) -> list[str]:
        # Returns aliases for a command

        normalized = validate_command(
            command
        )

        alias_map = {
            COMMAND_ENCRYPT: ["enc"],
            COMMAND_DECRYPT: ["dec"],
            COMMAND_ANALYZE: ["analysis"],
            COMMAND_BRUTE_FORCE: [
                "brute",
                "crack",
            ],
            COMMAND_FREQUENCY: ["freq"],
            COMMAND_ENTROPY: ["ent"],
            COMMAND_IOC: ["index"],
            COMMAND_NGRAMS: ["ngram"],
            COMMAND_HISTORY: ["hist"],
            COMMAND_EXPORT: ["save"],
            COMMAND_BACKUP: ["backups"],
            COMMAND_VERSION: ["v"],
        }

        return list(
            alias_map.get(
                normalized,
                [],
            )
        )

    # Argument Validation

    @staticmethod
    def validate_key(
        key: int,
    ) -> int:
        # Validates a Caesar cipher key

        if not isinstance(
            key,
            int,
        ):
            raise InvalidArgumentError(
                "Key must be an integer."
            )

        return key

    @staticmethod
    def validate_key_range(
        minimum: int,
        maximum: int,
    ) -> tuple[int, int]:
        # Validates a brute-force key range

        if not isinstance(
            minimum,
            int,
        ):
            raise InvalidArgumentError(
                "Minimum key must be an integer."
            )

        if not isinstance(
            maximum,
            int,
        ):
            raise InvalidArgumentError(
                "Maximum key must be an integer."
            )

        if minimum > maximum:
            raise InvalidArgumentError(
                "Minimum key cannot exceed maximum key."
            )

        return (
            minimum,
            maximum,
        )

    @staticmethod
    def validate_input(
        value: str,
    ) -> str:
        # Validates a CLI input value

        if not isinstance(
            value,
            str,
        ):
            raise InvalidArgumentError(
                "Input must be a string."
            )

        if not value.strip():
            raise InvalidArgumentError(
                "Input cannot be empty."
            )

        return value

    # Parsed Command Validation

    def validate_parsed(
        self,
        parsed: ParsedCommand,
    ) -> ParsedCommand:
        # Performs additional validation on a
        # ParsedCommand object

        if not isinstance(
            parsed,
            ParsedCommand,
        ):
            raise TypeError(
                "parsed must be a ParsedCommand."
            )

        command = validate_command(
            parsed.command
        )

        if command in {
            COMMAND_ENCRYPT,
            COMMAND_DECRYPT,
        }:
            input_value = parsed.get(
                "input"
            )

            if input_value is None:
                raise MissingArgumentError(
                    "Input is required."
                )

            self.validate_input(
                input_value
            )

            key = parsed.get(
                "key"
            )

            if key is None:
                raise MissingArgumentError(
                    "A key is required."
                )

            self.validate_key(
                key
            )

        elif command in {
            COMMAND_ANALYZE,
            COMMAND_BRUTE_FORCE,
            COMMAND_FREQUENCY,
            COMMAND_ENTROPY,
            COMMAND_IOC,
            COMMAND_NGRAMS,
        }:
            input_value = parsed.get(
                "input"
            )

            if input_value is None:
                raise MissingArgumentError(
                    "Input is required."
                )

            self.validate_input(
                input_value
            )

        if command == COMMAND_BRUTE_FORCE:
            minimum = parsed.get(
                "min_key",
                0,
            )

            maximum = parsed.get(
                "max_key",
                25,
            )

            self.validate_key_range(
                minimum,
                maximum,
            )

        return parsed

    # Parsing Convenience

    def parse_and_validate(
        self,
        args: Sequence[str] | None = None,
    ) -> ParsedCommand:
        # Parses and validates CLI arguments

        parsed = self.parse(
            args
        )

        return self.validate_parsed(
            parsed
        )


# Default Parser


_default_parser = ToolkitParser()


def get_parser() -> ToolkitParser:
    # Returns the default toolkit parser

    return _default_parser


# Convenience Functions


def parse_args(
    args: Sequence[str] | None = None,
) -> ParsedCommand:
    # Parses command-line arguments using
    # the default parser

    return _default_parser.parse(
        args
    )


def parse_and_validate(
    args: Sequence[str] | None = None,
) -> ParsedCommand:
    # Parses and validates command-line arguments

    return _default_parser.parse_and_validate(
        args
    )


def is_command(
    command: str,
) -> bool:
    # Checks whether a command is supported

    return is_valid_command(
        command
    )


def get_commands() -> list[str]:
    # Returns all supported commands

    return _default_parser.commands()


def get_aliases(
    command: str,
) -> list[str]:
    # Returns aliases for a command

    return _default_parser.aliases(
        command
    )


def show_help() -> None:
    # Displays general CLI help

    _default_parser.print_help()


def get_help() -> str:
    # Returns general CLI help text

    return _default_parser.format_help()


def get_command_help(
    command: str,
) -> str:
    # Returns help text for a specific command

    return _default_parser.command_help(
        command
    )


# Parser Self-Test


def self_test() -> bool:
    # Runs basic parser verification tests

    parser = ToolkitParser()

    try:
        # Test encryption parsing

        encrypted = parser.parse_and_validate(
            [
                "encrypt",
                "hello",
                "--key",
                "3",
            ]
        )

        if encrypted.command != COMMAND_ENCRYPT:
            return False

        if encrypted.get(
            "input"
        ) != "hello":
            return False

        if encrypted.get(
            "key"
        ) != 3:
            return False

        # Test decryption parsing

        decrypted = parser.parse_and_validate(
            [
                "decrypt",
                "khoor",
                "-k",
                "3",
            ]
        )

        if decrypted.command != COMMAND_DECRYPT:
            return False

        # Test frequency parsing

        frequency = parser.parse_and_validate(
            [
                "frequency",
                "message.txt",
                "--top",
                "5",
            ]
        )

        if frequency.command != COMMAND_FREQUENCY:
            return False

        if frequency.get(
            "top"
        ) != 5:
            return False

        # Test brute-force parsing

        brute_force = parser.parse_and_validate(
            [
                "bruteforce",
                "encrypted.txt",
                "--min-key",
                "1",
                "--max-key",
                "10",
            ]
        )

        if brute_force.command != COMMAND_BRUTE_FORCE:
            return False

        if brute_force.get(
            "min_key"
        ) != 1:
            return False

        if brute_force.get(
            "max_key"
        ) != 10:
            return False

        # Test aliases

        if not parser.has_command(
            "enc"
        ):
            return False

        if not parser.has_command(
            "brute"
        ):
            return False

        # Test invalid command

        if parser.has_command(
            "invalid-command"
        ):
            return False

        return True

    except (
        ParserError,
        argparse.ArgumentError,
        ValueError,
        TypeError,
    ):
        return False


# Module Exports


__all__ = [
    # Exceptions
    "ParserError",
    "InvalidCommandError",
    "InvalidArgumentError",
    "MissingArgumentError",

    # Data Models
    "ParsedCommand",
    "CommandDefinition",

    # Configuration
    "PROGRAM_NAME",
    "PROGRAM_DESCRIPTION",
    "PROGRAM_VERSION",
    "SUPPORTED_COMMANDS",

    # Command Constants
    "COMMAND_ENCRYPT",
    "COMMAND_DECRYPT",
    "COMMAND_ANALYZE",
    "COMMAND_BRUTE_FORCE",
    "COMMAND_FREQUENCY",
    "COMMAND_ENTROPY",
    "COMMAND_IOC",
    "COMMAND_NGRAMS",
    "COMMAND_HISTORY",
    "COMMAND_EXPORT",
    "COMMAND_BACKUP",
    "COMMAND_VERSION",

    # Helpers
    "normalize_command",
    "is_valid_command",
    "validate_command",
    "convert_argument",
    "positive_integer",
    "non_negative_integer",

    # Parser
    "ToolkitParser",
    "get_parser",

    # Convenience Functions
    "parse_args",
    "parse_and_validate",
    "is_command",
    "get_commands",
    "get_aliases",
    "show_help",
    "get_help",
    "get_command_help",

    # Testing
    "self_test",
]

