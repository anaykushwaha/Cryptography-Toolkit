# windows.py
# Application windows for the Cryptography Toolkit GUI
#
# Provides the main application window, secondary windows,
# window configuration, lifecycle management, navigation,
# and shared window utilities.


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # pragma: no cover
    tk = None
    ttk = None


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class WindowError(Exception):
    """Base exception for GUI window errors."""

    pass


class WindowConfigurationError(WindowError):
    """Raised when a window is configured incorrectly."""

    pass


class WindowStateError(WindowError):
    """Raised when a window is used in an invalid state."""

    pass


class WindowNavigationError(WindowError):
    """Raised when window navigation fails."""

    pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


DEFAULT_WINDOW_WIDTH = 1000
DEFAULT_WINDOW_HEIGHT = 700

MIN_WINDOW_WIDTH = 700
MIN_WINDOW_HEIGHT = 500

WINDOW_MAIN = "main"
WINDOW_SETTINGS = "settings"
WINDOW_ABOUT = "about"
WINDOW_HELP = "help"
WINDOW_HISTORY = "history"
WINDOW_ANALYSIS = "analysis"

STATE_CREATED = "created"
STATE_VISIBLE = "visible"
STATE_HIDDEN = "hidden"
STATE_CLOSED = "closed"

DEFAULT_WINDOW_TITLE = "Cryptography Toolkit"


# ---------------------------------------------------------------------------
# Window Configuration
# ---------------------------------------------------------------------------


@dataclass
class WindowConfig:
    """
    Shared configuration for application windows.
    """

    title: str = DEFAULT_WINDOW_TITLE

    width: int = DEFAULT_WINDOW_WIDTH
    height: int = DEFAULT_WINDOW_HEIGHT

    min_width: int = MIN_WINDOW_WIDTH
    min_height: int = MIN_WINDOW_HEIGHT

    resizable: bool = True

    center: bool = True

    maximized: bool = False

    fullscreen: bool = False

    background: str | None = None

    icon_path: str | None = None

    transient: bool = False

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """Validate window configuration."""

        if not isinstance(
            self.title,
            str,
        ):
            raise TypeError(
                "title must be a string."
            )

        if not self.title.strip():
            raise ValueError(
                "title cannot be empty."
            )

        if self.width <= 0:
            raise ValueError(
                "width must be greater than zero."
            )

        if self.height <= 0:
            raise ValueError(
                "height must be greater than zero."
            )

        if self.min_width <= 0:
            raise ValueError(
                "min_width must be greater than zero."
            )

        if self.min_height <= 0:
            raise ValueError(
                "min_height must be greater than zero."
            )

        if self.width < self.min_width:
            raise ValueError(
                "width cannot be smaller than min_width."
            )

        if self.height < self.min_height:
            raise ValueError(
                "height cannot be smaller than min_height."
            )


# ---------------------------------------------------------------------------
# Window State
# ---------------------------------------------------------------------------


@dataclass
class WindowState:
    """
    Runtime state information for an application window.
    """

    name: str

    state: str = STATE_CREATED

    visible: bool = False

    focused: bool = False

    maximized: bool = False

    fullscreen: bool = False

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def is_open(self) -> bool:
        """Return whether the window is currently open."""

        return self.state != STATE_CLOSED

    def is_visible(self) -> bool:
        """Return whether the window is visible."""

        return self.visible

    def is_closed(self) -> bool:
        """Return whether the window is closed."""

        return self.state == STATE_CLOSED


# ---------------------------------------------------------------------------
# Window Manager
# ---------------------------------------------------------------------------


class WindowManager:
    """
    Manages application windows and navigation.

    The manager keeps track of registered windows,
    their instances, and their runtime states.
    """

    def __init__(
        self,
        root: Any = None,
    ) -> None:
        """Initialize the window manager."""

        self.root = root

        self._windows: dict[
            str,
            type[BaseWindow],
        ] = {}

        self._instances: dict[
            str,
            BaseWindow,
        ] = {}

        self._states: dict[
            str,
            WindowState,
        ] = {}

        self._current: str | None = None

        self._callbacks: dict[
            str,
            list[Callable[..., Any]],
        ] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        name: str,
        window_class: type["BaseWindow"],
    ) -> None:
        """
        Register a window class.

        Raises
        ------
        WindowConfigurationError
            If the name or class is invalid.
        """

        self._validate_name(
            name
        )

        if not isinstance(
            window_class,
            type,
        ):
            raise WindowConfigurationError(
                "window_class must be a class."
            )

        if not issubclass(
            window_class,
            BaseWindow,
        ):
            raise WindowConfigurationError(
                "window_class must inherit from BaseWindow."
            )

        self._windows[name] = window_class

        self._states.setdefault(
            name,
            WindowState(
                name=name
            ),
        )

    def unregister(
        self,
        name: str,
    ) -> None:
        """Unregister a window."""

        if name in self._instances:
            self.close(
                name
            )

        self._windows.pop(
            name,
            None,
        )

        self._states.pop(
            name,
            None,
        )

    def is_registered(
        self,
        name: str,
    ) -> bool:
        """Return whether a window is registered."""

        return name in self._windows

    def registered_windows(self) -> tuple[str, ...]:
        """Return all registered window names."""

        return tuple(
            self._windows.keys()
        )

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    def create(
        self,
        name: str,
        **kwargs: Any,
    ) -> "BaseWindow":
        """
        Create an instance of a registered window.
        """

        if not self.is_registered(name):
            raise WindowConfigurationError(
                f"Window '{name}' is not registered."
            )

        if name in self._instances:
            return self._instances[name]

        window_class = self._windows[name]

        instance = window_class(
            self.root,
            manager=self,
            **kwargs,
        )

        self._instances[name] = instance

        self._states[name] = instance.state

        self.emit(
            "created",
            instance,
        )

        return instance

    # ------------------------------------------------------------------
    # Showing
    # ------------------------------------------------------------------

    def show(
        self,
        name: str,
        **kwargs: Any,
    ) -> "BaseWindow":
        """
        Create and display a window.
        """

        instance = self.create(
            name,
            **kwargs,
        )

        instance.show()

        self._current = name

        self.emit(
            "shown",
            instance,
        )

        return instance

    def hide(
        self,
        name: str,
    ) -> None:
        """Hide a registered window."""

        instance = self.get(
            name
        )

        instance.hide()

        if self._current == name:
            self._current = None

        self.emit(
            "hidden",
            instance,
        )

    def close(
        self,
        name: str,
    ) -> None:
        """Close a registered window."""

        instance = self._instances.get(
            name
        )

        if instance is None:
            return

        instance.close()

        self._instances.pop(
            name,
            None,
        )

        if self._current == name:
            self._current = None

        self.emit(
            "closed",
            instance,
        )

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> "BaseWindow":
        """Return an active window instance."""

        instance = self._instances.get(
            name
        )

        if instance is None:
            raise WindowStateError(
                f"Window '{name}' is not active."
            )

        return instance

    def get_state(
        self,
        name: str,
    ) -> WindowState:
        """Return the state of a registered window."""

        if name not in self._states:
            raise WindowStateError(
                f"Unknown window: {name}"
            )

        return self._states[name]

    @property
    def current(self) -> str | None:
        """Return the name of the current window."""

        return self._current

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(
        self,
        name: str,
        **kwargs: Any,
    ) -> "BaseWindow":
        """
        Navigate to another application window.

        The current window is hidden before the target
        window is displayed.
        """

        if not self.is_registered(name):
            raise WindowNavigationError(
                f"Window '{name}' is not registered."
            )

        if self._current is not None:
            if self._current != name:
                try:
                    self.hide(
                        self._current
                    )
                except WindowStateError:
                    pass

        return self.show(
            name,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def bind(
        self,
        event: str,
        callback: Callable[..., Any],
    ) -> None:
        """Register a manager event callback."""

        if not isinstance(
            event,
            str,
        ):
            raise TypeError(
                "event must be a string."
            )

        if not callable(
            callback
        ):
            raise TypeError(
                "callback must be callable."
            )

        self._callbacks.setdefault(
            event,
            [],
        ).append(
            callback
        )

    def emit(
        self,
        event: str,
        *args: Any,
        **kwargs: Any,
    ) -> list[Any]:
        """Emit an event to registered callbacks."""

        results: list[Any] = []

        for callback in self._callbacks.get(
            event,
            [],
        ):
            results.append(
                callback(
                    *args,
                    **kwargs,
                )
            )

        return results

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_name(
        name: str,
    ) -> None:
        """Validate a window name."""

        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "Window name must be a string."
            )

        if not name.strip():
            raise ValueError(
                "Window name cannot be empty."
            )

    def close_all(self) -> None:
        """Close all active windows."""

        for name in tuple(
            self._instances.keys()
        ):
            self.close(
                name
            )

        self._current = None


# ---------------------------------------------------------------------------
# Base Window
# ---------------------------------------------------------------------------


class BaseWindow:
    """
    Base class for all Cryptography Toolkit windows.

    Provides:

    - Window creation
    - Configuration
    - Lifecycle management
    - Centering
    - Resizing
    - Focus handling
    - State tracking
    - Event callbacks
    - Window manager integration
    """

    window_type = WINDOW_MAIN

    def __init__(
        self,
        parent: Any = None,
        *,
        manager: WindowManager | None = None,
        config: WindowConfig | None = None,
    ) -> None:
        """Initialize the base window."""

        self.parent = parent
        self.manager = manager

        self.config = (
            config
            if config is not None
            else WindowConfig()
        )

        self.window: Any = None

        self.state = WindowState(
            name=self.window_type
        )

        self._initialized = False
        self._callbacks: dict[
            str,
            list[Callable[..., Any]],
        ] = {}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def initialized(self) -> bool:
        """Return whether the window has been initialized."""

        return self._initialized

    @property
    def visible(self) -> bool:
        """Return whether the window is visible."""

        return self.state.visible

    @property
    def closed(self) -> bool:
        """Return whether the window is closed."""

        return self.state.is_closed()

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    def build(self) -> Any:
        """
        Build the window.

        Subclasses should extend this method to add
        application-specific content.
        """

        self.require_tkinter()

        if self._initialized:
            return self.window

        if self.parent is None:
            self.window = tk.Tk()
        else:
            self.window = tk.Toplevel(
                self.parent
            )

        self.window.title(
            self.config.title
        )

        self.window.geometry(
            f"{self.config.width}"
            f"x"
            f"{self.config.height}"
        )

        self.window.minsize(
            self.config.min_width,
            self.config.min_height,
        )

        self.window.resizable(
            self.config.resizable,
            self.config.resizable,
        )

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close,
        )

        self._configure_window()

        self._initialized = True

        self.state.state = STATE_CREATED
        self.state.visible = False
        self.state.maximized = (
            self.config.maximized
        )
        self.state.fullscreen = (
            self.config.fullscreen
        )

        self.emit(
            "built",
            self,
        )

        return self.window

    def _configure_window(self) -> None:
        """Apply standard window configuration."""

        if self.window is None:
            return

        if self.config.background is not None:
            try:
                self.window.configure(
                    background=self.config.background
                )
            except tk.TclError:
                pass

        if self.config.transient:
            try:
                self.window.transient(
                    self.parent
                )
            except tk.TclError:
                pass

        if self.config.center:
            self.center()

        if self.config.maximized:
            self.maximize()

        if self.config.fullscreen:
            self.set_fullscreen(
                True
            )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def show(self) -> None:
        """Display the window."""

        if not self._initialized:
            self.build()

        if self.window is None:
            raise WindowStateError(
                "Window could not be created."
            )

        try:
            self.window.deiconify()
            self.window.lift()
        except tk.TclError as error:
            raise WindowStateError(
                "Unable to display window."
            ) from error

        self.state.state = STATE_VISIBLE
        self.state.visible = True

        self.emit(
            "shown",
            self,
        )

    def hide(self) -> None:
        """Hide the window."""

        if self.window is None:
            return

        try:
            self.window.withdraw()
        except tk.TclError:
            return

        self.state.state = STATE_HIDDEN
        self.state.visible = False

        self.emit(
            "hidden",
            self,
        )

    def close(self) -> None:
        """Close and destroy the window."""

        if self.window is None:
            self.state.state = STATE_CLOSED
            self.state.visible = False
            return

        self.emit(
            "before_close",
            self,
        )

        try:
            self.window.destroy()
        except tk.TclError:
            pass

        self.window = None

        self._initialized = False

        self.state.state = STATE_CLOSED
        self.state.visible = False

        self.emit(
            "closed",
            self,
        )

    # ------------------------------------------------------------------
    # Window Controls
    # ------------------------------------------------------------------

    def center(self) -> None:
        """Center the window relative to its parent."""

        if self.window is None:
            return

        try:
            self.window.update_idletasks()

            width = self.window.winfo_width()
            height = self.window.winfo_height()

            if width <= 1:
                width = self.config.width

            if height <= 1:
                height = self.config.height

            if self.parent is not None:
                parent_x = (
                    self.parent.winfo_rootx()
                )

                parent_y = (
                    self.parent.winfo_rooty()
                )

                parent_width = (
                    self.parent.winfo_width()
                )

                parent_height = (
                    self.parent.winfo_height()
                )

                x = (
                    parent_x
                    + (
                        parent_width
                        - width
                    )
                    // 2
                )

                y = (
                    parent_y
                    + (
                        parent_height
                        - height
                    )
                    // 2
                )

            else:
                screen_width = (
                    self.window.winfo_screenwidth()
                )

                screen_height = (
                    self.window.winfo_screenheight()
                )

                x = (
                    screen_width
                    - width
                ) // 2

                y = (
                    screen_height
                    - height
                ) // 2

            self.window.geometry(
                f"{width}x{height}"
                f"+{max(0, x)}"
                f"+{max(0, y)}"
            )

        except tk.TclError:
            pass

    def maximize(self) -> None:
        """Maximize the window."""

        if self.window is None:
            return

        try:
            self.window.state(
                "zoomed"
            )

            self.state.maximized = True

        except tk.TclError:
            pass

    def restore(self) -> None:
        """Restore the window from maximized state."""

        if self.window is None:
            return

        try:
            self.window.state(
                "normal"
            )

            self.state.maximized = False

        except tk.TclError:
            pass

    def minimize(self) -> None:
        """Minimize the window."""

        if self.window is None:
            return

        try:
            self.window.iconify()

        except tk.TclError:
            pass

    def set_fullscreen(
        self,
        enabled: bool,
    ) -> None:
        """Enable or disable fullscreen mode."""

        if self.window is None:
            return

        try:
            self.window.attributes(
                "-fullscreen",
                bool(enabled),
            )

            self.state.fullscreen = bool(
                enabled
            )

        except tk.TclError:
            pass

    def focus(self) -> None:
        """Focus the window."""

        if self.window is None:
            return

        try:
            self.window.focus_force()

            self.state.focused = True

        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def set_size(
        self,
        width: int,
        height: int,
    ) -> None:
        """Set the window size."""

        if width <= 0 or height <= 0:
            raise ValueError(
                "Window dimensions must be positive."
            )

        if self.window is None:
            raise WindowStateError(
                "Window has not been initialized."
            )

        self.window.geometry(
            f"{width}x{height}"
        )

    def get_size(self) -> tuple[int, int]:
        """Return the current window dimensions."""

        if self.window is None:
            raise WindowStateError(
                "Window has not been initialized."
            )

        return (
            self.window.winfo_width(),
            self.window.winfo_height(),
        )

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def bind_event(
        self,
        event: str,
        callback: Callable[..., Any],
    ) -> None:
        """Register a window lifecycle callback."""

        if not isinstance(
            event,
            str,
        ):
            raise TypeError(
                "event must be a string."
            )

        if not callable(
            callback
        ):
            raise TypeError(
                "callback must be callable."
            )

        self._callbacks.setdefault(
            event,
            [],
        ).append(
            callback
        )

    def unbind_event(
        self,
        event: str,
        callback: Callable[..., Any] | None = None,
    ) -> None:
        """Remove a window event callback."""

        if event not in self._callbacks:
            return

        if callback is None:
            self._callbacks.pop(
                event,
                None,
            )

            return

        callbacks = self._callbacks[event]

        if callback in callbacks:
            callbacks.remove(
                callback
            )

        if not callbacks:
            self._callbacks.pop(
                event,
                None,
            )

    def emit(
        self,
        event: str,
        *args: Any,
        **kwargs: Any,
    ) -> list[Any]:
        """Emit a window event."""

        results: list[Any] = []

        for callback in self._callbacks.get(
            event,
            [],
        ):
            results.append(
                callback(
                    *args,
                    **kwargs,
                )
            )

        return results

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def require_tkinter() -> None:
        """Ensure Tkinter is available."""

        if tk is None or ttk is None:
            raise WindowConfigurationError(
                "Tkinter is unavailable."
            )

    def require_initialized(self) -> None:
        """Ensure the window has been initialized."""

        if not self._initialized:
            raise WindowStateError(
                "Window has not been initialized."
            )

    def update(self) -> None:
        """Process pending GUI updates."""

        self.require_initialized()

        try:
            self.window.update_idletasks()
        except tk.TclError:
            pass

    def __enter__(self) -> "BaseWindow":
        """Enter a window context."""

        self.build()

        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:
        """Exit the window context."""

        if not self.closed:
            self.close()

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""

        return (
            f"{self.__class__.__name__}("
            f"initialized={self.initialized}, "
            f"visible={self.visible}, "
            f"closed={self.closed}"
            f")"
        )

    # ---------------------------------------------------------------------------
# Main Application Window
# ---------------------------------------------------------------------------


class MainWindow(BaseWindow):
    """
    Primary application window for the Cryptography Toolkit.

    Provides the main application shell, navigation area,
    content area, status bar, and application-level controls.
    """

    window_type = WINDOW_MAIN

    def __init__(
        self,
        parent: Any = None,
        *,
        manager: WindowManager | None = None,
        title: str = DEFAULT_WINDOW_TITLE,
    ) -> None:
        """Initialize the main application window."""

        config = WindowConfig(
            title=title,
            width=1100,
            height=750,
            min_width=800,
            min_height=550,
        )

        super().__init__(
            parent,
            manager=manager,
            config=config,
        )

        self.main_frame: Any = None
        self.header_frame: Any = None
        self.navigation_frame: Any = None
        self.content_frame: Any = None
        self.status_frame: Any = None

        self.status_label: Any = None
        self.content_title: Any = None

        self.navigation_buttons: dict[
            str,
            Any,
        ] = {}

        self._active_view: str | None = None

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self) -> Any:
        """Build the main application window."""

        window = super().build()

        if ttk is None:
            raise WindowConfigurationError(
                "ttk is unavailable."
            )

        self._build_main_frame()
        self._build_header()
        self._build_navigation()
        self._build_content_area()
        self._build_status_bar()
        self._configure_bindings()

        return window

    def _build_main_frame(self) -> None:
        """Create the root application frame."""

        self.main_frame = ttk.Frame(
            self.window,
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
        )

        self.main_frame.columnconfigure(
            1,
            weight=1,
        )

        self.main_frame.rowconfigure(
            1,
            weight=1,
        )

    def _build_header(self) -> None:
        """Create the application header."""

        self.header_frame = ttk.Frame(
            self.main_frame,
            padding=(20, 15),
        )

        self.header_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
        )

        self.header_frame.columnconfigure(
            0,
            weight=1,
        )

        title_label = ttk.Label(
            self.header_frame,
            text="Cryptography Toolkit",
            font=(
                "TkDefaultFont",
                18,
                "bold",
            ),
        )

        title_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        subtitle_label = ttk.Label(
            self.header_frame,
            text=(
                "Encryption, decryption, "
                "and cryptanalysis tools"
            ),
        )

        subtitle_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(3, 0),
        )

    def _build_navigation(self) -> None:
        """Create the main navigation panel."""

        self.navigation_frame = ttk.Frame(
            self.main_frame,
            padding=(
                10,
                10,
            ),
        )

        self.navigation_frame.grid(
            row=1,
            column=0,
            sticky="ns",
        )

        self._add_navigation_button(
            "encrypt",
            "Encrypt",
            self.show_encrypt_view,
        )

        self._add_navigation_button(
            "decrypt",
            "Decrypt",
            self.show_decrypt_view,
        )

        self._add_navigation_button(
            "analysis",
            "Analysis",
            self.show_analysis_view,
        )

        self._add_navigation_button(
            "history",
            "History",
            self.show_history_view,
        )

        self._add_navigation_button(
            "settings",
            "Settings",
            self.show_settings_view,
        )

        self._add_navigation_button(
            "about",
            "About",
            self.show_about_view,
        )

        separator = ttk.Separator(
            self.navigation_frame,
            orient="horizontal",
        )

        separator.pack(
            fill="x",
            pady=(
                12,
                12,
            ),
        )

        exit_button = ttk.Button(
            self.navigation_frame,
            text="Exit",
            command=self.close,
        )

        exit_button.pack(
            fill="x",
        )

    def _add_navigation_button(
        self,
        name: str,
        text: str,
        command: Callable[[], Any],
    ) -> None:
        """Add a button to the navigation panel."""

        if self.navigation_frame is None:
            return

        button = ttk.Button(
            self.navigation_frame,
            text=text,
            command=command,
        )

        button.pack(
            fill="x",
            pady=(
                3,
                3,
            ),
        )

        self.navigation_buttons[name] = button

    def _build_content_area(self) -> None:
        """Create the main content area."""

        self.content_frame = ttk.Frame(
            self.main_frame,
            padding=20,
        )

        self.content_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
        )

        self.content_frame.columnconfigure(
            0,
            weight=1,
        )

        self.content_frame.rowconfigure(
            1,
            weight=1,
        )

        self.content_title = ttk.Label(
            self.content_frame,
            text="Welcome",
            font=(
                "TkDefaultFont",
                16,
                "bold",
            ),
        )

        self.content_title.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(
                0,
                15,
            ),
        )

        welcome_frame = ttk.Frame(
            self.content_frame,
        )

        welcome_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        welcome_frame.columnconfigure(
            0,
            weight=1,
        )

        welcome_frame.rowconfigure(
            0,
            weight=1,
        )

        welcome_label = ttk.Label(
            welcome_frame,
            text=(
                "Welcome to the "
                "Cryptography Toolkit.\n\n"
                "Select a tool from the navigation "
                "menu to get started."
            ),
            justify="center",
        )

        welcome_label.grid(
            row=0,
            column=0,
        )

    def _build_status_bar(self) -> None:
        """Create the application status bar."""

        self.status_frame = ttk.Frame(
            self.main_frame,
            padding=(
                10,
                5,
            ),
        )

        self.status_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
        )

        self.status_frame.columnconfigure(
            0,
            weight=1,
        )

        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready",
        )

        self.status_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

    def _configure_bindings(self) -> None:
        """Configure application-level keyboard bindings."""

        if self.window is None:
            return

        self.window.bind(
            "<Control-q>",
            self._on_quit_shortcut,
        )

        self.window.bind(
            "<Escape>",
            self._on_escape,
        )

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def show_view(
        self,
        name: str,
        title: str | None = None,
    ) -> None:
        """
        Switch the active content view.

        The actual view implementation can be supplied
        by subclasses or the GUI application controller.
        """

        self._active_view = name

        if title is not None:
            self.set_content_title(
                title
            )
        else:
            self.set_content_title(
                name.replace(
                    "_",
                    " ",
                ).title()
            )

        self.set_status(
            f"Viewing {name.replace('_', ' ')}"
        )

        self.emit(
            "view_changed",
            self,
            name,
        )

    def show_encrypt_view(self) -> None:
        """Display the encryption view."""

        self.show_view(
            "encrypt",
            "Encrypt Message",
        )

    def show_decrypt_view(self) -> None:
        """Display the decryption view."""

        self.show_view(
            "decrypt",
            "Decrypt Message",
        )

    def show_analysis_view(self) -> None:
        """Display the analysis view."""

        self.show_view(
            "analysis",
            "Cryptanalysis",
        )

    def show_history_view(self) -> None:
        """Display the history view."""

        self.show_view(
            "history",
            "Encryption History",
        )

    def show_settings_view(self) -> None:
        """Display the settings view."""

        self.show_view(
            "settings",
            "Settings",
        )

    def show_about_view(self) -> None:
        """Display the about view."""

        self.show_view(
            "about",
            "About Cryptography Toolkit",
        )

    @property
    def active_view(self) -> str | None:
        """Return the currently active view."""

        return self._active_view

    # ------------------------------------------------------------------
    # Content
    # ------------------------------------------------------------------

    def set_content_title(
        self,
        title: str,
    ) -> None:
        """Update the content-area title."""

        if self.content_title is not None:
            self.content_title.configure(
                text=title
            )

    def clear_content(self) -> None:
        """Remove all widgets from the content area."""

        if self.content_frame is None:
            return

        for widget in self.content_frame.winfo_children():
            if widget is not self.content_title:
                widget.destroy()

    def set_content(
        self,
        widget: Any,
    ) -> None:
        """
        Display a widget inside the main content area.
        """

        if self.content_frame is None:
            raise WindowStateError(
                "Content frame has not been initialized."
            )

        self.clear_content()

        widget.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def set_status(
        self,
        message: str,
    ) -> None:
        """Update the status-bar message."""

        if self.status_label is not None:
            self.status_label.configure(
                text=str(message)
            )

    def clear_status(self) -> None:
        """Reset the status bar."""

        self.set_status(
            "Ready"
        )

    # ------------------------------------------------------------------
    # Window Events
    # ------------------------------------------------------------------

    def _on_quit_shortcut(
        self,
        event: Any = None,
    ) -> str:
        """Handle Ctrl+Q."""

        self.close()

        return "break"

    def _on_escape(
        self,
        event: Any = None,
    ) -> str:
        """Handle Escape."""

        return "break"


# ---------------------------------------------------------------------------
# Secondary Window
# ---------------------------------------------------------------------------


class SecondaryWindow(BaseWindow):
    """
    Base class for windows displayed above the main application.
    """

    window_type = "secondary"

    def __init__(
        self,
        parent: Any = None,
        *,
        manager: WindowManager | None = None,
        title: str = DEFAULT_WINDOW_TITLE,
        width: int = 700,
        height: int = 500,
    ) -> None:
        """Initialize a secondary window."""

        config = WindowConfig(
            title=title,
            width=width,
            height=height,
            min_width=500,
            min_height=350,
            transient=True,
        )

        super().__init__(
            parent,
            manager=manager,
            config=config,
        )

    def build(self) -> Any:
        """Build the secondary window."""

        window = super().build()

        self._configure_transient()

        return window

    def _configure_transient(self) -> None:
        """Configure the secondary window as transient."""

        if self.window is None:
            return

        if self.parent is not None:
            try:
                self.window.transient(
                    self.parent
                )
            except tk.TclError:
                pass

    def show(self) -> None:
        """Show and focus the secondary window."""

        super().show()

        self.focus()


# ---------------------------------------------------------------------------
# Settings Window
# ---------------------------------------------------------------------------


class SettingsWindow(SecondaryWindow):
    """
    Application settings window.

    Provides a container for user-configurable
    application preferences.
    """

    window_type = WINDOW_SETTINGS

    def __init__(
        self,
        parent: Any = None,
        *,
        manager: WindowManager | None = None,
    ) -> None:
        """Initialize the settings window."""

        super().__init__(
            parent,
            manager=manager,
            title="Settings",
            width=650,
            height=500,
        )

        self.settings_frame: Any = None
        self.status_label: Any = None

        self.settings: dict[
            str,
            Any,
        ] = {}

    def build(self) -> Any:
        """Build the settings window."""

        window = super().build()

        if ttk is None:
            raise WindowConfigurationError(
                "ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=20,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        container.columnconfigure(
            0,
            weight=1,
        )

        container.rowconfigure(
            1,
            weight=1,
        )

        ttk.Label(
            container,
            text="Application Settings",
            font=(
                "TkDefaultFont",
                16,
                "bold",
            ),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 15),
        )

        self.settings_frame = ttk.Frame(
            container,
        )

        self.settings_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self._build_settings_content()

        button_frame = ttk.Frame(
            container,
        )

        button_frame.grid(
            row=2,
            column=0,
            sticky="e",
            pady=(15, 0),
        )

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.close,
        ).pack(
            side="right",
            padx=(8, 0),
        )

        ttk.Button(
            button_frame,
            text="Save",
            command=self.save_settings,
        ).pack(
            side="right",
        )

        return window

    def _build_settings_content(self) -> None:
        """Build the settings form."""

        if self.settings_frame is None:
            return

        ttk.Label(
            self.settings_frame,
            text=(
                "Settings can be configured "
                "here."
            ),
        ).pack(
            anchor="w",
            pady=5,
        )

        self.status_label = ttk.Label(
            self.settings_frame,
            text="",
        )

        self.status_label.pack(
            anchor="w",
            pady=5,
        )

    def load_settings(
        self,
        settings: dict[str, Any],
    ) -> None:
        """Load settings into the window."""

        self.settings = dict(
            settings
        )

    def save_settings(self) -> None:
        """Save the current settings."""

        self.emit(
            "settings_saved",
            self,
            dict(self.settings),
        )

        if self.status_label is not None:
            self.status_label.configure(
                text="Settings saved."
            )

    # ---------------------------------------------------------------------------
# About Window
# ---------------------------------------------------------------------------


class AboutWindow(SecondaryWindow):
    """
    Displays information about the Cryptography Toolkit.

    Contains the application name, description, version,
    author information, and project details.
    """

    window_type = WINDOW_ABOUT

    def __init__(
        self,
        parent: Any = None,
        *,
        manager: WindowManager | None = None,
        version: str = "1.0.0",
        author: str = "Cryptography Toolkit",
    ) -> None:
        """Initialize the about window."""

        super().__init__(
            parent,
            manager=manager,
            title="About Cryptography Toolkit",
            width=600,
            height=420,
        )

        self.version = version
        self.author = author

    def build(self) -> Any:
        """Build the about window."""

        window = super().build()

        if ttk is None:
            raise WindowConfigurationError(
                "ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=30,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        container.columnconfigure(
            0,
            weight=1,
        )

        ttk.Label(
            container,
            text="Cryptography Toolkit",
            font=(
                "TkDefaultFont",
                22,
                "bold",
            ),
        ).pack(
            pady=(10, 8),
        )

        ttk.Label(
            container,
            text=f"Version {self.version}",
        ).pack(
            pady=(0, 20),
        )

        description = (
            "A modular Python toolkit for "
            "classical encryption, decryption, "
            "cryptanalysis, file processing, "
            "and educational experimentation."
        )

        ttk.Label(
            container,
            text=description,
            justify="center",
            wraplength=480,
        ).pack(
            pady=(0, 20),
        )

        ttk.Label(
            container,
            text=f"Author: {self.author}",
        ).pack(
            pady=(0, 8),
        )

        ttk.Label(
            container,
            text=(
                "Built with Python and Tkinter."
            ),
        ).pack(
            pady=(0, 20),
        )

        ttk.Button(
            container,
            text="Close",
            command=self.close,
        ).pack()

        return window


# ---------------------------------------------------------------------------
# Help Window
# ---------------------------------------------------------------------------


class HelpWindow(SecondaryWindow):
    """
    Displays application help and usage information.
    """

    window_type = WINDOW_HELP

    def __init__(
        self,
        parent: Any = None,
        *,
        manager: WindowManager | None = None,
        title: str = "Help",
    ) -> None:
        """Initialize the help window."""

        super().__init__(
            parent,
            manager=manager,
            title=title,
            width=750,
            height=600,
        )

        self.text_widget: Any = None

    def build(self) -> Any:
        """Build the help window."""

        window = super().build()

        if ttk is None or tk is None:
            raise WindowConfigurationError(
                "Tkinter/ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=20,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        container.columnconfigure(
            0,
            weight=1,
        )

        container.rowconfigure(
            1,
            weight=1,
        )

        ttk.Label(
            container,
            text="Cryptography Toolkit Help",
            font=(
                "TkDefaultFont",
                16,
                "bold",
            ),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 12),
        )

        text_frame = ttk.Frame(
            container,
        )

        text_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        text_frame.columnconfigure(
            0,
            weight=1,
        )

        text_frame.rowconfigure(
            0,
            weight=1,
        )

        self.text_widget = tk.Text(
            text_frame,
            wrap="word",
            state="normal",
        )

        self.text_widget.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.text_widget.yview,
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        self.text_widget.configure(
            yscrollcommand=scrollbar.set
        )

        self.set_help_text(
            self.default_help_text()
        )

        self.text_widget.configure(
            state="disabled"
        )

        ttk.Button(
            container,
            text="Close",
            command=self.close,
        ).grid(
            row=2,
            column=0,
            sticky="e",
            pady=(12, 0),
        )

        return window

    def set_help_text(
        self,
        text: str,
    ) -> None:
        """Replace the displayed help text."""

        if self.text_widget is None:
            return

        self.text_widget.configure(
            state="normal"
        )

        self.text_widget.delete(
            "1.0",
            tk.END,
        )

        self.text_widget.insert(
            "1.0",
            text,
        )

        self.text_widget.configure(
            state="disabled"
        )

    @staticmethod
    def default_help_text() -> str:
        """Return the default application help."""

        return (
            "Cryptography Toolkit Help\n"
            "\n"
            "Encryption\n"
            "----------\n"
            "Use the encryption tools to apply "
            "supported classical ciphers to text "
            "or files.\n"
            "\n"
            "Decryption\n"
            "----------\n"
            "Use the decryption tools to reverse "
            "supported cipher transformations.\n"
            "\n"
            "Analysis\n"
            "--------\n"
            "Use cryptanalysis tools to inspect "
            "ciphertext, frequency distributions, "
            "entropy, and statistical properties.\n"
            "\n"
            "History\n"
            "-------\n"
            "Review previous encryption and "
            "decryption operations.\n"
            "\n"
            "Files\n"
            "-----\n"
            "The toolkit supports reading, writing, "
            "exporting, and backing up files.\n"
            "\n"
            "Keyboard Shortcuts\n"
            "------------------\n"
            "Ctrl+Q   Exit the application\n"
            "Escape   Cancel or close the active view\n"
        )


# ---------------------------------------------------------------------------
# History Window
# ---------------------------------------------------------------------------


class HistoryWindow(SecondaryWindow):
    """
    Displays encryption and decryption history.
    """

    window_type = WINDOW_HISTORY

    def __init__(
        self,
        parent: Any = None,
        *,
        manager: WindowManager | None = None,
        history: list[dict[str, Any]] | None = None,
    ) -> None:
        """Initialize the history window."""

        super().__init__(
            parent,
            manager=manager,
            title="Encryption History",
            width=850,
            height=550,
        )

        self.history = (
            list(history)
            if history is not None
            else []
        )

        self.tree: Any = None

    def build(self) -> Any:
        """Build the history window."""

        window = super().build()

        if ttk is None:
            raise WindowConfigurationError(
                "ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=20,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        container.columnconfigure(
            0,
            weight=1,
        )

        container.rowconfigure(
            1,
            weight=1,
        )

        ttk.Label(
            container,
            text="Encryption History",
            font=(
                "TkDefaultFont",
                16,
                "bold",
            ),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 12),
        )

        columns = (
            "operation",
            "cipher",
            "timestamp",
            "source",
        )

        tree_frame = ttk.Frame(
            container,
        )

        tree_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        tree_frame.columnconfigure(
            0,
            weight=1,
        )

        tree_frame.rowconfigure(
            0,
            weight=1,
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        headings = {
            "operation": "Operation",
            "cipher": "Cipher",
            "timestamp": "Timestamp",
            "source": "Source",
        }

        for column in columns:
            self.tree.heading(
                column,
                text=headings[column],
            )

            self.tree.column(
                column,
                anchor="w",
                width=150,
            )

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview,
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self._populate_history()

        button_frame = ttk.Frame(
            container,
        )

        button_frame.grid(
            row=2,
            column=0,
            sticky="e",
            pady=(12, 0),
        )

        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh,
        ).pack(
            side="left",
            padx=(0, 8),
        )

        ttk.Button(
            button_frame,
            text="Close",
            command=self.close,
        ).pack(
            side="left",
        )

        return window

    def _populate_history(self) -> None:
        """Populate the history tree."""

        if self.tree is None:
            return

        for item in self.tree.get_children():
            self.tree.delete(
                item
            )

        for entry in self.history:
            self.tree.insert(
                "",
                "end",
                values=(
                    entry.get(
                        "operation",
                        "",
                    ),
                    entry.get(
                        "cipher",
                        "",
                    ),
                    entry.get(
                        "timestamp",
                        "",
                    ),
                    entry.get(
                        "source",
                        "",
                    ),
                ),
            )

    def set_history(
        self,
        history: list[dict[str, Any]],
    ) -> None:
        """Replace the displayed history."""

        self.history = list(
            history
        )

        self._populate_history()

    def refresh(self) -> None:
        """Refresh the history display."""

        self._populate_history()

        self.emit(
            "history_refreshed",
            self,
        )


# ---------------------------------------------------------------------------
# Analysis Window
# ---------------------------------------------------------------------------


class AnalysisWindow(SecondaryWindow):
    """
    Window for displaying cryptanalysis results.
    """

    window_type = WINDOW_ANALYSIS

    def __init__(
        self,
        parent: Any = None,
        *,
        manager: WindowManager | None = None,
        title: str = "Cryptanalysis",
    ) -> None:
        """Initialize the analysis window."""

        super().__init__(
            parent,
            manager=manager,
            title=title,
            width=900,
            height=650,
        )

        self.results_frame: Any = None
        self.results_text: Any = None

    def build(self) -> Any:
        """Build the analysis window."""

        window = super().build()

        if ttk is None or tk is None:
            raise WindowConfigurationError(
                "Tkinter/ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=20,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        container.columnconfigure(
            0,
            weight=1,
        )

        container.rowconfigure(
            1,
            weight=1,
        )

        ttk.Label(
            container,
            text="Cryptanalysis Results",
            font=(
                "TkDefaultFont",
                16,
                "bold",
            ),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 12),
        )

        self.results_frame = ttk.Frame(
            container,
        )

        self.results_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self.results_frame.columnconfigure(
            0,
            weight=1,
        )

        self.results_frame.rowconfigure(
            0,
            weight=1,
        )

        self.results_text = tk.Text(
            self.results_frame,
            wrap="word",
            state="disabled",
        )

        self.results_text.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        scrollbar = ttk.Scrollbar(
            self.results_frame,
            orient="vertical",
            command=self.results_text.yview,
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        self.results_text.configure(
            yscrollcommand=scrollbar.set
        )

        ttk.Button(
            container,
            text="Close",
            command=self.close,
        ).grid(
            row=2,
            column=0,
            sticky="e",
            pady=(12, 0),
        )

        return window

    def set_results(
        self,
        results: Any,
    ) -> None:
        """
        Display analysis results.

        Dictionaries are displayed as key/value pairs,
        while other values are converted to strings.
        """

        if self.results_text is None:
            return

        if isinstance(
            results,
            dict,
        ):
            lines = []

            for key, value in results.items():
                lines.append(
                    f"{key}: {value}"
                )

            output = "\n".join(
                lines
            )

        elif isinstance(
            results,
            (list, tuple),
        ):
            output = "\n".join(
                str(item)
                for item in results
            )

        else:
            output = str(results)

        self.results_text.configure(
            state="normal"
        )

        self.results_text.delete(
            "1.0",
            tk.END,
        )

        self.results_text.insert(
            "1.0",
            output,
        )

        self.results_text.configure(
            state="disabled"
        )

        self.emit(
            "results_updated",
            self,
            results,
        )


# ---------------------------------------------------------------------------
# Window Factory Helpers
# ---------------------------------------------------------------------------


def create_main_window(
    root: Any = None,
    *,
    manager: WindowManager | None = None,
    title: str = DEFAULT_WINDOW_TITLE,
) -> MainWindow:
    """
    Create the application's main window.
    """

    return MainWindow(
        root,
        manager=manager,
        title=title,
    )


def create_settings_window(
    parent: Any,
    *,
    manager: WindowManager | None = None,
) -> SettingsWindow:
    """Create the settings window."""

    return SettingsWindow(
        parent,
        manager=manager,
    )


def create_about_window(
    parent: Any,
    *,
    manager: WindowManager | None = None,
    version: str = "1.0.0",
    author: str = "Cryptography Toolkit",
) -> AboutWindow:
    """Create the about window."""

    return AboutWindow(
        parent,
        manager=manager,
        version=version,
        author=author,
    )


def create_help_window(
    parent: Any,
    *,
    manager: WindowManager | None = None,
) -> HelpWindow:
    """Create the help window."""

    return HelpWindow(
        parent,
        manager=manager,
    )


def create_history_window(
    parent: Any,
    *,
    manager: WindowManager | None = None,
    history: list[dict[str, Any]] | None = None,
) -> HistoryWindow:
    """Create the history window."""

    return HistoryWindow(
        parent,
        manager=manager,
        history=history,
    )


def create_analysis_window(
    parent: Any,
    *,
    manager: WindowManager | None = None,
) -> AnalysisWindow:
    """Create the analysis window."""

    return AnalysisWindow(
        parent,
        manager=manager,
    )


# ---------------------------------------------------------------------------
# Window Registration
# ---------------------------------------------------------------------------


def register_default_windows(
    manager: WindowManager,
) -> WindowManager:
    """
    Register the standard Cryptography Toolkit windows.

    Returns the supplied manager so registration can be
    performed during application initialization.
    """

    manager.register(
        WINDOW_MAIN,
        MainWindow,
    )

    manager.register(
        WINDOW_SETTINGS,
        SettingsWindow,
    )

    manager.register(
        WINDOW_ABOUT,
        AboutWindow,
    )

    manager.register(
        WINDOW_HELP,
        HelpWindow,
    )

    manager.register(
        WINDOW_HISTORY,
        HistoryWindow,
    )

    manager.register(
        WINDOW_ANALYSIS,
        AnalysisWindow,
    )

    return manager


# ---------------------------------------------------------------------------
# Application Window Helpers
# ---------------------------------------------------------------------------


def configure_window_style(
    window: Any,
    *,
    theme: str | None = None,
) -> None:
    """
    Apply basic ttk styling to a window.

    The actual theme definitions are handled by
    gui.themes.
    """

    if ttk is None:
        raise WindowConfigurationError(
            "ttk is unavailable."
        )

    if window is None:
        return

    style = ttk.Style(
        window
    )

    if theme:
        try:
            style.theme_use(
                theme
            )
        except tk.TclError:
            pass


def center_window(
    window: Any,
    *,
    width: int | None = None,
    height: int | None = None,
    parent: Any = None,
) -> None:
    """
    Center an arbitrary Tkinter window.

    This helper is useful when a window is not represented
    by a BaseWindow instance.
    """

    if window is None:
        return

    try:
        window.update_idletasks()

        if width is None:
            width = window.winfo_width()

        if height is None:
            height = window.winfo_height()

        if width <= 1:
            width = DEFAULT_WINDOW_WIDTH

        if height <= 1:
            height = DEFAULT_WINDOW_HEIGHT

        if parent is not None:
            parent.update_idletasks()

            parent_x = (
                parent.winfo_rootx()
            )

            parent_y = (
                parent.winfo_rooty()
            )

            parent_width = (
                parent.winfo_width()
            )

            parent_height = (
                parent.winfo_height()
            )

            x = (
                parent_x
                + (
                    parent_width
                    - width
                )
                // 2
            )

            y = (
                parent_y
                + (
                    parent_height
                    - height
                )
                // 2
            )

        else:
            screen_width = (
                window.winfo_screenwidth()
            )

            screen_height = (
                window.winfo_screenheight()
            )

            x = (
                screen_width
                - width
            ) // 2

            y = (
                screen_height
                - height
            ) // 2

        window.geometry(
            f"{width}x{height}"
            f"+{max(0, x)}"
            f"+{max(0, y)}"
        )

    except tk.TclError:
        pass


def set_window_title(
    window: Any,
    title: str,
) -> None:
    """Set the title of a Tkinter window."""

    if window is None:
        return

    if not isinstance(
        title,
        str,
    ):
        raise TypeError(
            "title must be a string."
        )

    if not title.strip():
        raise ValueError(
            "title cannot be empty."
        )

    try:
        window.title(
            title
        )
    except tk.TclError:
        pass


def close_window(
    window: Any,
) -> None:
    """Safely destroy a Tkinter window."""

    if window is None:
        return

    try:
        window.destroy()
    except tk.TclError:
        pass


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Exceptions
    "WindowError",
    "WindowConfigurationError",
    "WindowStateError",
    "WindowNavigationError",

    # Constants
    "DEFAULT_WINDOW_WIDTH",
    "DEFAULT_WINDOW_HEIGHT",
    "MIN_WINDOW_WIDTH",
    "MIN_WINDOW_HEIGHT",

    "WINDOW_MAIN",
    "WINDOW_SETTINGS",
    "WINDOW_ABOUT",
    "WINDOW_HELP",
    "WINDOW_HISTORY",
    "WINDOW_ANALYSIS",

    "STATE_CREATED",
    "STATE_VISIBLE",
    "STATE_HIDDEN",
    "STATE_CLOSED",

    "DEFAULT_WINDOW_TITLE",

    # Configuration / State
    "WindowConfig",
    "WindowState",

    # Window Management
    "WindowManager",

    # Base Windows
    "BaseWindow",
    "SecondaryWindow",

    # Application Windows
    "MainWindow",
    "SettingsWindow",
    "AboutWindow",
    "HelpWindow",
    "HistoryWindow",
    "AnalysisWindow",

    # Factory Helpers
    "create_main_window",
    "create_settings_window",
    "create_about_window",
    "create_help_window",
    "create_history_window",
    "create_analysis_window",

    # Registration
    "register_default_windows",

    # Utilities
    "configure_window_style",
    "center_window",
    "set_window_title",
    "close_window",
]

