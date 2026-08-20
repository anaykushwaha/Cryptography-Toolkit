# menu.py

# Interactive menu system for the
# Cryptography Toolkit CLI

# Provides menu items, menu navigation,
# interactive selection, command dispatching,
# and terminal-based menu management


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


# Menu Exceptions


class MenuError(Exception):
    # Base exception for CLI menu errors

    pass


class MenuSelectionError(MenuError):
    # Raised when an invalid menu selection is made

    pass


class MenuExitRequested(MenuError):
    # Raised when the user requests to leave a menu

    pass


class MenuConfigurationError(MenuError):
    # Raised when menu configuration is invalid

    pass


# Menu Result


@dataclass
class MenuResult:
    # Represents the result of a menu interaction

    success: bool = True
    message: str = ""
    value: Any = None
    exit_menu: bool = False
    command: str | None = None

    @classmethod
    def ok(
        cls,
        value: Any = None,
        *,
        message: str = "",
        command: str | None = None,
    ) -> MenuResult:
        # Creates a successful menu result

        return cls(
            success=True,
            message=message,
            value=value,
            exit_menu=False,
            command=command,
        )

    @classmethod
    def exit(
        cls,
        *,
        message: str = "",
    ) -> MenuResult:
        # Creates a result indicating that the
        # current menu should close

        return cls(
            success=True,
            message=message,
            value=None,
            exit_menu=True,
        )

    @classmethod
    def failure(
        cls,
        message: str,
    ) -> MenuResult:
        # Creates a failed menu result

        return cls(
            success=False,
            message=message,
            value=None,
            exit_menu=False,
        )

    def __bool__(
        self,
    ) -> bool:
        # Allows direct boolean evaluation

        return self.success


# Menu Item


@dataclass
class MenuItem:
    # Represents one selectable menu option

    key: str
    label: str
    description: str = ""
    action: Callable[
        ...,
        Any,
    ] | None = None
    command: str | None = None
    enabled: bool = True
    hidden: bool = False
    shortcut: str | None = None
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(
        self,
    ) -> None:
        # Validates menu item configuration

        if not isinstance(
            self.key,
            str,
        ):
            raise TypeError(
                "Menu item key must be a string."
            )

        self.key = (
            self.key.strip()
        )

        if not self.key:
            raise ValueError(
                "Menu item key cannot be empty."
            )

        if not isinstance(
            self.label,
            str,
        ):
            raise TypeError(
                "Menu item label must be a string."
            )

        self.label = (
            self.label.strip()
        )

        if not self.label:
            raise ValueError(
                "Menu item label cannot be empty."
            )

        if self.action is not None:
            if not callable(
                self.action
            ):
                raise TypeError(
                    "Menu item action must be callable."
                )

        if self.command is not None:
            self.command = (
                self.command.strip().lower()
            )

        if self.shortcut is not None:
            self.shortcut = (
                self.shortcut.strip()
            )

    def is_available(
        self,
    ) -> bool:
        # Returns whether the item can be selected

        return (
            self.enabled
            and not self.hidden
        )

    def matches(
        self,
        selection: str,
    ) -> bool:
        # Checks whether user input matches
        # this menu item

        if not isinstance(
            selection,
            str,
        ):
            return False

        normalized = (
            selection.strip().lower()
        )

        candidates = {
            self.key.lower(),
            self.label.lower(),
        }

        if self.shortcut:
            candidates.add(
                self.shortcut.lower()
            )

        return normalized in candidates

    def execute(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        # Executes the item's callback

        if not self.enabled:
            raise MenuSelectionError(
                f"Menu item '{self.key}' is disabled."
            )

        if self.action is None:
            return None

        return self.action(
            *args,
            **kwargs,
        )


# Menu Configuration


@dataclass
class MenuConfig:
    # Controls how a menu is displayed

    title: str = "Cryptography Toolkit"
    subtitle: str | None = None
    width: int = 70
    show_descriptions: bool = True
    show_shortcuts: bool = True
    numbered: bool = True
    allow_exit: bool = True
    exit_key: str = "q"
    clear_screen: bool = False
    prompt: str = "Select an option"

    def __post_init__(
        self,
    ) -> None:
        # Validates menu configuration

        if not isinstance(
            self.title,
            str,
        ):
            raise TypeError(
                "Menu title must be a string."
            )

        if self.subtitle is not None:
            if not isinstance(
                self.subtitle,
                str,
            ):
                raise TypeError(
                    "Menu subtitle must be a string."
                )

        if not isinstance(
            self.width,
            int,
        ):
            raise TypeError(
                "Menu width must be an integer."
            )

        if self.width < 30:
            raise ValueError(
                "Menu width must be at least 30."
            )

        if not isinstance(
            self.exit_key,
            str,
        ):
            raise TypeError(
                "Exit key must be a string."
            )

        if not self.exit_key.strip():
            raise ValueError(
                "Exit key cannot be empty."
            )

        if not isinstance(
            self.prompt,
            str,
        ):
            raise TypeError(
                "Menu prompt must be a string."
            )


# Menu Manager


class MenuManager:
    # Manages menu items, rendering,
    # selection, and execution

    def __init__(
        self,
        *,
        config: MenuConfig | None = None,
        input_function: Callable[
            [str],
            str,
        ] = input,
        output_function: Callable[
            [str],
            Any,
        ] = print,
    ) -> None:
        # Initializes the menu manager

        self.config = (
            config
            if config is not None
            else MenuConfig()
        )

        if not callable(
            input_function
        ):
            raise TypeError(
                "input_function must be callable."
            )

        if not callable(
            output_function
        ):
            raise TypeError(
                "output_function must be callable."
            )

        self.input_function = (
            input_function
        )

        self.output_function = (
            output_function
        )

        self._items: list[
            MenuItem
        ] = []

        self._running = False

        self._selection_history: list[
            str
        ] = []

    # Item Registration

    def add_item(
        self,
        item: MenuItem,
    ) -> None:
        # Adds an item to the menu

        if not isinstance(
            item,
            MenuItem,
        ):
            raise TypeError(
                "item must be a MenuItem."
            )

        if any(
            existing.key.lower()
            == item.key.lower()
            for existing in self._items
        ):
            raise MenuConfigurationError(
                f"Duplicate menu key: {item.key}"
            )

        self._items.append(
            item
        )

    def add(
        self,
        key: str,
        label: str,
        *,
        description: str = "",
        action: Callable[
            ...,
            Any,
        ] | None = None,
        command: str | None = None,
        enabled: bool = True,
        hidden: bool = False,
        shortcut: str | None = None,
        metadata: Mapping[
            str,
            Any,
        ] | None = None,
    ) -> MenuItem:
        # Creates and adds a menu item

        item = MenuItem(
            key=key,
            label=label,
            description=description,
            action=action,
            command=command,
            enabled=enabled,
            hidden=hidden,
            shortcut=shortcut,
            metadata=dict(
                metadata or {}
            ),
        )

        self.add_item(
            item
        )

        return item

    def remove_item(
        self,
        key: str,
    ) -> MenuItem:
        # Removes and returns a menu item

        item = self.get_item(
            key
        )

        self._items.remove(
            item
        )

        return item

    def clear_items(
        self,
    ) -> None:
        # Removes every menu item

        self._items.clear()

    # Item Lookup

    def get_item(
        self,
        key: str,
    ) -> MenuItem:
        # Retrieves an item by key

        if not isinstance(
            key,
            str,
        ):
            raise TypeError(
                "Menu item key must be a string."
            )

        normalized = (
            key.strip().lower()
        )

        for item in self._items:
            if (
                item.key.lower()
                == normalized
            ):
                return item

        raise MenuSelectionError(
            f"Unknown menu item: {key}"
        )

    def find_selection(
        self,
        selection: str,
    ) -> MenuItem | None:
        # Finds an item matching user input

        if not isinstance(
            selection,
            str,
        ):
            return None

        normalized = (
            selection.strip().lower()
        )

        for item in self.available_items():
            if item.matches(
                normalized
            ):
                return item

        return None

    def has_item(
        self,
        key: str,
    ) -> bool:
        # Checks whether an item exists

        try:
            self.get_item(
                key
            )

            return True

        except MenuSelectionError:
            return False

    # Item Listing

    def items(
        self,
        *,
        include_hidden: bool = False,
    ) -> list[MenuItem]:
        # Returns menu items

        if include_hidden:
            return list(
                self._items
            )

        return [
            item
            for item in self._items
            if not item.hidden
        ]

    def available_items(
        self,
    ) -> list[MenuItem]:
        # Returns selectable menu items

        return [
            item
            for item in self._items
            if item.is_available()
        ]

    def enabled_items(
        self,
    ) -> list[MenuItem]:
        # Returns enabled menu items,
        # including hidden ones

        return [
            item
            for item in self._items
            if item.enabled
        ]

    def __len__(
        self,
    ) -> int:
        # Returns number of registered items

        return len(
            self._items
        )

    # Selection History

    def record_selection(
        self,
        key: str,
    ) -> None:
        # Records a menu selection

        if not isinstance(
            key,
            str,
        ):
            raise TypeError(
                "Selection key must be a string."
            )

        self._selection_history.append(
            key
        )

    def selection_history(
        self,
    ) -> list[str]:
        # Returns a copy of selection history

        return list(
            self._selection_history
        )

    def clear_selection_history(
        self,
    ) -> None:
        # Clears selection history

        self._selection_history.clear()

    # State

    @property
    def running(
        self,
    ) -> bool:
        # Returns whether the menu is active

        return self._running

    def stop(
        self,
    ) -> None:
        # Stops the current menu loop

        self._running = False

    # Rendering

    def _separator(
        self,
        character: str = "=",
    ) -> str:
        # Creates a horizontal separator

        if not character:
            character = "="

        return character * self.config.width

    def _render_header(
        self,
    ) -> list[str]:
        # Renders the menu header

        lines = [
            self._separator(),
            self.config.title.center(
                self.config.width
            ),
            self._separator(),
        ]

        if self.config.subtitle:
            lines.extend(
                [
                    self.config.subtitle.center(
                        self.config.width
                    ),
                    self._separator("-"),
                ]
            )

        return lines

    def _render_item(
        self,
        item: MenuItem,
        index: int,
    ) -> str:
        # Renders one menu item

        prefix = (
            f"{index}. "
            if self.config.numbered
            else ""
        )

        shortcut = ""

        if (
            self.config.show_shortcuts
            and item.shortcut
        ):
            shortcut = (
                f" [{item.shortcut}]"
            )

        line = (
            f"{prefix}"
            f"{item.label}"
            f"{shortcut}"
        )

        if (
            self.config.show_descriptions
            and item.description
        ):
            line += (
                f" - {item.description}"
            )

        return line

    def render(
        self,
    ) -> str:
        # Renders the complete menu

        lines = self._render_header()

        lines.append("")

        available = (
            self.available_items()
        )

        for index, item in enumerate(
            available,
            start=1,
        ):
            lines.append(
                self._render_item(
                    item,
                    index,
                )
            )

        if self.config.allow_exit:
            lines.extend(
                [
                    "",
                    self._separator("-"),
                    (
                        f"Q. Exit"
                        f" [{self.config.exit_key}]"
                    ),
                ]
            )

        return "\n".join(
            lines
        )

    def display(
        self,
    ) -> None:
        # Displays the rendered menu

        self.output_function(
            self.render()
        )

        # Selection

    def normalize_selection(
        self,
        selection: str,
    ) -> str:
        # Normalizes user menu input

        if not isinstance(
            selection,
            str,
        ):
            raise TypeError(
                "Menu selection must be a string."
            )

        return selection.strip().lower()

    def select(
        self,
        selection: str,
    ) -> MenuItem:
        # Resolves a user selection to a menu item

        normalized = (
            self.normalize_selection(
                selection
            )
        )

        if (
            self.config.allow_exit
            and normalized
            == self.config.exit_key.lower()
        ):
            raise MenuExitRequested()

        # Support numeric menu selection

        if (
            self.config.numbered
            and normalized.isdigit()
        ):
            index = int(
                normalized
            )

            available = (
                self.available_items()
            )

            if (
                index < 1
                or index > len(
                    available
                )
            ):
                raise MenuSelectionError(
                    f"Invalid menu selection: "
                    f"{selection}"
                )

            item = available[
                index - 1
            ]

            self.record_selection(
                item.key
            )

            return item

        item = self.find_selection(
            normalized
        )

        if item is None:
            raise MenuSelectionError(
                f"Invalid menu selection: "
                f"{selection}"
            )

        if not item.enabled:
            raise MenuSelectionError(
                f"Menu item '{item.key}' "
                "is disabled."
            )

        self.record_selection(
            item.key
        )

        return item

    # Execution

    def execute_item(
        self,
        item: MenuItem,
        *args: Any,
        **kwargs: Any,
    ) -> MenuResult:
        # Executes a selected menu item

        if not isinstance(
            item,
            MenuItem,
        ):
            raise TypeError(
                "item must be a MenuItem."
            )

        if not item.enabled:
            return MenuResult.failure(
                f"Menu item '{item.key}' "
                "is disabled."
            )

        try:
            value = item.execute(
                *args,
                **kwargs,
            )

        except MenuError:
            raise

        except Exception as error:
            return MenuResult.failure(
                (
                    f"Menu item '{item.key}' "
                    f"failed: {error}"
                )
            )

        if isinstance(
            value,
            MenuResult,
        ):
            return value

        return MenuResult.ok(
            value=value,
            command=item.command,
        )

    def execute_selection(
        self,
        selection: str,
        *args: Any,
        **kwargs: Any,
    ) -> MenuResult:
        # Resolves and executes a selection

        try:
            item = self.select(
                selection
            )

        except MenuExitRequested:
            return MenuResult.exit()

        return self.execute_item(
            item,
            *args,
            **kwargs,
        )

    # Input

    def prompt(
        self,
    ) -> str:
        # Prompts the user for a menu selection

        prompt_text = (
            f"{self.config.prompt}: "
        )

        return self.input_function(
            prompt_text
        )

    def get_selection(
        self,
    ) -> MenuItem | None:
        # Prompts for and resolves a selection

        selection = self.prompt()

        try:
            return self.select(
                selection
            )

        except MenuExitRequested:
            return None

        except MenuSelectionError as error:
            self.output_function(
                f"Error: {error}"
            )

            return None

    # Menu Loop

    def run_once(
        self,
        *,
        clear_screen: bool | None = None,
    ) -> MenuResult:
        # Displays the menu, reads one selection,
        # and executes it

        should_clear = (
            self.config.clear_screen
            if clear_screen is None
            else clear_screen
        )

        if should_clear:
            self._clear_screen()

        self.display()

        selection = self.prompt()

        try:
            item = self.select(
                selection
            )

        except MenuExitRequested:
            self.stop()

            return MenuResult.exit(
                message="Exiting menu."
            )

        except MenuSelectionError as error:
            result = MenuResult.failure(
                str(error)
            )

            self.output_function(
                f"Error: {result.message}"
            )

            return result

        result = self.execute_item(
            item
        )

        if result.message:
            self.output_function(
                result.message
            )

        if result.exit_menu:
            self.stop()

        return result

    def run(
        self,
        *,
        clear_screen: bool | None = None,
        max_iterations: int | None = None,
    ) -> MenuResult:
        # Runs the interactive menu loop

        if (
            max_iterations is not None
            and (
                not isinstance(
                    max_iterations,
                    int,
                )
                or max_iterations < 1
            )
        ):
            raise ValueError(
                "max_iterations must be a "
                "positive integer or None."
            )

        self._running = True

        iterations = 0
        last_result = MenuResult.ok()

        try:
            while self._running:

                if (
                    max_iterations is not None
                    and iterations
                    >= max_iterations
                ):
                    break

                iterations += 1

                last_result = self.run_once(
                    clear_screen=clear_screen
                )

                if last_result.exit_menu:
                    break

        except (
            KeyboardInterrupt,
        ):
            self.stop()

            return MenuResult.exit(
                message="Menu interrupted."
            )

        finally:
            self._running = False

        return last_result

    # Screen Utilities

    def _clear_screen(
        self,
    ) -> None:
        # Clears the terminal screen

        import os

        command = (
            "cls"
            if os.name == "nt"
            else "clear"
        )

        os.system(
            command
        )

    # Command Integration

    def add_command(
        self,
        key: str,
        label: str,
        command: str,
        *,
        description: str = "",
        command_manager: Any = None,
        options: Mapping[
            str,
            Any,
        ] | None = None,
        args: Sequence[
            Any,
        ] = (),
        input_text: str | None = None,
        output_path: str | None = None,
        shortcut: str | None = None,
        enabled: bool = True,
        hidden: bool = False,
    ) -> MenuItem:
        # Adds a menu item connected to the CLI
        # command manager

        if not isinstance(
            command,
            str,
        ):
            raise TypeError(
                "command must be a string."
            )

        command = (
            command.strip().lower()
        )

        if not command:
            raise ValueError(
                "command cannot be empty."
            )

        if command_manager is None:
            try:
                from .commands import (
                    get_command_manager,
                )

                command_manager = (
                    get_command_manager()
                )

            except ImportError as error:
                raise MenuConfigurationError(
                    "Unable to load command manager."
                ) from error

        def command_action() -> Any:
            # Executes the associated command

            result = (
                command_manager.execute_safe(
                    command,
                    args=args,
                    options=options,
                    input_text=input_text,
                    output_path=output_path,
                    interactive=True,
                )
            )

            if not result.success:
                self.output_function(
                    result.message
                )

            elif result.message:
                self.output_function(
                    result.message
                )

            return result

        return self.add(
            key=key,
            label=label,
            description=description,
            action=command_action,
            command=command,
            shortcut=shortcut,
            enabled=enabled,
            hidden=hidden,
        )

    def add_commands(
        self,
        commands: Iterable[
            Mapping[str, Any]
        ],
        *,
        command_manager: Any = None,
    ) -> list[MenuItem]:
        # Adds multiple command-backed menu items

        items = []

        for specification in commands:

            if not isinstance(
                specification,
                Mapping,
            ):
                raise TypeError(
                    "Each command specification "
                    "must be a mapping."
                )

            required = {
                "key",
                "label",
                "command",
            }

            missing = (
                required
                - set(
                    specification.keys()
                )
            )

            if missing:
                raise MenuConfigurationError(
                    "Missing command specification "
                    f"fields: {sorted(missing)}"
                )

            item = self.add_command(
                command_manager=command_manager,
                **dict(
                    specification
                ),
            )

            items.append(
                item
            )

        return items

    # Menu State

    def enable(
        self,
        key: str,
    ) -> None:
        # Enables a menu item

        item = self.get_item(
            key
        )

        item.enabled = True

    def disable(
        self,
        key: str,
    ) -> None:
        # Disables a menu item

        item = self.get_item(
            key
        )

        item.enabled = False

    def show(
        self,
        key: str,
    ) -> None:
        # Makes a menu item visible

        item = self.get_item(
            key
        )

        item.hidden = False

    def hide(
        self,
        key: str,
    ) -> None:
        # Hides a menu item

        item = self.get_item(
            key
        )

        item.hidden = True

    def toggle(
        self,
        key: str,
    ) -> bool:
        # Toggles the enabled state of an item

        item = self.get_item(
            key
        )

        item.enabled = not item.enabled

        return item.enabled

    # Configuration

    def configure(
        self,
        **settings: Any,
    ) -> None:
        # Updates menu configuration

        valid_fields = {
            "title",
            "subtitle",
            "width",
            "show_descriptions",
            "show_shortcuts",
            "numbered",
            "allow_exit",
            "exit_key",
            "clear_screen",
            "prompt",
        }

        unknown = (
            set(settings)
            - valid_fields
        )

        if unknown:
            raise MenuConfigurationError(
                "Unknown menu configuration "
                f"options: {sorted(unknown)}"
            )

        values = {
            field_name: getattr(
                self.config,
                field_name,
            )
            for field_name in valid_fields
        }

        values.update(
            settings
        )

        self.config = MenuConfig(
            **values
        )

    def reset(
        self,
    ) -> None:
        # Resets the menu to an empty default state

        self.stop()
        self.clear_items()
        self.clear_selection_history()
        self.config = MenuConfig()

    # Information

    def item_count(
        self,
        *,
        include_hidden: bool = False,
    ) -> int:
        # Returns the number of menu items

        return len(
            self.items(
                include_hidden=include_hidden
            )
        )

    def available_count(
        self,
    ) -> int:
        # Returns the number of selectable items

        return len(
            self.available_items()
        )

    def summary(
        self,
    ) -> dict[str, Any]:
        # Returns structured menu information

        return {
            "title": self.config.title,
            "items": self.item_count(
                include_hidden=True
            ),
            "visible_items": self.item_count(),
            "available_items": self.available_count(),
            "running": self.running,
            "selection_count": len(
                self._selection_history
            ),
        }  

    # menu.py — Part 3
# Continued from Part 2


# Menu Factory Functions


def create_menu(
    title: str = "Cryptography Toolkit",
    *,
    subtitle: str | None = None,
    width: int = 70,
    show_descriptions: bool = True,
    show_shortcuts: bool = True,
    numbered: bool = True,
    allow_exit: bool = True,
    exit_key: str = "q",
    clear_screen: bool = False,
    prompt: str = "Select an option",
) -> MenuManager:
    # Creates and returns a configured menu manager

    config = MenuConfig(
        title=title,
        subtitle=subtitle,
        width=width,
        show_descriptions=show_descriptions,
        show_shortcuts=show_shortcuts,
        numbered=numbered,
        allow_exit=allow_exit,
        exit_key=exit_key,
        clear_screen=clear_screen,
        prompt=prompt,
    )

    return MenuManager(
        config=config
    )


def create_main_menu(
    *,
    command_manager: Any = None,
) -> MenuManager:
    # Creates the main Cryptography Toolkit menu

    menu = create_menu(
        title="Caesar Cipher Toolkit",
        subtitle=(
            "Cryptography and Cryptanalysis"
        ),
    )

    menu.add_command(
        key="encrypt",
        label="Encrypt Text",
        command="encrypt",
        description=(
            "Encrypt plaintext using a "
            "Caesar Cipher."
        ),
        command_manager=command_manager,
        shortcut="E",
    )

    menu.add_command(
        key="decrypt",
        label="Decrypt Text",
        command="decrypt",
        description=(
            "Decrypt ciphertext using a "
            "Caesar Cipher."
        ),
        command_manager=command_manager,
        shortcut="D",
    )

    menu.add_command(
        key="analyze",
        label="Cryptanalysis",
        command="analyze",
        description=(
            "Analyze text using multiple "
            "cryptanalysis techniques."
        ),
        command_manager=command_manager,
        shortcut="A",
    )

    menu.add_command(
        key="bruteforce",
        label="Brute-Force Caesar Cipher",
        command="bruteforce",
        description=(
            "Automatically test possible "
            "Caesar Cipher keys."
        ),
        command_manager=command_manager,
        shortcut="B",
    )

    menu.add_command(
        key="frequency",
        label="Frequency Analysis",
        command="frequency",
        description=(
            "Analyze letter-frequency patterns."
        ),
        command_manager=command_manager,
        shortcut="F",
    )

    menu.add_command(
        key="entropy",
        label="Entropy Analysis",
        command="entropy",
        description=(
            "Calculate Shannon entropy."
        ),
        command_manager=command_manager,
        shortcut="H",
    )

    menu.add_command(
        key="ioc",
        label="Index of Coincidence",
        command="ioc",
        description=(
            "Calculate the Index of Coincidence."
        ),
        command_manager=command_manager,
        shortcut="I",
    )

    menu.add_command(
        key="ngrams",
        label="N-Gram Analysis",
        command="ngrams",
        description=(
            "Analyze common character sequences."
        ),
        command_manager=command_manager,
        shortcut="N",
    )

    menu.add_command(
        key="history",
        label="History",
        command="history",
        description=(
            "View previous toolkit operations."
        ),
        command_manager=command_manager,
        shortcut="Y",
    )

    menu.add_command(
        key="export",
        label="Export Report",
        command="export",
        description=(
            "Export analysis results and reports."
        ),
        command_manager=command_manager,
        shortcut="X",
    )

    menu.add_command(
        key="backup",
        label="Manage Backups",
        command="backup",
        description=(
            "Create and restore file backups."
        ),
        command_manager=command_manager,
        shortcut="U",
    )

    menu.add_command(
        key="version",
        label="Version Information",
        command="version",
        description=(
            "Display toolkit version information."
        ),
        command_manager=command_manager,
        shortcut="V",
    )

    return menu


# Menu Dispatch Helpers


def run_menu(
    menu: MenuManager,
    *,
    clear_screen: bool | None = None,
    max_iterations: int | None = None,
) -> MenuResult:
    # Runs an existing menu

    if not isinstance(
        menu,
        MenuManager,
    ):
        raise TypeError(
            "menu must be a MenuManager."
        )

    return menu.run(
        clear_screen=clear_screen,
        max_iterations=max_iterations,
    )


def run_main_menu(
    *,
    command_manager: Any = None,
    clear_screen: bool | None = None,
    max_iterations: int | None = None,
) -> MenuResult:
    # Creates and runs the main toolkit menu

    menu = create_main_menu(
        command_manager=command_manager
    )

    return menu.run(
        clear_screen=clear_screen,
        max_iterations=max_iterations,
    )


# Default Menu Manager


_default_menu = create_main_menu()


def get_menu() -> MenuManager:
    # Returns the default menu manager

    return _default_menu


def set_menu(
    menu: MenuManager,
) -> None:
    # Replaces the default menu manager

    global _default_menu

    if not isinstance(
        menu,
        MenuManager,
    ):
        raise TypeError(
            "menu must be a MenuManager."
        )

    _default_menu = menu


# Convenience Functions


def add_menu_item(
    key: str,
    label: str,
    *,
    description: str = "",
    action: Callable[
        ...,
        Any,
    ] | None = None,
    command: str | None = None,
    enabled: bool = True,
    hidden: bool = False,
    shortcut: str | None = None,
    metadata: Mapping[
        str,
        Any,
    ] | None = None,
) -> MenuItem:
    # Adds an item to the default menu

    return _default_menu.add(
        key=key,
        label=label,
        description=description,
        action=action,
        command=command,
        enabled=enabled,
        hidden=hidden,
        shortcut=shortcut,
        metadata=metadata,
    )


def remove_menu_item(
    key: str,
) -> MenuItem:
    # Removes an item from the default menu

    return _default_menu.remove_item(
        key
    )


def get_menu_item(
    key: str,
) -> MenuItem:
    # Retrieves an item from the default menu

    return _default_menu.get_item(
        key
    )


def list_menu_items(
    *,
    include_hidden: bool = False,
) -> list[MenuItem]:
    # Returns items from the default menu

    return _default_menu.items(
        include_hidden=include_hidden
    )


def display_menu() -> None:
    # Displays the default menu

    _default_menu.display()


def execute_menu_selection(
    selection: str,
    *args: Any,
    **kwargs: Any,
) -> MenuResult:
    # Executes a selection from the default menu

    return _default_menu.execute_selection(
        selection,
        *args,
        **kwargs,
    )


# Menu Presets


def create_analysis_menu(
    *,
    command_manager: Any = None,
) -> MenuManager:
    # Creates a menu specifically for
    # cryptanalysis operations

    menu = create_menu(
        title="Cryptanalysis",
        subtitle=(
            "Analyze encrypted and plaintext "
            "messages"
        ),
    )

    menu.add_command(
        key="frequency",
        label="Frequency Analysis",
        command="frequency",
        description=(
            "Analyze letter-frequency distribution."
        ),
        command_manager=command_manager,
        shortcut="F",
    )

    menu.add_command(
        key="entropy",
        label="Shannon Entropy",
        command="entropy",
        description=(
            "Measure the information density "
            "of the supplied text."
        ),
        command_manager=command_manager,
        shortcut="E",
    )

    menu.add_command(
        key="ioc",
        label="Index of Coincidence",
        command="ioc",
        description=(
            "Measure character coincidence "
            "patterns."
        ),
        command_manager=command_manager,
        shortcut="I",
    )

    menu.add_command(
        key="ngrams",
        label="N-Gram Analysis",
        command="ngrams",
        description=(
            "Analyze common bigrams, trigrams, "
            "and other n-grams."
        ),
        command_manager=command_manager,
        shortcut="N",
    )

    menu.add_command(
        key="bruteforce",
        label="Brute-Force Cracking",
        command="bruteforce",
        description=(
            "Test possible Caesar Cipher keys "
            "automatically."
        ),
        command_manager=command_manager,
        shortcut="B",
    )

    return menu


def create_file_menu(
    *,
    command_manager: Any = None,
) -> MenuManager:
    # Creates a menu for file-related operations

    menu = create_menu(
        title="File Operations",
        subtitle=(
            "Manage encrypted files and reports"
        ),
    )

    menu.add_command(
        key="encrypt",
        label="Encrypt File",
        command="encrypt",
        description=(
            "Encrypt text from a file."
        ),
        command_manager=command_manager,
        shortcut="E",
    )

    menu.add_command(
        key="decrypt",
        label="Decrypt File",
        command="decrypt",
        description=(
            "Decrypt ciphertext from a file."
        ),
        command_manager=command_manager,
        shortcut="D",
    )

    menu.add_command(
        key="export",
        label="Export Report",
        command="export",
        description=(
            "Export analysis data to a report."
        ),
        command_manager=command_manager,
        shortcut="X",
    )

    menu.add_command(
        key="backup",
        label="Backups",
        command="backup",
        description=(
            "Create, restore, and manage backups."
        ),
        command_manager=command_manager,
        shortcut="B",
    )

    menu.add_command(
        key="history",
        label="History",
        command="history",
        description=(
            "View previous file operations."
        ),
        command_manager=command_manager,
        shortcut="H",
    )

    return menu


# Menu Validation


def validate_menu(
    menu: MenuManager,
) -> bool:
    # Validates the basic structure of a menu

    if not isinstance(
        menu,
        MenuManager,
    ):
        return False

    try:
        items = menu.items(
            include_hidden=True
        )

        keys: set[str] = set()

        for item in items:

            if not isinstance(
                item,
                MenuItem,
            ):
                return False

            normalized = (
                item.key.lower()
            )

            if normalized in keys:
                return False

            keys.add(
                normalized
            )

            if not item.label:
                return False

        if menu.config.width < 30:
            return False

        return True

    except (
        TypeError,
        ValueError,
        MenuError,
    ):
        return False


# Self-Test


def self_test() -> bool:
    # Runs non-interactive menu system tests

    try:
        calls: list[str] = []

        def test_action() -> str:
            calls.append(
                "executed"
            )

            return "success"

        menu = create_menu(
            title="Test Menu"
        )

        menu.add(
            key="test",
            label="Test Item",
            description=(
                "Test menu item."
            ),
            action=test_action,
            shortcut="T",
        )

        if menu.item_count() != 1:
            return False

        if not menu.has_item(
            "test"
        ):
            return False

        item = menu.select(
            "test"
        )

        if item.key != "test":
            return False

        result = menu.execute_item(
            item
        )

        if not result.success:
            return False

        if result.value != "success":
            return False

        if calls != [
            "executed"
        ]:
            return False

        numeric_item = menu.select(
            "1"
        )

        if numeric_item.key != "test":
            return False

        if not validate_menu(
            menu
        ):
            return False

        menu.disable(
            "test"
        )

        if menu.available_count() != 0:
            return False

        menu.enable(
            "test"
        )

        if menu.available_count() != 1:
            return False

        menu.hide(
            "test"
        )

        if menu.item_count() != 0:
            return False

        menu.show(
            "test"
        )

        if menu.item_count() != 1:
            return False

        return True

    except (
        MenuError,
        TypeError,
        ValueError,
    ):
        return False


# Module Exports


__all__ = [
    # Exceptions
    "MenuError",
    "MenuSelectionError",
    "MenuExitRequested",
    "MenuConfigurationError",

    # Models
    "MenuResult",
    "MenuItem",
    "MenuConfig",

    # Manager
    "MenuManager",

    # Factories
    "create_menu",
    "create_main_menu",
    "create_analysis_menu",
    "create_file_menu",

    # Execution
    "run_menu",
    "run_main_menu",

    # Default Menu
    "get_menu",
    "set_menu",

    # Convenience
    "add_menu_item",
    "remove_menu_item",
    "get_menu_item",
    "list_menu_items",
    "display_menu",
    "execute_menu_selection",

    # Validation
    "validate_menu",

    # Testing
    "self_test",
]

