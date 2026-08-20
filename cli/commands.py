# commands.py

# Command execution system for the
# Cryptography Toolkit CLI

# Provides command registration, command dispatching,
# command execution, result handling, and integration
# between the CLI and the toolkit's core components


from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

from typing import (
    Any,
    Callable,
    Iterable,
    Mapping,
    Sequence,
)


# Command Exceptions


class CommandError(Exception):
    # Base exception for CLI command errors

    pass


class UnknownCommandError(CommandError):
    # Raised when an unknown command is requested

    pass


class CommandExecutionError(CommandError):
    # Raised when a command fails during execution

    pass


class CommandRegistrationError(CommandError):
    # Raised when command registration fails

    pass


class CommandValidationError(CommandError):
    # Raised when command arguments are invalid

    pass


# Command Result


@dataclass
class CommandResult:
    # Represents the result of a CLI command

    success: bool = True
    message: str = ""
    data: Any = None
    exit_code: int = 0
    command: str | None = None
    error: Exception | None = None

    @classmethod
    def ok(
        cls,
        message: str = "",
        *,
        data: Any = None,
        command: str | None = None,
    ) -> CommandResult:
        # Creates a successful command result

        return cls(
            success=True,
            message=message,
            data=data,
            exit_code=0,
            command=command,
        )

    @classmethod
    def failure(
        cls,
        message: str,
        *,
        exit_code: int = 1,
        command: str | None = None,
        error: Exception | None = None,
        data: Any = None,
    ) -> CommandResult:
        # Creates a failed command result

        return cls(
            success=False,
            message=message,
            data=data,
            exit_code=exit_code,
            command=command,
            error=error,
        )

    def __bool__(
        self,
    ) -> bool:
        # Allows a CommandResult to be evaluated
        # directly as True or False

        return self.success


# Command Context


@dataclass
class CommandContext:
    # Stores information shared during command execution

    command: str
    args: Sequence[Any] = field(
        default_factory=tuple
    )
    options: Mapping[
        str,
        Any
    ] = field(
        default_factory=dict
    )
    input_text: str | None = None
    output_path: str | None = None
    interactive: bool = False
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def get_option(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        # Returns a command option

        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "Option name must be a string."
            )

        return self.options.get(
            name,
            default,
        )

    def has_option(
        self,
        name: str,
    ) -> bool:
        # Checks whether an option exists

        return name in self.options

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        # Stores execution metadata

        if not isinstance(
            key,
            str,
        ):
            raise TypeError(
                "Metadata key must be a string."
            )

        self.metadata[
            key
        ] = value


# Command Specification


@dataclass
class CommandSpec:
    # Describes a registered CLI command

    name: str
    description: str
    handler: Callable[
        [CommandContext],
        CommandResult | Any,
    ]

    aliases: tuple[str, ...] = ()
    usage: str | None = None
    requires_input: bool = False
    requires_key: bool = False
    requires_output: bool = False
    hidden: bool = False
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(
        self,
    ) -> None:
        # Validates command configuration

        if not isinstance(
            self.name,
            str,
        ):
            raise TypeError(
                "Command name must be a string."
            )

        self.name = (
            self.name.strip().lower()
        )

        if not self.name:
            raise ValueError(
                "Command name cannot be empty."
            )

        if not isinstance(
            self.description,
            str,
        ):
            raise TypeError(
                "Command description must be a string."
            )

        if not callable(
            self.handler
        ):
            raise TypeError(
                "Command handler must be callable."
            )

        normalized_aliases = []

        for alias in self.aliases:
            if not isinstance(
                alias,
                str,
            ):
                raise TypeError(
                    "Command aliases must be strings."
                )

            alias = (
                alias.strip().lower()
            )

            if (
                alias
                and alias != self.name
            ):
                normalized_aliases.append(
                    alias
                )

        self.aliases = tuple(
            dict.fromkeys(
                normalized_aliases
            )
        )

    def matches(
        self,
        name: str,
    ) -> bool:
        # Checks whether a name matches this command

        if not isinstance(
            name,
            str,
        ):
            return False

        normalized = (
            name.strip().lower()
        )

        return (
            normalized == self.name
            or normalized in self.aliases
        )


# Command Registry


class CommandRegistry:
    # Stores and manages registered commands

    def __init__(
        self,
    ) -> None:
        # Initializes the registry

        self._commands: dict[
            str,
            CommandSpec,
        ] = {}

        self._aliases: dict[
            str,
            str,
        ] = {}

    # Registration

    def register(
        self,
        command: CommandSpec,
        *,
        replace: bool = False,
    ) -> None:
        # Registers a command

        if not isinstance(
            command,
            CommandSpec,
        ):
            raise TypeError(
                "command must be a CommandSpec."
            )

        name = command.name

        if (
            name in self._commands
            and not replace
        ):
            raise CommandRegistrationError(
                f"Command already registered: {name}"
            )

        # Check aliases against existing commands

        for alias in command.aliases:
            existing_command = (
                self.resolve(alias)
                if (
                    alias in self._commands
                    or alias in self._aliases
                )
                else None
            )

            if (
                existing_command is not None
                and existing_command.name != name
                and not replace
            ):
                raise CommandRegistrationError(
                    f"Alias already registered: {alias}"
                )

        # Remove previous aliases when replacing

        if (
            replace
            and name in self._commands
        ):
            previous = self._commands[
                name
            ]

            for alias in previous.aliases:
                self._aliases.pop(
                    alias,
                    None,
                )

        self._commands[
            name
        ] = command

        for alias in command.aliases:
            self._aliases[
                alias
            ] = name

    def unregister(
        self,
        name: str,
    ) -> CommandSpec:
        # Removes and returns a command

        command = self.resolve(
            name
        )

        if command is None:
            raise UnknownCommandError(
                f"Unknown command: {name}"
            )

        self._commands.pop(
            command.name,
            None,
        )

        for alias in command.aliases:
            self._aliases.pop(
                alias,
                None,
            )

        return command

    # Lookup

    def resolve(
        self,
        name: str,
    ) -> CommandSpec | None:
        # Resolves a command name or alias

        if not isinstance(
            name,
            str,
        ):
            return None

        normalized = (
            name.strip().lower()
        )

        if normalized in self._commands:
            return self._commands[
                normalized
            ]

        canonical = self._aliases.get(
            normalized
        )

        if canonical is None:
            return None

        return self._commands.get(
            canonical
        )

    def get(
        self,
        name: str,
    ) -> CommandSpec:
        # Retrieves a command or raises an error

        command = self.resolve(
            name
        )

        if command is None:
            raise UnknownCommandError(
                f"Unknown command: {name}"
            )

        return command

    def contains(
        self,
        name: str,
    ) -> bool:
        # Checks whether a command exists

        return self.resolve(
            name
        ) is not None

    # Listing

    def list_commands(
        self,
        *,
        include_hidden: bool = False,
    ) -> list[CommandSpec]:
        # Returns registered commands

        commands = list(
            self._commands.values()
        )

        if not include_hidden:
            commands = [
                command
                for command in commands
                if not command.hidden
            ]

        return sorted(
            commands,
            key=lambda command: command.name,
        )

    def names(
        self,
        *,
        include_hidden: bool = False,
    ) -> list[str]:
        # Returns registered command names

        return [
            command.name
            for command in self.list_commands(
                include_hidden=include_hidden
            )
        ]

    def aliases(
        self,
    ) -> dict[str, str]:
        # Returns a copy of the alias mapping

        return dict(
            self._aliases
        )

    def clear(
        self,
    ) -> None:
        # Removes all registered commands

        self._commands.clear()
        self._aliases.clear()

    def __len__(
        self,
    ) -> int:
        # Returns the number of commands

        return len(
            self._commands
        )

    def __contains__(
        self,
        name: str,
    ) -> bool:
        # Supports membership testing

        return self.contains(
            name
        )


# Command Manager


class CommandManager:
    # Handles command registration and execution

    def __init__(
        self,
        registry: CommandRegistry | None = None,
    ) -> None:
        # Initializes the command manager

        self.registry = (
            registry
            if registry is not None
            else CommandRegistry()
        )

    # Registration

    def register(
        self,
        command: CommandSpec,
        *,
        replace: bool = False,
    ) -> None:
        # Registers a command with the manager

        self.registry.register(
            command,
            replace=replace,
        )

    def register_function(
        self,
        name: str,
        handler: Callable[
            [CommandContext],
            CommandResult | Any,
        ],
        *,
        description: str = "",
        aliases: Iterable[str] = (),
        usage: str | None = None,
        requires_input: bool = False,
        requires_key: bool = False,
        requires_output: bool = False,
        hidden: bool = False,
        metadata: Mapping[str, Any] | None = None,
    ) -> CommandSpec:
        # Creates and registers a command from a function

        command = CommandSpec(
            name=name,
            description=description,
            handler=handler,
            aliases=tuple(
                aliases
            ),
            usage=usage,
            requires_input=requires_input,
            requires_key=requires_key,
            requires_output=requires_output,
            hidden=hidden,
            metadata=dict(
                metadata or {}
            ),
        )

        self.register(
            command
        )

        return command

    # Lookup

    def get_command(
        self,
        name: str,
    ) -> CommandSpec:
        # Retrieves a registered command

        return self.registry.get(
            name
        )

    def has_command(
        self,
        name: str,
    ) -> bool:
        # Checks whether a command exists

        return self.registry.contains(
            name
        )

    def list_commands(
        self,
        *,
        include_hidden: bool = False,
    ) -> list[CommandSpec]:
        # Lists available commands

        return self.registry.list_commands(
            include_hidden=include_hidden
        )

    # Context Creation

    def create_context(
        self,
        command: str,
        *,
        args: Sequence[Any] = (),
        options: Mapping[str, Any] | None = None,
        input_text: str | None = None,
        output_path: str | None = None,
        interactive: bool = False,
        metadata: Mapping[str, Any] | None = None,
    ) -> CommandContext:
        # Creates a command execution context

        if not isinstance(
            command,
            str,
        ):
            raise TypeError(
                "command must be a string."
            )

        if not command.strip():
            raise ValueError(
                "command cannot be empty."
            )

        return CommandContext(
            command=command.strip().lower(),
            args=tuple(args),
            options=dict(
                options or {}
            ),
            input_text=input_text,
            output_path=output_path,
            interactive=interactive,
            metadata=dict(
                metadata or {}
            ),
        )

    # Validation

    def validate_context(
        self,
        command: CommandSpec,
        context: CommandContext,
    ) -> None:
        # Validates a command context against
        # its command specification

        if command.requires_input:
            if (
                context.input_text is None
                and not context.args
            ):
                raise CommandValidationError(
                    f"Command '{command.name}' "
                    "requires input."
                )

        if command.requires_key:
            if not context.has_option(
                "key"
            ):
                raise CommandValidationError(
                    f"Command '{command.name}' "
                    "requires a key."
                )

        if command.requires_output:
            if not context.output_path:
                raise CommandValidationError(
                    f"Command '{command.name}' "
                    "requires an output path."
                )

    # Execution

    def execute(
        self,
        name: str,
        *,
        args: Sequence[Any] = (),
        options: Mapping[str, Any] | None = None,
        input_text: str | None = None,
        output_path: str | None = None,
        interactive: bool = False,
        metadata: Mapping[str, Any] | None = None,
    ) -> CommandResult:
        # Executes a registered command

        command = self.registry.get(
            name
        )

        context = self.create_context(
            command.name,
            args=args,
            options=options,
            input_text=input_text,
            output_path=output_path,
            interactive=interactive,
            metadata=metadata,
        )

        self.validate_context(
            command,
            context,
        )

        try:
            result = command.handler(
                context
            )

        except CommandError:
            raise

        except Exception as error:
            raise CommandExecutionError(
                f"Command '{command.name}' "
                "failed during execution."
            ) from error

        if isinstance(
            result,
            CommandResult,
        ):
            if result.command is None:
                result.command = command.name

            return result

        return CommandResult.ok(
            data=result,
            command=command.name,
        )

    # Safe Execution

    def execute_safe(
        self,
        name: str,
        *,
        args: Sequence[Any] = (),
        options: Mapping[str, Any] | None = None,
        input_text: str | None = None,
        output_path: str | None = None,
        interactive: bool = False,
        metadata: Mapping[str, Any] | None = None,
    ) -> CommandResult:
        # Executes a command while converting failures
        # into CommandResult objects

        try:
            return self.execute(
                name,
                args=args,
                options=options,
                input_text=input_text,
                output_path=output_path,
                interactive=interactive,
                metadata=metadata,
            )

        except UnknownCommandError as error:
            return CommandResult.failure(
                str(error),
                exit_code=2,
                command=name,
                error=error,
            )

        except CommandValidationError as error:
            return CommandResult.failure(
                str(error),
                exit_code=3,
                command=name,
                error=error,
            )

        except CommandExecutionError as error:
            return CommandResult.failure(
                str(error),
                exit_code=1,
                command=name,
                error=error,
            )

        except CommandError as error:
            return CommandResult.failure(
                str(error),
                exit_code=1,
                command=name,
                error=error,
            )

            # Command Removal

    def unregister(
        self,
        name: str,
    ) -> CommandSpec:
        # Removes a command from the registry

        return self.registry.unregister(
            name
        )

    def clear(
        self,
    ) -> None:
        # Removes all commands

        self.registry.clear()

    # Command Execution Helpers

    def execute_context(
        self,
        context: CommandContext,
    ) -> CommandResult:
        # Executes a command using an existing context

        if not isinstance(
            context,
            CommandContext,
        ):
            raise TypeError(
                "context must be a CommandContext."
            )

        command = self.registry.get(
            context.command
        )

        self.validate_context(
            command,
            context,
        )

        try:
            result = command.handler(
                context
            )

        except CommandError:
            raise

        except Exception as error:
            raise CommandExecutionError(
                f"Command '{command.name}' "
                "failed during execution."
            ) from error

        if isinstance(
            result,
            CommandResult,
        ):
            if result.command is None:
                result.command = command.name

            return result

        return CommandResult.ok(
            data=result,
            command=command.name,
        )

    def execute_safe_context(
        self,
        context: CommandContext,
    ) -> CommandResult:
        # Safely executes an existing command context

        try:
            return self.execute_context(
                context
            )

        except UnknownCommandError as error:
            return CommandResult.failure(
                str(error),
                exit_code=2,
                command=context.command,
                error=error,
            )

        except CommandValidationError as error:
            return CommandResult.failure(
                str(error),
                exit_code=3,
                command=context.command,
                error=error,
            )

        except CommandExecutionError as error:
            return CommandResult.failure(
                str(error),
                exit_code=1,
                command=context.command,
                error=error,
            )

        except CommandError as error:
            return CommandResult.failure(
                str(error),
                exit_code=1,
                command=context.command,
                error=error,
            )

    # Command Information

    def command_info(
        self,
        name: str,
    ) -> dict[str, Any]:
        # Returns structured information about
        # a registered command

        command = self.get_command(
            name
        )

        return {
            "name": command.name,
            "description": command.description,
            "aliases": list(
                command.aliases
            ),
            "usage": command.usage,
            "requires_input": (
                command.requires_input
            ),
            "requires_key": (
                command.requires_key
            ),
            "requires_output": (
                command.requires_output
            ),
            "hidden": command.hidden,
            "metadata": dict(
                command.metadata
            ),
        }

    def all_command_info(
        self,
        *,
        include_hidden: bool = False,
    ) -> list[dict[str, Any]]:
        # Returns information for every command

        return [
            self.command_info(
                command.name
            )
            for command in self.list_commands(
                include_hidden=include_hidden
            )
        ]


# Built-in Command Handlers


def _get_input(
    context: CommandContext,
) -> str:
    # Retrieves command input from the context

    if context.input_text is not None:
        return context.input_text

    if context.args:
        return " ".join(
            str(argument)
            for argument in context.args
        )

    raise CommandValidationError(
        "No input text was provided."
    )


def _get_key(
    context: CommandContext,
) -> int:
    # Retrieves and validates a cipher key

    value = context.get_option(
        "key"
    )

    if value is None:
        raise CommandValidationError(
            "A cipher key is required."
        )

    try:
        return int(
            value
        )

    except (
        TypeError,
        ValueError,
    ) as error:
        raise CommandValidationError(
            "Cipher key must be an integer."
        ) from error


def _get_output_path(
    context: CommandContext,
) -> str | None:
    # Retrieves the requested output path

    value = context.output_path

    if value is None:
        value = context.get_option(
            "output"
        )

    if value is None:
        return None

    return str(
        value
    )


def _import_caesar():
    # Imports the Caesar cipher implementation

    try:
        from cipher.caesar import (
            CaesarCipher,
        )

        return CaesarCipher

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load the Caesar Cipher "
            "implementation."
        ) from error


def _create_caesar_cipher(
    key: int,
):
    # Creates a Caesar Cipher instance

    CaesarCipher = _import_caesar()

    try:
        return CaesarCipher(
            key
        )

    except TypeError:
        try:
            return CaesarCipher(
                shift=key
            )

        except TypeError as error:
            raise CommandExecutionError(
                "Unable to initialize Caesar Cipher."
            ) from error


def handle_encrypt(
    context: CommandContext,
) -> CommandResult:
    # Handles the encrypt command

    text = _get_input(
        context
    )

    key = _get_key(
        context
    )

    cipher = _create_caesar_cipher(
        key
    )

    try:
        encrypted = cipher.encrypt(
            text
        )

    except AttributeError as error:
        raise CommandExecutionError(
            "Caesar Cipher does not provide "
            "an encrypt method."
        ) from error

    output_path = _get_output_path(
        context
    )

    if output_path:
        try:
            from fileio.file_manager import (
                FileManager,
            )

            manager = FileManager()

            manager.write_file(
                output_path,
                encrypted,
            )

            return CommandResult.ok(
                message=(
                    f"Encrypted output written to "
                    f"{output_path}"
                ),
                data=encrypted,
                command="encrypt",
            )

        except ImportError:
            raise CommandExecutionError(
                "Unable to load file manager."
            )

    return CommandResult.ok(
        message=encrypted,
        data=encrypted,
        command="encrypt",
    )


def handle_decrypt(
    context: CommandContext,
) -> CommandResult:
    # Handles the decrypt command

    text = _get_input(
        context
    )

    key = _get_key(
        context
    )

    cipher = _create_caesar_cipher(
        key
    )

    try:
        decrypted = cipher.decrypt(
            text
        )

    except AttributeError as error:
        raise CommandExecutionError(
            "Caesar Cipher does not provide "
            "a decrypt method."
        ) from error

    output_path = _get_output_path(
        context
    )

    if output_path:
        try:
            from fileio.file_manager import (
                FileManager,
            )

            manager = FileManager()

            manager.write_file(
                output_path,
                decrypted,
            )

            return CommandResult.ok(
                message=(
                    f"Decrypted output written to "
                    f"{output_path}"
                ),
                data=decrypted,
                command="decrypt",
            )

        except ImportError:
            raise CommandExecutionError(
                "Unable to load file manager."
            )

    return CommandResult.ok(
        message=decrypted,
        data=decrypted,
        command="decrypt",
    )


def handle_frequency(
    context: CommandContext,
) -> CommandResult:
    # Handles frequency analysis

    text = _get_input(
        context
    )

    try:
        from analysis.frequency import (
            frequency_analysis,
        )

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load frequency analysis."
        ) from error

    try:
        result = frequency_analysis(
            text
        )

    except TypeError:
        try:
            result = frequency_analysis(
                text=text
            )

        except Exception as error:
            raise CommandExecutionError(
                "Frequency analysis failed."
            ) from error

    except Exception as error:
        raise CommandExecutionError(
            "Frequency analysis failed."
        ) from error

    return CommandResult.ok(
        message="Frequency analysis completed.",
        data=result,
        command="frequency",
    )


def handle_entropy(
    context: CommandContext,
) -> CommandResult:
    # Handles entropy analysis

    text = _get_input(
        context
    )

    try:
        from analysis.entropy import (
            shannon_entropy,
        )

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load entropy analysis."
        ) from error

    try:
        result = shannon_entropy(
            text
        )

    except TypeError:
        try:
            result = shannon_entropy(
                text=text
            )

        except Exception as error:
            raise CommandExecutionError(
                "Entropy calculation failed."
            ) from error

    except Exception as error:
        raise CommandExecutionError(
            "Entropy calculation failed."
        ) from error

    return CommandResult.ok(
        message="Entropy calculation completed.",
        data=result,
        command="entropy",
    )


def handle_ioc(
    context: CommandContext,
) -> CommandResult:
    # Handles Index of Coincidence analysis

    text = _get_input(
        context
    )

    try:
        from analysis.ioc import (
            index_of_coincidence,
        )

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load IOC analysis."
        ) from error

    try:
        result = index_of_coincidence(
            text
        )

    except TypeError:
        try:
            result = index_of_coincidence(
                text=text
            )

        except Exception as error:
            raise CommandExecutionError(
                "IOC calculation failed."
            ) from error

    except Exception as error:
        raise CommandExecutionError(
            "IOC calculation failed."
        ) from error

    return CommandResult.ok(
        message=(
            "Index of Coincidence calculation "
            "completed."
        ),
        data=result,
        command="ioc",
    )


def handle_ngrams(
    context: CommandContext,
) -> CommandResult:
    # Handles n-gram analysis

    text = _get_input(
        context
    )

    n = context.get_option(
        "n",
        2,
    )

    try:
        n = int(
            n
        )

    except (
        TypeError,
        ValueError,
    ) as error:
        raise CommandValidationError(
            "n-gram size must be an integer."
        ) from error

    if n < 1:
        raise CommandValidationError(
            "n-gram size must be at least 1."
        )

    try:
        from analysis.ngrams import (
            ngram_analysis,
        )

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load n-gram analysis."
        ) from error

    try:
        result = ngram_analysis(
            text,
            n=n,
        )

    except TypeError:
        try:
            result = ngram_analysis(
                text,
                n,
            )

        except Exception as error:
            raise CommandExecutionError(
                "N-gram analysis failed."
            ) from error

    except Exception as error:
        raise CommandExecutionError(
            "N-gram analysis failed."
        ) from error

    return CommandResult.ok(
        message="N-gram analysis completed.",
        data=result,
        command="ngrams",
    )

# commands.py — Part 3
# Continued from Part 2


def handle_bruteforce(
    context: CommandContext,
) -> CommandResult:
    # Handles automatic Caesar Cipher cracking

    text = _get_input(
        context
    )

    min_key = context.get_option(
        "min_key",
        0,
    )

    max_key = context.get_option(
        "max_key",
        25,
    )

    top = context.get_option(
        "top",
        5,
    )

    try:
        min_key = int(
            min_key
        )
        max_key = int(
            max_key
        )
        top = int(
            top
        )
    except (
        TypeError,
        ValueError,
    ) as error:
        raise CommandValidationError(
            "Brute-force key values and "
            "result count must be integers."
        ) from error

    if min_key > max_key:
        raise CommandValidationError(
            "Minimum key cannot be greater "
            "than maximum key."
        )

    if top < 1:
        raise CommandValidationError(
            "Top result count must be at least 1."
        )

    try:
        from analysis.brute_force import (
            brute_force,
        )

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load brute-force analysis."
        ) from error

    try:
        result = brute_force(
            text,
            min_key=min_key,
            max_key=max_key,
            top=top,
        )

    except TypeError:
        try:
            result = brute_force(
                text,
                min_key,
                max_key,
            )

        except Exception as error:
            raise CommandExecutionError(
                "Brute-force analysis failed."
            ) from error

    except Exception as error:
        raise CommandExecutionError(
            "Brute-force analysis failed."
        ) from error

    return CommandResult.ok(
        message=(
            "Brute-force analysis completed."
        ),
        data=result,
        command="bruteforce",
    )


def handle_analyze(
    context: CommandContext,
) -> CommandResult:
    # Handles combined cryptanalysis

    text = _get_input(
        context
    )

    results: dict[
        str,
        Any,
    ] = {}

    requested = False

    if context.get_option(
        "frequency",
        False,
    ):
        requested = True

        frequency_context = CommandContext(
            command="frequency",
            input_text=text,
            options=dict(
                context.options
            ),
            metadata=dict(
                context.metadata
            ),
        )

        result = handle_frequency(
            frequency_context
        )

        results[
            "frequency"
        ] = result.data

    if context.get_option(
        "entropy",
        False,
    ):
        requested = True

        entropy_context = CommandContext(
            command="entropy",
            input_text=text,
            options=dict(
                context.options
            ),
            metadata=dict(
                context.metadata
            ),
        )

        result = handle_entropy(
            entropy_context
        )

        results[
            "entropy"
        ] = result.data

    if context.get_option(
        "ioc",
        False,
    ):
        requested = True

        ioc_context = CommandContext(
            command="ioc",
            input_text=text,
            options=dict(
                context.options
            ),
            metadata=dict(
                context.metadata
            ),
        )

        result = handle_ioc(
            ioc_context
        )

        results[
            "ioc"
        ] = result.data

    if context.get_option(
        "ngrams",
        False,
    ):
        requested = True

        ngram_context = CommandContext(
            command="ngrams",
            input_text=text,
            options=dict(
                context.options
            ),
            metadata=dict(
                context.metadata
            ),
        )

        result = handle_ngrams(
            ngram_context
        )

        results[
            "ngrams"
        ] = result.data

    if not requested:
        # Run the most useful default analysis set

        results[
            "frequency"
        ] = handle_frequency(
            CommandContext(
                command="frequency",
                input_text=text,
                options=dict(
                    context.options
                ),
            )
        ).data

        results[
            "entropy"
        ] = handle_entropy(
            CommandContext(
                command="entropy",
                input_text=text,
                options=dict(
                    context.options
                ),
            )
        ).data

        results[
            "ioc"
        ] = handle_ioc(
            CommandContext(
                command="ioc",
                input_text=text,
                options=dict(
                    context.options
                ),
            )
        ).data

    return CommandResult.ok(
        message=(
            "Cryptanalysis completed."
        ),
        data=results,
        command="analyze",
    )


def handle_history(
    context: CommandContext,
) -> CommandResult:
    # Handles encryption and analysis history

    action = (
        str(
            context.args[0]
        ).lower()
        if context.args
        else "list"
    )

    try:
        from fileio.history import (
            HistoryManager,
        )

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load history manager."
        ) from error

    try:
        manager = HistoryManager()

    except TypeError:
        manager = HistoryManager

    if action == "list":
        try:
            data = manager.list_history()

        except AttributeError:
            try:
                data = manager.get_history()

            except AttributeError as error:
                raise CommandExecutionError(
                    "History manager does not support "
                    "listing history."
                ) from error

        return CommandResult.ok(
            message="History retrieved.",
            data=data,
            command="history",
        )

    if action == "latest":
        try:
            data = manager.latest()

        except AttributeError:
            try:
                data = manager.get_latest()

            except AttributeError as error:
                raise CommandExecutionError(
                    "History manager does not support "
                    "latest-entry retrieval."
                ) from error

        return CommandResult.ok(
            message="Latest history entry retrieved.",
            data=data,
            command="history",
        )

    if action == "clear":
        try:
            manager.clear()

        except AttributeError as error:
            raise CommandExecutionError(
                "History manager does not support "
                "clearing history."
            ) from error

        return CommandResult.ok(
            message="History cleared.",
            command="history",
        )

    if action == "summary":
        try:
            data = manager.summary()

        except AttributeError as error:
            raise CommandExecutionError(
                "History manager does not support "
                "history summaries."
            ) from error

        return CommandResult.ok(
            message="History summary generated.",
            data=data,
            command="history",
        )

    if action == "search":
        if len(
            context.args
        ) < 2:
            raise CommandValidationError(
                "A search query is required."
            )

        query = " ".join(
            str(argument)
            for argument in context.args[1:]
        )

        try:
            data = manager.search(
                query
            )

        except AttributeError as error:
            raise CommandExecutionError(
                "History manager does not support "
                "history searching."
            ) from error

        return CommandResult.ok(
            message="History search completed.",
            data=data,
            command="history",
        )

    raise CommandValidationError(
        f"Unknown history action: {action}"
    )


def handle_export(
    context: CommandContext,
) -> CommandResult:
    # Handles exporting command or analysis data

    if not context.args:
        raise CommandValidationError(
            "Export requires input and output "
            "information."
        )

    source = context.args[0]

    output = (
        context.output_path
        or context.get_option(
            "output"
        )
    )

    if output is None and len(
        context.args
    ) > 1:
        output = context.args[1]

    if output is None:
        raise CommandValidationError(
            "An output path is required."
        )

    export_format = context.get_option(
        "format"
    )

    try:
        from fileio.exporters import (
            export_data,
        )

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load export utilities."
        ) from error

    try:
        result = export_data(
            source,
            output,
            format=export_format,
        )

    except TypeError:
        try:
            result = export_data(
                source,
                output,
            )

        except Exception as error:
            raise CommandExecutionError(
                "Export operation failed."
            ) from error

    except Exception as error:
        raise CommandExecutionError(
            "Export operation failed."
        ) from error

    return CommandResult.ok(
        message=(
            f"Data exported to {output}"
        ),
        data=result,
        command="export",
    )


def handle_backup(
    context: CommandContext,
) -> CommandResult:
    # Handles file backup operations

    action = (
        str(
            context.args[0]
        ).lower()
        if context.args
        else "list"
    )

    try:
        from fileio.backups import (
            BackupManager,
        )

    except ImportError as error:
        raise CommandExecutionError(
            "Unable to load backup manager."
        ) from error

    manager = BackupManager()

    if action == "list":
        try:
            data = manager.list_backups()

        except AttributeError as error:
            raise CommandExecutionError(
                "Backup manager does not support "
                "listing backups."
            ) from error

        return CommandResult.ok(
            message="Backups retrieved.",
            data=data,
            command="backup",
        )

    if action == "create":
        if len(
            context.args
        ) < 2:
            raise CommandValidationError(
                "A source file is required."
            )

        source = context.args[1]

        try:
            data = manager.create_backup(
                source
            )

        except AttributeError as error:
            raise CommandExecutionError(
                "Backup manager does not support "
                "creating backups."
            ) from error

        return CommandResult.ok(
            message="Backup created.",
            data=data,
            command="backup",
        )

    if action == "restore":
        if len(
            context.args
        ) < 3:
            raise CommandValidationError(
                "Backup name and destination "
                "are required."
            )

        backup_name = context.args[1]
        destination = context.args[2]

        try:
            data = manager.restore_backup(
                backup_name,
                destination,
            )

        except AttributeError as error:
            raise CommandExecutionError(
                "Backup manager does not support "
                "restoring backups."
            ) from error

        return CommandResult.ok(
            message="Backup restored.",
            data=data,
            command="backup",
        )

    if action == "delete":
        if len(
            context.args
        ) < 2:
            raise CommandValidationError(
                "A backup name is required."
            )

        backup_name = context.args[1]

        try:
            data = manager.delete_backup(
                backup_name
            )

        except AttributeError as error:
            raise CommandExecutionError(
                "Backup manager does not support "
                "deleting backups."
            ) from error

        return CommandResult.ok(
            message="Backup deleted.",
            data=data,
            command="backup",
        )

    if action == "summary":
        try:
            data = manager.summary()

        except AttributeError as error:
            raise CommandExecutionError(
                "Backup manager does not support "
                "backup summaries."
            ) from error

        return CommandResult.ok(
            message="Backup summary generated.",
            data=data,
            command="backup",
        )

    raise CommandValidationError(
        f"Unknown backup action: {action}"
    )


def handle_version(
    context: CommandContext,
) -> CommandResult:
    # Handles the version command

    try:
        from .help import (
            get_version,
        )

        version = get_version()

    except ImportError:
        version = (
            "Caesar Cipher Toolkit version 1.0.0"
        )

    return CommandResult.ok(
        message=version,
        data=version,
        command="version",
    )


# Default Command Registration


def register_default_commands(
    manager: CommandManager,
) -> CommandManager:
    # Registers all built-in CLI commands

    if not isinstance(
        manager,
        CommandManager,
    ):
        raise TypeError(
            "manager must be a CommandManager."
        )

    manager.register_function(
        "encrypt",
        handle_encrypt,
        description=(
            "Encrypt plaintext using a "
            "Caesar Cipher."
        ),
        aliases=(
            "enc",
            "e",
        ),
        requires_input=True,
        requires_key=True,
    )

    manager.register_function(
        "decrypt",
        handle_decrypt,
        description=(
            "Decrypt ciphertext using a "
            "Caesar Cipher."
        ),
        aliases=(
            "dec",
            "d",
        ),
        requires_input=True,
        requires_key=True,
    )

    manager.register_function(
        "analyze",
        handle_analyze,
        description=(
            "Run cryptanalysis operations."
        ),
        aliases=(
            "analysis",
            "analyse",
        ),
        requires_input=True,
    )

    manager.register_function(
        "bruteforce",
        handle_bruteforce,
        description=(
            "Automatically test Caesar Cipher keys."
        ),
        aliases=(
            "brute",
            "crack",
        ),
        requires_input=True,
    )

    manager.register_function(
        "frequency",
        handle_frequency,
        description=(
            "Perform letter frequency analysis."
        ),
        aliases=(
            "freq",
        ),
        requires_input=True,
    )

    manager.register_function(
        "entropy",
        handle_entropy,
        description=(
            "Calculate Shannon entropy."
        ),
        aliases=(
            "ent",
        ),
        requires_input=True,
    )

    manager.register_function(
        "ioc",
        handle_ioc,
        description=(
            "Calculate the Index of Coincidence."
        ),
        aliases=(
            "coincidence",
        ),
        requires_input=True,
    )

    manager.register_function(
        "ngrams",
        handle_ngrams,
        description=(
            "Perform n-gram analysis."
        ),
        aliases=(
            "ngram",
        ),
        requires_input=True,
    )

    manager.register_function(
        "history",
        handle_history,
        description=(
            "View and manage operation history."
        ),
        aliases=(
            "hist",
        ),
    )

    manager.register_function(
        "export",
        handle_export,
        description=(
            "Export analysis or toolkit data."
        ),
        aliases=(
            "save-report",
        ),
        requires_input=True,
    )

    manager.register_function(
        "backup",
        handle_backup,
        description=(
            "Manage file backups."
        ),
        aliases=(
            "backups",
        ),
    )

    manager.register_function(
        "version",
        handle_version,
        description=(
            "Display the toolkit version."
        ),
        aliases=(
            "v",
            "--version",
        ),
    )

    return manager


# Default Command Manager


_default_command_manager = (
    CommandManager()
)

register_default_commands(
    _default_command_manager
)


def get_command_manager() -> CommandManager:
    # Returns the default command manager

    return _default_command_manager


def set_command_manager(
    manager: CommandManager,
) -> None:
    # Replaces the default command manager

    global _default_command_manager

    if not isinstance(
        manager,
        CommandManager,
    ):
        raise TypeError(
            "manager must be a CommandManager."
        )

    _default_command_manager = manager


# Convenience Execution Functions


def execute_command(
    name: str,
    *,
    args: Sequence[Any] = (),
    options: Mapping[str, Any] | None = None,
    input_text: str | None = None,
    output_path: str | None = None,
    interactive: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> CommandResult:
    # Executes a command using the default manager

    return _default_command_manager.execute(
        name,
        args=args,
        options=options,
        input_text=input_text,
        output_path=output_path,
        interactive=interactive,
        metadata=metadata,
    )


def execute_command_safe(
    name: str,
    *,
    args: Sequence[Any] = (),
    options: Mapping[str, Any] | None = None,
    input_text: str | None = None,
    output_path: str | None = None,
    interactive: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> CommandResult:
    # Safely executes a command using the
    # default manager

    return _default_command_manager.execute_safe(
        name,
        args=args,
        options=options,
        input_text=input_text,
        output_path=output_path,
        interactive=interactive,
        metadata=metadata,
    )


def list_commands(
    *,
    include_hidden: bool = False,
) -> list[str]:
    # Returns available command names

    return _default_command_manager.registry.names(
        include_hidden=include_hidden
    )


def get_command(
    name: str,
) -> CommandSpec:
    # Returns a registered command

    return _default_command_manager.get_command(
        name
    )


def has_command(
    name: str,
) -> bool:
    # Checks whether a command exists

    return _default_command_manager.has_command(
        name
    )


# Self-Test


def self_test() -> bool:
    # Runs non-interactive command-system tests

    try:
        manager = CommandManager()

        def test_handler(
            context: CommandContext,
        ) -> CommandResult:
            return CommandResult.ok(
                message="Test successful.",
                data={
                    "command": context.command,
                    "args": list(
                        context.args
                    ),
                },
            )

        manager.register_function(
            "test",
            test_handler,
            description="Test command.",
            aliases=(
                "t",
            ),
        )

        if not manager.has_command(
            "test"
        ):
            return False

        if not manager.has_command(
            "t"
        ):
            return False

        result = manager.execute(
            "test",
            args=(
                "hello",
                "world",
            ),
        )

        if not result.success:
            return False

        if result.command != "test":
            return False

        if result.data[
            "args"
        ] != [
            "hello",
            "world",
        ]:
            return False

        safe_result = manager.execute_safe(
            "does-not-exist"
        )

        if safe_result.success:
            return False

        return True

    except (
        CommandError,
        TypeError,
        ValueError,
    ):
        return False


# Module Exports


__all__ = [
    # Exceptions
    "CommandError",
    "UnknownCommandError",
    "CommandExecutionError",
    "CommandRegistrationError",
    "CommandValidationError",

    # Models
    "CommandResult",
    "CommandContext",
    "CommandSpec",

    # Registry
    "CommandRegistry",

    # Manager
    "CommandManager",

    # Handlers
    "handle_encrypt",
    "handle_decrypt",
    "handle_analyze",
    "handle_bruteforce",
    "handle_frequency",
    "handle_entropy",
    "handle_ioc",
    "handle_ngrams",
    "handle_history",
    "handle_export",
    "handle_backup",
    "handle_version",

    # Registration
    "register_default_commands",

    # Manager Access
    "get_command_manager",
    "set_command_manager",

    # Execution
    "execute_command",
    "execute_command_safe",

    # Lookup
    "list_commands",
    "get_command",
    "has_command",

    # Testing
    "self_test",
]

