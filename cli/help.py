# help.py

# Help and documentation utilities for the
# Cryptography Toolkit CLI

# Provides command descriptions, usage information,
# examples, command-specific help, and formatted
# help output for the command-line interface


from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    Any,
    Iterable,
    Sequence,
)


# Help Exceptions


class HelpError(Exception):
    # Base exception for CLI help errors

    pass


class UnknownHelpTopicError(HelpError):
    # Raised when an unknown help topic is requested

    pass


class HelpFormattingError(HelpError):
    # Raised when help content cannot be formatted

    pass


# Help Models


@dataclass
class HelpExample:
    # Represents a CLI usage example

    command: str
    description: str
    output: str | None = None

    def format(
        self,
        *,
        include_output: bool = False,
    ) -> str:
        # Formats the example for display

        lines = [
            f"$ {self.command}",
            f"  {self.description}",
        ]

        if (
            include_output
            and self.output is not None
        ):
            lines.extend(
                [
                    "",
                    "Output:",
                    self.output,
                ]
            )

        return "\n".join(
            lines
        )


@dataclass
class HelpTopic:
    # Represents a help topic

    name: str
    title: str
    description: str
    usage: str | None = None
    examples: list[HelpExample] = field(
        default_factory=list
    )
    notes: list[str] = field(
        default_factory=list
    )
    related: list[str] = field(
        default_factory=list
    )

    def add_example(
        self,
        example: HelpExample,
    ) -> None:
        # Adds an example to the topic

        if not isinstance(
            example,
            HelpExample,
        ):
            raise TypeError(
                "example must be a HelpExample."
            )

        self.examples.append(
            example
        )

    def add_note(
        self,
        note: str,
    ) -> None:
        # Adds a note to the topic

        if not isinstance(
            note,
            str,
        ):
            raise TypeError(
                "note must be a string."
            )

        if note.strip():
            self.notes.append(
                note.strip()
            )


# Help Constants


TOOLKIT_NAME = "Caesar Cipher Toolkit"

TOOLKIT_COMMAND = "caesar-toolkit"

TOOLKIT_VERSION = "1.0.0"


HELP_WIDTH = 78


HELP_TOPICS = (
    "overview",
    "encrypt",
    "decrypt",
    "analyze",
    "bruteforce",
    "frequency",
    "entropy",
    "ioc",
    "ngrams",
    "history",
    "export",
    "backup",
    "examples",
)


# General Help Text


OVERVIEW_DESCRIPTION = (
    "A command-line cryptography toolkit for "
    "Caesar Cipher encryption, decryption, "
    "cryptanalysis, file operations, and "
    "statistical analysis."
)


GENERAL_USAGE = (
    f"{TOOLKIT_COMMAND} <command> [options]"
)


# Command Descriptions


COMMAND_DESCRIPTIONS = {
    "encrypt": (
        "Encrypt plaintext using a Caesar Cipher."
    ),
    "decrypt": (
        "Decrypt ciphertext using a Caesar Cipher."
    ),
    "analyze": (
        "Run one or more cryptanalysis operations "
        "against text or a file."
    ),
    "bruteforce": (
        "Test possible Caesar Cipher keys and "
        "rank the resulting plaintext candidates."
    ),
    "frequency": (
        "Analyze character frequency distributions "
        "within text."
    ),
    "entropy": (
        "Calculate the Shannon entropy of text."
    ),
    "ioc": (
        "Calculate the Index of Coincidence."
    ),
    "ngrams": (
        "Analyze repeated bigrams, trigrams, or "
        "other n-grams."
    ),
    "history": (
        "View and manage previous toolkit operations."
    ),
    "export": (
        "Export analysis or toolkit data to a file."
    ),
    "backup": (
        "Create, restore, list, and manage file backups."
    ),
    "version": (
        "Display the current toolkit version."
    ),
}


# Command Usage


COMMAND_USAGE = {
    "encrypt": (
        f"{TOOLKIT_COMMAND} encrypt "
        "<input> --key <key> [options]"
    ),
    "decrypt": (
        f"{TOOLKIT_COMMAND} decrypt "
        "<input> --key <key> [options]"
    ),
    "analyze": (
        f"{TOOLKIT_COMMAND} analyze "
        "<input> [options]"
    ),
    "bruteforce": (
        f"{TOOLKIT_COMMAND} bruteforce "
        "<input> [options]"
    ),
    "frequency": (
        f"{TOOLKIT_COMMAND} frequency "
        "<input> [options]"
    ),
    "entropy": (
        f"{TOOLKIT_COMMAND} entropy "
        "<input> [options]"
    ),
    "ioc": (
        f"{TOOLKIT_COMMAND} ioc "
        "<input> [options]"
    ),
    "ngrams": (
        f"{TOOLKIT_COMMAND} ngrams "
        "<input> [options]"
    ),
    "history": (
        f"{TOOLKIT_COMMAND} history "
        "<action> [options]"
    ),
    "export": (
        f"{TOOLKIT_COMMAND} export "
        "<input> <output> [options]"
    ),
    "backup": (
        f"{TOOLKIT_COMMAND} backup "
        "<action> [options]"
    ),
    "version": (
        f"{TOOLKIT_COMMAND} version"
    ),
}


# Command Options


COMMAND_OPTIONS = {
    "encrypt": [
        (
            "-k, --key <key>",
            "Caesar Cipher shift value.",
        ),
        (
            "-o, --output <file>",
            "Write encrypted output to a file.",
        ),
        (
            "-a, --alphabet <name>",
            "Select an alphabet.",
        ),
        (
            "--preserve-case",
            "Preserve uppercase and lowercase characters.",
        ),
        (
            "--preserve-nonalpha",
            "Preserve non-alphabetic characters.",
        ),
    ],
    "decrypt": [
        (
            "-k, --key <key>",
            "Caesar Cipher shift value.",
        ),
        (
            "-o, --output <file>",
            "Write decrypted output to a file.",
        ),
        (
            "-a, --alphabet <name>",
            "Select an alphabet.",
        ),
        (
            "--preserve-case",
            "Preserve uppercase and lowercase characters.",
        ),
        (
            "--preserve-nonalpha",
            "Preserve non-alphabetic characters.",
        ),
    ],
    "analyze": [
        (
            "--frequency",
            "Run frequency analysis.",
        ),
        (
            "--entropy",
            "Calculate Shannon entropy.",
        ),
        (
            "--ioc",
            "Calculate Index of Coincidence.",
        ),
        (
            "--ngrams",
            "Run n-gram analysis.",
        ),
        (
            "-o, --output <file>",
            "Write the analysis results to a file.",
        ),
    ],
    "bruteforce": [
        (
            "--min-key <key>",
            "Minimum key to test.",
        ),
        (
            "--max-key <key>",
            "Maximum key to test.",
        ),
        (
            "-n, --top <number>",
            "Number of candidates to display.",
        ),
        (
            "-o, --output <file>",
            "Write results to a file.",
        ),
        (
            "--show-all",
            "Display every tested candidate.",
        ),
    ],
    "frequency": [
        (
            "-n, --top <number>",
            "Number of frequency results.",
        ),
        (
            "--letters-only",
            "Analyze alphabetic characters only.",
        ),
        (
            "--case-sensitive",
            "Treat uppercase and lowercase separately.",
        ),
        (
            "-o, --output <file>",
            "Write results to a file.",
        ),
    ],
    "entropy": [
        (
            "--base <number>",
            "Logarithm base used for entropy.",
        ),
        (
            "--normalized",
            "Display normalized entropy.",
        ),
        (
            "-o, --output <file>",
            "Write results to a file.",
        ),
    ],
    "ioc": [
        (
            "--letters-only",
            "Use alphabetic characters only.",
        ),
        (
            "--case-sensitive",
            "Treat uppercase and lowercase separately.",
        ),
        (
            "-o, --output <file>",
            "Write results to a file.",
        ),
    ],
    "ngrams": [
        (
            "-n <number>",
            "Size of the n-grams.",
        ),
        (
            "--top <number>",
            "Number of n-grams to display.",
        ),
        (
            "--overlapping",
            "Include overlapping n-grams.",
        ),
        (
            "-o, --output <file>",
            "Write results to a file.",
        ),
    ],
    "history": [
        (
            "list",
            "List recorded operations.",
        ),
        (
            "latest",
            "Display the latest operation.",
        ),
        (
            "clear",
            "Clear operation history.",
        ),
        (
            "search <query>",
            "Search operation history.",
        ),
        (
            "summary",
            "Display history statistics.",
        ),
        (
            "export <file>",
            "Export operation history.",
        ),
    ],
    "export": [
        (
            "--format <format>",
            "Export as txt, json, or csv.",
        ),
        (
            "--overwrite",
            "Allow overwriting an existing file.",
        ),
    ],
    "backup": [
        (
            "create <source>",
            "Create a backup of a file.",
        ),
        (
            "restore <name> <destination>",
            "Restore a backup.",
        ),
        (
            "delete <name>",
            "Delete a backup.",
        ),
        (
            "list",
            "List available backups.",
        ),
        (
            "summary",
            "Display backup statistics.",
        ),
    ],
}


# Command Examples


COMMAND_EXAMPLES = {
    "encrypt": [
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} encrypt "
                "\"Hello World\" --key 3"
            ),
            description=(
                "Encrypt a text string using a "
                "shift of 3."
            ),
        ),
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} encrypt "
                "message.txt --key 7 "
                "--output encrypted.txt"
            ),
            description=(
                "Encrypt the contents of a file."
            ),
        ),
    ],
    "decrypt": [
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} decrypt "
                "\"Khoor Zruog\" --key 3"
            ),
            description=(
                "Decrypt a Caesar-encrypted message."
            ),
        ),
    ],
    "analyze": [
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} analyze "
                "encrypted.txt "
                "--frequency --entropy --ioc"
            ),
            description=(
                "Run several analysis operations."
            ),
        ),
    ],
    "bruteforce": [
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} bruteforce "
                "encrypted.txt"
            ),
            description=(
                "Try all standard Caesar Cipher keys."
            ),
        ),
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} bruteforce "
                "encrypted.txt "
                "--min-key 1 --max-key 10 --top 3"
            ),
            description=(
                "Test a specific key range."
            ),
        ),
    ],
    "frequency": [
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} frequency "
                "message.txt --top 10"
            ),
            description=(
                "Display the ten most common characters."
            ),
        ),
    ],
    "entropy": [
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} entropy "
                "\"Hello World\""
            ),
            description=(
                "Calculate the entropy of a text string."
            ),
        ),
    ],
    "ioc": [
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} ioc "
                "encrypted.txt"
            ),
            description=(
                "Calculate the Index of Coincidence."
            ),
        ),
    ],
    "ngrams": [
        HelpExample(
            command=(
                f"{TOOLKIT_COMMAND} ngrams "
                "message.txt -n 3 --top 20"
            ),
            description=(
                "Find common trigrams in a message."
            ),
        ),
    ],
}


# Help Manager


class HelpManager:
    # Manages CLI help topics and formatting

    def __init__(
        self,
        *,
        width: int = HELP_WIDTH,
    ) -> None:
        # Initializes the help manager

        if not isinstance(
            width,
            int,
        ):
            raise TypeError(
                "width must be an integer."
            )

        if width < 40:
            raise ValueError(
                "width must be at least 40."
            )

        self.width = width

        self.topics: dict[
            str,
            HelpTopic,
        ] = {}

        self._register_default_topics()

    # Topic Registration

    def register_topic(
        self,
        topic: HelpTopic,
    ) -> None:
        # Registers a custom help topic

        if not isinstance(
            topic,
            HelpTopic,
        ):
            raise TypeError(
                "topic must be a HelpTopic."
            )

        name = topic.name.strip().lower()

        if not name:
            raise ValueError(
                "Help topic name cannot be empty."
            )

        self.topics[name] = topic

    def has_topic(
        self,
        name: str,
    ) -> bool:
        # Checks whether a topic exists

        if not isinstance(
            name,
            str,
        ):
            return False

        return (
            name.strip().lower()
            in self.topics
        )

    def get_topic(
        self,
        name: str,
    ) -> HelpTopic:
        # Retrieves a help topic

        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "Help topic name must be a string."
            )

        normalized = (
            name.strip().lower()
        )

        if normalized not in self.topics:
            raise UnknownHelpTopicError(
                f"Unknown help topic: {name}"
            )

        return self.topics[
            normalized
        ]

    # Default Topics

    def _register_default_topics(
        self,
    ) -> None:
        # Registers the built-in help topics

        self.register_topic(
            HelpTopic(
                name="overview",
                title=TOOLKIT_NAME,
                description=OVERVIEW_DESCRIPTION,
                usage=GENERAL_USAGE,
                notes=[
                    (
                        "Use --help after a command to "
                        "view command-specific information."
                    ),
                    (
                        "Use 'version' to display the "
                        "current toolkit version."
                    ),
                ],
                related=[
                    "encrypt",
                    "decrypt",
                    "analyze",
                ],
            )
        )

        for command, description in (
            COMMAND_DESCRIPTIONS.items()
        ):
            self.register_topic(
                HelpTopic(
                    name=command,
                    title=(
                        f"{command.title()} Command"
                    ),
                    description=description,
                    usage=COMMAND_USAGE.get(
                        command
                    ),
                    examples=list(
                        COMMAND_EXAMPLES.get(
                            command,
                            [],
                        )
                    ),
                )
            )

        self.register_topic(
            HelpTopic(
                name="examples",
                title="Command Examples",
                description=(
                    "Common examples showing how "
                    "to use the toolkit."
                ),
                examples=[
                    HelpExample(
                        command=(
                            f"{TOOLKIT_COMMAND} "
                            "encrypt \"Hello\" --key 3"
                        ),
                        description=(
                            "Encrypt a message."
                        ),
                    ),
                    HelpExample(
                        command=(
                            f"{TOOLKIT_COMMAND} "
                            "decrypt \"Khoor\" --key 3"
                        ),
                        description=(
                            "Decrypt a message."
                        ),
                    ),
                    HelpExample(
                        command=(
                            f"{TOOLKIT_COMMAND} "
                            "bruteforce encrypted.txt"
                        ),
                        description=(
                            "Attempt automatic cracking."
                        ),
                    ),
                    HelpExample(
                        command=(
                            f"{TOOLKIT_COMMAND} "
                            "frequency message.txt"
                        ),
                        description=(
                            "Analyze character frequencies."
                        ),
                    ),
                ],
            )
        )

    # Topic Listing

    def list_topics(
        self,
    ) -> list[str]:
        # Returns all registered topic names

        return sorted(
            self.topics.keys()
        )

    def command_topics(
        self,
    ) -> list[str]:
        # Returns topics corresponding to commands

        return [
            topic
            for topic in self.list_topics()
            if topic in COMMAND_DESCRIPTIONS
        ]

        # Formatting Helpers

    def _separator(
        self,
        character: str = "=",
    ) -> str:
        # Creates a horizontal separator

        if not character:
            character = "="

        return character * self.width

    def _heading(
        self,
        text: str,
        *,
        character: str = "=",
    ) -> str:
        # Formats a section heading

        if not isinstance(
            text,
            str,
        ):
            raise TypeError(
                "text must be a string."
            )

        return (
            f"{text}\n"
            f"{self._separator(character)}"
        )

    def _wrap(
        self,
        text: str,
        *,
        indent: int = 0,
    ) -> list[str]:
        # Wraps text to the configured help width

        import textwrap

        if not isinstance(
            text,
            str,
        ):
            raise TypeError(
                "text must be a string."
            )

        prefix = " " * max(
            0,
            indent,
        )

        return textwrap.wrap(
            text,
            width=max(
                1,
                self.width - len(prefix),
            ),
            initial_indent=prefix,
            subsequent_indent=prefix,
        )

    def _format_option(
        self,
        option: str,
        description: str,
    ) -> str:
        # Formats a command option

        if not isinstance(
            option,
            str,
        ):
            raise TypeError(
                "option must be a string."
            )

        if not isinstance(
            description,
            str,
        ):
            raise TypeError(
                "description must be a string."
            )

        return (
            f"  {option:<30}"
            f"{description}"
        )

    # Topic Formatting

    def format_topic(
        self,
        name: str,
        *,
        include_examples: bool = True,
        include_options: bool = True,
        include_related: bool = True,
    ) -> str:
        # Formats a complete help topic

        topic = self.get_topic(
            name
        )

        lines: list[str] = []

        lines.append(
            self._heading(
                topic.title
            )
        )

        lines.append("")

        lines.extend(
            self._wrap(
                topic.description
            )
        )

        if topic.usage:
            lines.extend(
                [
                    "",
                    "Usage:",
                    f"  {topic.usage}",
                ]
            )

        options = COMMAND_OPTIONS.get(
            topic.name,
            [],
        )

        if (
            include_options
            and options
        ):
            lines.extend(
                [
                    "",
                    "Options:",
                ]
            )

            for option, description in options:
                lines.append(
                    self._format_option(
                        option,
                        description,
                    )
                )

        if (
            include_examples
            and topic.examples
        ):
            lines.extend(
                [
                    "",
                    "Examples:",
                ]
            )

            for index, example in enumerate(
                topic.examples,
                start=1,
            ):
                lines.append(
                    f"  {index}. "
                    f"{example.description}"
                )
                lines.append(
                    f"     $ {example.command}"
                )

                if example.output:
                    lines.append(
                        "     Output:"
                    )

                    for output_line in (
                        example.output.splitlines()
                    ):
                        lines.append(
                            f"       {output_line}"
                        )

        if topic.notes:
            lines.extend(
                [
                    "",
                    "Notes:",
                ]
            )

            for note in topic.notes:
                wrapped = self._wrap(
                    f"- {note}",
                    indent=2,
                )

                lines.extend(
                    wrapped
                )

        if (
            include_related
            and topic.related
        ):
            lines.extend(
                [
                    "",
                    "Related:",
                    "  "
                    + ", ".join(
                        topic.related
                    ),
                ]
            )

        return "\n".join(
            lines
        )

    # Overview Formatting

    def format_overview(
        self,
    ) -> str:
        # Formats the main toolkit overview

        lines = [
            self._heading(
                TOOLKIT_NAME
            ),
            "",
            OVERVIEW_DESCRIPTION,
            "",
            "Usage:",
            f"  {GENERAL_USAGE}",
            "",
            "Commands:",
        ]

        for command in (
            "encrypt",
            "decrypt",
            "analyze",
            "bruteforce",
            "frequency",
            "entropy",
            "ioc",
            "ngrams",
            "history",
            "export",
            "backup",
            "version",
        ):
            description = (
                COMMAND_DESCRIPTIONS.get(
                    command,
                    "",
                )
            )

            lines.append(
                f"  {command:<15}"
                f"{description}"
            )

        lines.extend(
            [
                "",
                "Global Options:",
                "  -h, --help      "
                "Show this help message.",
                "  --version       "
                "Show the toolkit version.",
                "",
                "Examples:",
                (
                    f"  {TOOLKIT_COMMAND} "
                    "encrypt \"Hello\" --key 3"
                ),
                (
                    f"  {TOOLKIT_COMMAND} "
                    "decrypt \"Khoor\" --key 3"
                ),
                (
                    f"  {TOOLKIT_COMMAND} "
                    "bruteforce encrypted.txt"
                ),
                (
                    f"  {TOOLKIT_COMMAND} "
                    "frequency message.txt"
                ),
            ]
        )

        return "\n".join(
            lines
        )

    # Command Summary

    def format_command_summary(
        self,
    ) -> str:
        # Formats a compact command summary

        lines = [
            self._heading(
                "Available Commands"
            ),
            "",
        ]

        for command in (
            "encrypt",
            "decrypt",
            "analyze",
            "bruteforce",
            "frequency",
            "entropy",
            "ioc",
            "ngrams",
            "history",
            "export",
            "backup",
            "version",
        ):
            description = (
                COMMAND_DESCRIPTIONS[
                    command
                ]
            )

            lines.append(
                f"{command:<15}"
                f"{description}"
            )

        return "\n".join(
            lines
        )

    # Examples Formatting

    def format_examples(
        self,
        *,
        command: str | None = None,
    ) -> str:
        # Formats examples for either a specific
        # command or the entire toolkit

        if command is not None:
            topic = self.get_topic(
                command
            )

            examples = topic.examples

            title = (
                f"{topic.title} Examples"
            )

        else:
            examples = []

            for topic_name in (
                self.command_topics()
            ):
                topic = self.get_topic(
                    topic_name
                )

                examples.extend(
                    topic.examples
                )

            title = "Command Examples"

        lines = [
            self._heading(
                title
            ),
            "",
        ]

        if not examples:
            lines.append(
                "No examples available."
            )

            return "\n".join(
                lines
            )

        for index, example in enumerate(
            examples,
            start=1,
        ):
            lines.append(
                f"{index}. "
                f"{example.description}"
            )
            lines.append(
                f"   $ {example.command}"
            )

            if example.output:
                lines.append(
                    "   Output:"
                )

                for output_line in (
                    example.output.splitlines()
                ):
                    lines.append(
                        f"     {output_line}"
                    )

            lines.append("")

        return "\n".join(
            lines
        ).rstrip()

    # Option Formatting

    def format_options(
        self,
        command: str,
    ) -> str:
        # Formats options for a specific command

        normalized = (
            command.strip().lower()
        )

        if normalized not in COMMAND_OPTIONS:
            raise UnknownHelpTopicError(
                f"No options available for: "
                f"{command}"
            )

        options = COMMAND_OPTIONS[
            normalized
        ]

        lines = [
            self._heading(
                f"{normalized.title()} Options"
            ),
            "",
        ]

        if not options:
            lines.append(
                "No command-specific options."
            )

            return "\n".join(
                lines
            )

        for option, description in options:
            lines.append(
                self._format_option(
                    option,
                    description,
                )
            )

        return "\n".join(
            lines
        )

    # Usage Formatting

    def format_usage(
        self,
        command: str | None = None,
    ) -> str:
        # Formats general or command-specific usage

        if command is None:
            return (
                "Usage:\n"
                f"  {GENERAL_USAGE}"
            )

        normalized = (
            command.strip().lower()
        )

        usage = COMMAND_USAGE.get(
            normalized
        )

        if usage is None:
            raise UnknownHelpTopicError(
                f"Unknown command: {command}"
            )

        return (
            f"Usage:\n"
            f"  {usage}"
        )

    # Search Help

    def search(
        self,
        query: str,
    ) -> list[HelpTopic]:
        # Searches help topics by name, title,
        # description, and related information

        if not isinstance(
            query,
            str,
        ):
            raise TypeError(
                "query must be a string."
            )

        normalized = (
            query.strip().lower()
        )

        if not normalized:
            return []

        matches: list[HelpTopic] = []

        for topic in self.topics.values():
            searchable = " ".join(
                [
                    topic.name,
                    topic.title,
                    topic.description,
                    topic.usage or "",
                    " ".join(
                        topic.notes
                    ),
                    " ".join(
                        topic.related
                    ),
                ]
            ).lower()

            if normalized in searchable:
                matches.append(
                    topic
                )

        return matches

    # Related Topics

    def related_topics(
        self,
        command: str,
    ) -> list[str]:
        # Returns topics related to a command

        topic = self.get_topic(
            command
        )

        return list(
            topic.related
        )

    # Version Information

    def format_version(
        self,
    ) -> str:
        # Formats toolkit version information

        return (
            f"{TOOLKIT_NAME} "
            f"version {TOOLKIT_VERSION}"
        )

        # Full Help Output

    def format_full_help(
        self,
    ) -> str:
        # Formats the complete toolkit help page

        sections = [
            self.format_overview(),
            "",
            self.format_examples(),
        ]

        return "\n\n".join(
            sections
        )

    def format(
        self,
        topic: str | None = None,
    ) -> str:
        # Formats help for a requested topic

        if topic is None:
            return self.format_overview()

        normalized = (
            topic.strip().lower()
        )

        if normalized in {
            "help",
            "overview",
            "main",
            "all",
        }:
            if normalized == "all":
                return self.format_full_help()

            return self.format_overview()

        if normalized in {
            "commands",
            "command",
            "list",
        }:
            return self.format_command_summary()

        if normalized in {
            "example",
            "examples",
        }:
            return self.format_examples()

        if normalized in {
            "usage",
        }:
            return self.format_usage()

        if normalized in {
            "version",
            "v",
        }:
            return self.format_version()

        if normalized.endswith(
            " options"
        ):
            command = normalized[
                :-len(" options")
            ].strip()

            return self.format_options(
                command
            )

        return self.format_topic(
            normalized
        )

    def display(
        self,
        topic: str | None = None,
        *,
        output_function: Any = print,
    ) -> None:
        # Displays formatted help text

        if not callable(
            output_function
        ):
            raise TypeError(
                "output_function must be callable."
            )

        output_function(
            self.format(
                topic
            )
        )

    # Topic Management

    def remove_topic(
        self,
        name: str,
    ) -> HelpTopic:
        # Removes and returns a registered topic

        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "Help topic name must be a string."
            )

        normalized = (
            name.strip().lower()
        )

        if normalized not in self.topics:
            raise UnknownHelpTopicError(
                f"Unknown help topic: {name}"
            )

        return self.topics.pop(
            normalized
        )

    def clear_topics(
        self,
    ) -> None:
        # Removes all registered topics

        self.topics.clear()

    def reset_topics(
        self,
    ) -> None:
        # Restores all default help topics

        self.clear_topics()
        self._register_default_topics()

    # Custom Examples

    def add_example(
        self,
        command: str,
        example: HelpExample,
    ) -> None:
        # Adds an example to an existing command

        if not isinstance(
            example,
            HelpExample,
        ):
            raise TypeError(
                "example must be a HelpExample."
            )

        topic = self.get_topic(
            command
        )

        topic.add_example(
            example
        )

    # Custom Notes

    def add_note(
        self,
        command: str,
        note: str,
    ) -> None:
        # Adds a note to an existing topic

        topic = self.get_topic(
            command
        )

        topic.add_note(
            note
        )


# Default Help Manager


_default_help_manager = HelpManager()


def get_help_manager() -> HelpManager:
    # Returns the default help manager

    return _default_help_manager


def set_help_manager(
    manager: HelpManager,
) -> None:
    # Replaces the default help manager

    global _default_help_manager

    if not isinstance(
        manager,
        HelpManager,
    ):
        raise TypeError(
            "manager must be a HelpManager."
        )

    _default_help_manager = manager


# Convenience Functions


def show_help(
    topic: str | None = None,
) -> None:
    # Displays help for a topic

    _default_help_manager.display(
        topic
    )


def get_help(
    topic: str | None = None,
) -> str:
    # Returns formatted help text

    return _default_help_manager.format(
        topic
    )


def get_full_help() -> str:
    # Returns the complete help page

    return _default_help_manager.format_full_help()


def get_command_help(
    command: str,
) -> str:
    # Returns help for a specific command

    return _default_help_manager.format_topic(
        command
    )


def get_command_options(
    command: str,
) -> str:
    # Returns formatted options for a command

    return _default_help_manager.format_options(
        command
    )


def get_usage(
    command: str | None = None,
) -> str:
    # Returns usage information

    return _default_help_manager.format_usage(
        command
    )


def get_examples(
    command: str | None = None,
) -> str:
    # Returns formatted examples

    return _default_help_manager.format_examples(
        command=command
    )


def search_help(
    query: str,
) -> list[HelpTopic]:
    # Searches available help topics

    return _default_help_manager.search(
        query
    )


def has_help_topic(
    topic: str,
) -> bool:
    # Checks whether a help topic exists

    return _default_help_manager.has_topic(
        topic
    )


def list_help_topics() -> list[str]:
    # Returns all available help topics

    return _default_help_manager.list_topics()


def get_related_topics(
    command: str,
) -> list[str]:
    # Returns topics related to a command

    return _default_help_manager.related_topics(
        command
    )


def get_version() -> str:
    # Returns formatted toolkit version

    return _default_help_manager.format_version()


# Help Builder Functions


def create_topic(
    name: str,
    title: str,
    description: str,
    *,
    usage: str | None = None,
    examples: Iterable[
        HelpExample
    ] | None = None,
    notes: Iterable[
        str
    ] | None = None,
    related: Iterable[
        str
    ] | None = None,
) -> HelpTopic:
    # Creates a HelpTopic object

    topic = HelpTopic(
        name=name,
        title=title,
        description=description,
        usage=usage,
    )

    if examples is not None:
        for example in examples:
            topic.add_example(
                example
            )

    if notes is not None:
        for note in notes:
            topic.add_note(
                note
            )

    if related is not None:
        for related_topic in related:
            if isinstance(
                related_topic,
                str,
            ) and related_topic.strip():
                topic.related.append(
                    related_topic.strip()
                )

    return topic


def create_example(
    command: str,
    description: str,
    *,
    output: str | None = None,
) -> HelpExample:
    # Creates a HelpExample object

    return HelpExample(
        command=command,
        description=description,
        output=output,
    )


# Self-Test


def self_test() -> bool:
    # Runs non-interactive help-system tests

    try:
        manager = HelpManager()

        # Basic topic registration

        if not manager.has_topic(
            "overview"
        ):
            return False

        if not manager.has_topic(
            "encrypt"
        ):
            return False

        # Topic retrieval

        encrypt_topic = manager.get_topic(
            "encrypt"
        )

        if encrypt_topic.name != "encrypt":
            return False

        # Formatting

        overview = manager.format_overview()

        if TOOLKIT_NAME not in overview:
            return False

        if "encrypt" not in overview:
            return False

        command_help = manager.format_topic(
            "encrypt"
        )

        if "Encrypt" not in command_help:
            return False

        # Examples

        examples = manager.format_examples(
            command="encrypt"
        )

        if "Hello" not in examples:
            return False

        # Options

        options = manager.format_options(
            "encrypt"
        )

        if "--key" not in options:
            return False

        # Usage

        usage = manager.format_usage(
            "encrypt"
        )

        if "encrypt" not in usage:
            return False

        # Search

        matches = manager.search(
            "entropy"
        )

        if not any(
            topic.name == "entropy"
            for topic in matches
        ):
            return False

        # Custom topic

        custom_topic = create_topic(
            "custom",
            "Custom Topic",
            "A custom help topic.",
            usage="custom [options]",
        )

        manager.register_topic(
            custom_topic
        )

        if not manager.has_topic(
            "custom"
        ):
            return False

        # Custom example

        example = create_example(
            "custom --test",
            "Run the custom example.",
        )

        manager.add_example(
            "custom",
            example,
        )

        if not manager.get_topic(
            "custom"
        ).examples:
            return False

        # Version

        version = manager.format_version()

        if TOOLKIT_NAME not in version:
            return False

        if TOOLKIT_VERSION not in version:
            return False

        return True

    except (
        HelpError,
        TypeError,
        ValueError,
    ):
        return False


# Module Exports


__all__ = [
    # Exceptions
    "HelpError",
    "UnknownHelpTopicError",
    "HelpFormattingError",

    # Data Models
    "HelpExample",
    "HelpTopic",

    # Constants
    "TOOLKIT_NAME",
    "TOOLKIT_COMMAND",
    "TOOLKIT_VERSION",
    "HELP_WIDTH",
    "HELP_TOPICS",
    "OVERVIEW_DESCRIPTION",
    "GENERAL_USAGE",
    "COMMAND_DESCRIPTIONS",
    "COMMAND_USAGE",
    "COMMAND_OPTIONS",
    "COMMAND_EXAMPLES",

    # Manager
    "HelpManager",

    # Manager Access
    "get_help_manager",
    "set_help_manager",

    # Convenience Functions
    "show_help",
    "get_help",
    "get_full_help",
    "get_command_help",
    "get_command_options",
    "get_usage",
    "get_examples",
    "search_help",
    "has_help_topic",
    "list_help_topics",
    "get_related_topics",
    "get_version",

    # Builders
    "create_topic",
    "create_example",

    # Testing
    "self_test",
]

