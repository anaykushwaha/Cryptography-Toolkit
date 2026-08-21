# app.py
# Main GUI application controller for the
# Cryptography Toolkit
#
# Coordinates the GUI windows, widgets, themes,
# dialogs, application state, and user actions.


from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
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


class ApplicationError(Exception):
    """Base exception for GUI application errors."""

    pass


class ApplicationConfigurationError(
    ApplicationError
):
    """Raised when application configuration is invalid."""

    pass


class ApplicationStateError(
    ApplicationError
):
    """Raised when the application is in an invalid state."""

    pass


class ApplicationInitializationError(
    ApplicationError
):
    """Raised when the application cannot be initialized."""

    pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


APPLICATION_NAME = "Cryptography Toolkit"

APPLICATION_VERSION = "1.0.0"

APPLICATION_AUTHOR = "Cryptography Toolkit"

APPLICATION_DESCRIPTION = (
    "A modular Python toolkit for classical "
    "cryptography, encryption, decryption, "
    "and cryptanalysis."
)

APPLICATION_STATE_CREATED = "created"
APPLICATION_STATE_RUNNING = "running"
APPLICATION_STATE_PAUSED = "paused"
APPLICATION_STATE_CLOSING = "closing"
APPLICATION_STATE_CLOSED = "closed"

DEFAULT_THEME = "default"

DEFAULT_STATUS = "Ready"


# ---------------------------------------------------------------------------
# Application Configuration
# ---------------------------------------------------------------------------


@dataclass
class ApplicationConfig:
    """
    Configuration for the Cryptography Toolkit GUI.

    This object stores application-level settings rather
    than settings belonging to an individual window.
    """

    name: str = APPLICATION_NAME

    version: str = APPLICATION_VERSION

    author: str = APPLICATION_AUTHOR

    description: str = APPLICATION_DESCRIPTION

    theme: str = DEFAULT_THEME

    width: int = 1100

    height: int = 750

    min_width: int = 800

    min_height: int = 550

    center_window: bool = True

    resizable: bool = True

    start_maximized: bool = False

    start_fullscreen: bool = False

    confirm_exit: bool = True

    enable_history: bool = True

    enable_logging: bool = True

    enable_file_operations: bool = True

    data_directory: Path | None = None

    reports_directory: Path | None = None

    history_directory: Path | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """Validate application configuration."""

        if not self.name.strip():
            raise ValueError(
                "Application name cannot be empty."
            )

        if not self.version.strip():
            raise ValueError(
                "Application version cannot be empty."
            )

        if self.width <= 0:
            raise ValueError(
                "Application width must be positive."
            )

        if self.height <= 0:
            raise ValueError(
                "Application height must be positive."
            )

        if self.min_width <= 0:
            raise ValueError(
                "Minimum width must be positive."
            )

        if self.min_height <= 0:
            raise ValueError(
                "Minimum height must be positive."
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
# Application State
# ---------------------------------------------------------------------------


@dataclass
class ApplicationState:
    """
    Runtime state for the GUI application.
    """

    state: str = (
        APPLICATION_STATE_CREATED
    )

    current_view: str | None = None

    status_message: str = DEFAULT_STATUS

    initialized: bool = False

    running: bool = False

    closing: bool = False

    closed: bool = False

    encryption_count: int = 0

    decryption_count: int = 0

    analysis_count: int = 0

    error_count: int = 0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def mark_running(self) -> None:
        """Mark the application as running."""

        self.state = (
            APPLICATION_STATE_RUNNING
        )

        self.initialized = True
        self.running = True
        self.closing = False
        self.closed = False

    def mark_paused(self) -> None:
        """Mark the application as paused."""

        self.state = (
            APPLICATION_STATE_PAUSED
        )

        self.running = False

    def mark_closing(self) -> None:
        """Mark the application as closing."""

        self.state = (
            APPLICATION_STATE_CLOSING
        )

        self.running = False
        self.closing = True

    def mark_closed(self) -> None:
        """Mark the application as closed."""

        self.state = (
            APPLICATION_STATE_CLOSED
        )

        self.running = False
        self.closing = False
        self.closed = True


# ---------------------------------------------------------------------------
# Application Event
# ---------------------------------------------------------------------------


@dataclass
class ApplicationEvent:
    """
    Represents an application-level event.
    """

    name: str

    source: Any = None

    data: Any = None

    cancelled: bool = False

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def cancel(self) -> None:
        """Cancel the event."""

        self.cancelled = True


# ---------------------------------------------------------------------------
# Main Application Controller
# ---------------------------------------------------------------------------


class CryptographyApplication:
    """
    Main controller for the Cryptography Toolkit GUI.

    Responsibilities include:

    - Creating the Tkinter root window
    - Managing application state
    - Managing the window manager
    - Connecting GUI components
    - Handling application events
    - Starting and stopping the event loop
    - Managing application-level callbacks
    """

    def __init__(
        self,
        *,
        config: ApplicationConfig | None = None,
        root: Any = None,
    ) -> None:
        """Initialize the GUI application."""

        self.config = (
            config
            if config is not None
            else ApplicationConfig()
        )

        self.state = ApplicationState()

        self.root = root

        self.window_manager: Any = None

        self.main_window: Any = None

        self.theme_manager: Any = None

        self._callbacks: dict[
            str,
            list[Callable[..., Any]],
        ] = {}

        self._initialized = False

        self._shutdown_requested = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def initialized(self) -> bool:
        """Return whether the application is initialized."""

        return self._initialized

    @property
    def running(self) -> bool:
        """Return whether the application is running."""

        return self.state.running

    @property
    def closed(self) -> bool:
        """Return whether the application is closed."""

        return self.state.closed

    @property
    def current_view(self) -> str | None:
        """Return the currently active application view."""

        return self.state.current_view

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """
        Initialize all GUI application components.

        This method is intentionally separate from ``run()``
        so the application can be embedded or tested without
        immediately entering Tkinter's event loop.
        """

        if self._initialized:
            return

        self._require_tkinter()

        try:
            self._create_root()
            self._initialize_theme_manager()
            self._initialize_window_manager()
            self._create_main_window()
            self._configure_root()
            self._configure_application_events()

        except Exception as error:
            self._cleanup_after_initialization_error()

            raise ApplicationInitializationError(
                "Failed to initialize the GUI application."
            ) from error

        self._initialized = True

        self.state.initialized = True

        self.emit(
            "initialized",
            self,
        )

    def _create_root(self) -> None:
        """Create the Tkinter root window if required."""

        if self.root is not None:
            return

        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            raise ApplicationInitializationError(
                "Unable to create the Tkinter root window."
            ) from error

    def _initialize_theme_manager(self) -> None:
        """Initialize the GUI theme manager."""

        try:
            from .themes import ThemeManager

            self.theme_manager = ThemeManager(
                self.root
            )

            self.theme_manager.apply(
                self.config.theme
            )

        except ImportError:
            self.theme_manager = None

        except Exception as error:
            raise ApplicationInitializationError(
                "Unable to initialize the theme manager."
            ) from error

    def _initialize_window_manager(self) -> None:
        """Initialize and configure the window manager."""

        try:
            from .windows import (
                WindowManager,
                register_default_windows,
            )

            self.window_manager = WindowManager(
                self.root
            )

            register_default_windows(
                self.window_manager
            )

        except ImportError as error:
            raise ApplicationInitializationError(
                "Unable to initialize the window manager."
            ) from error

    def _create_main_window(self) -> None:
        """Create the application's main window."""

        if self.window_manager is None:
            raise ApplicationStateError(
                "Window manager has not been initialized."
            )

        self.main_window = (
            self.window_manager.create(
                "main"
            )
        )

        self.main_window.build()

    def _configure_root(self) -> None:
        """Configure root-window behavior."""

        if self.root is None:
            return

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.request_shutdown,
        )

        self.root.title(
            self.config.name
        )

        self.root.minsize(
            self.config.min_width,
            self.config.min_height,
        )

        self.root.resizable(
            self.config.resizable,
            self.config.resizable,
        )

        if self.config.center_window:
            self._center_root()

        if self.config.start_maximized:
            try:
                self.root.state(
                    "zoomed"
                )
            except tk.TclError:
                pass

        if self.config.start_fullscreen:
            try:
                self.root.attributes(
                    "-fullscreen",
                    True,
                )
            except tk.TclError:
                pass

    def _center_root(self) -> None:
        """Center the root application window."""

        if self.root is None:
            return

        try:
            self.root.update_idletasks()

            width = self.root.winfo_width()
            height = self.root.winfo_height()

            if width <= 1:
                width = self.config.width

            if height <= 1:
                height = self.config.height

            screen_width = (
                self.root.winfo_screenwidth()
            )

            screen_height = (
                self.root.winfo_screenheight()
            )

            x = (
                screen_width
                - width
            ) // 2

            y = (
                screen_height
                - height
            ) // 2

            self.root.geometry(
                f"{width}x{height}"
                f"+{max(0, x)}"
                f"+{max(0, y)}"
            )

        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    # Application Events
    # ------------------------------------------------------------------

    def _configure_application_events(
        self,
    ) -> None:
        """Configure application-level events."""

        if self.root is None:
            return

        self.root.bind(
            "<Control-q>",
            self._on_quit_shortcut,
        )

        self.root.bind(
            "<F1>",
            self._on_help_shortcut,
        )

    def bind(
        self,
        event: str,
        callback: Callable[
            [ApplicationEvent],
            Any,
        ],
    ) -> None:
        """
        Register an application event callback.
        """

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

    def unbind(
        self,
        event: str,
        callback: Callable[
            [ApplicationEvent],
            Any,
        ] | None = None,
    ) -> None:
        """Remove an application event callback."""

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
        event_name: str,
        *,
        source: Any = None,
        data: Any = None,
    ) -> ApplicationEvent:
        """
        Emit an application event.
        """

        event = ApplicationEvent(
            name=event_name,
            source=source,
            data=data,
        )

        for callback in self._callbacks.get(
            event_name,
            [],
        ):
            callback(
                event
            )

            if event.cancelled:
                break

        return event

    # ------------------------------------------------------------------
    # Application Startup
    # ------------------------------------------------------------------

    def start(self) -> None:
        """
        Start the application without entering the event loop.
        """

        if self.closed:
            raise ApplicationStateError(
                "Cannot start a closed application."
            )

        if not self.initialized:
            self.initialize()

        if self.state.running:
            return

        self.state.mark_running()

        if self.main_window is not None:
            self.main_window.show()

        self.emit(
            "started",
            source=self,
        )

    def run(self) -> None:
        """
        Initialize, start, and run the Tkinter event loop.
        """

        self.start()

        if self.root is None:
            raise ApplicationStateError(
                "Application root does not exist."
            )

        try:
            self.root.mainloop()

        except KeyboardInterrupt:
            self.request_shutdown()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def show_view(
        self,
        view_name: str,
        **kwargs: Any,
    ) -> Any:
        """
        Navigate to a registered application window/view.
        """

        if not self.initialized:
            raise ApplicationStateError(
                "Application has not been initialized."
            )

        if self.window_manager is None:
            raise ApplicationStateError(
                "Window manager is unavailable."
            )

        if view_name == "main":
            if self.main_window is None:
                raise ApplicationStateError(
                    "Main window is unavailable."
                )

            self.main_window.show()

            self.state.current_view = "main"

            return self.main_window

        window = self.window_manager.navigate(
            view_name,
            **kwargs,
        )

        self.state.current_view = view_name

        self.emit(
            "view_changed",
            source=self,
            data=view_name,
        )

        return window

    def show_main(self) -> Any:
        """Return to the main application window."""

        return self.show_view(
            "main"
        )

    def show_settings(self) -> Any:
        """Show the settings window."""

        return self.show_view(
            "settings"
        )

    def show_about(self) -> Any:
        """Show the about window."""

        return self.show_view(
            "about"
        )

    def show_help(self) -> Any:
        """Show the help window."""

        return self.show_view(
            "help"
        )

    def show_history(self) -> Any:
        """Show the history window."""

        return self.show_view(
            "history"
        )

    def show_analysis(self) -> Any:
        """Show the analysis window."""

        return self.show_view(
            "analysis"
        )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def set_status(
        self,
        message: str,
    ) -> None:
        """Update the global application status."""

        self.state.status_message = str(
            message
        )

        if self.main_window is not None:
            try:
                self.main_window.set_status(
                    self.state.status_message
                )
            except AttributeError:
                pass

        self.emit(
            "status_changed",
            source=self,
            data=self.state.status_message,
        )

    def clear_status(self) -> None:
        """Reset the application status."""

        self.set_status(
            DEFAULT_STATUS
        )

    # ------------------------------------------------------------------
    # Counters
    # ------------------------------------------------------------------

    def record_encryption(self) -> None:
        """Record a completed encryption operation."""

        self.state.encryption_count += 1

        self.emit(
            "encryption_completed",
            source=self,
        )

    def record_decryption(self) -> None:
        """Record a completed decryption operation."""

        self.state.decryption_count += 1

        self.emit(
            "decryption_completed",
            source=self,
        )

    def record_analysis(self) -> None:
        """Record a completed analysis operation."""

        self.state.analysis_count += 1

        self.emit(
            "analysis_completed",
            source=self,
        )

    def record_error(
        self,
        error: Exception | str,
    ) -> None:
        """Record an application error."""

        self.state.error_count += 1

        self.emit(
            "error",
            source=self,
            data=error,
        )

    # ------------------------------------------------------------------
    # Keyboard Shortcuts
    # ------------------------------------------------------------------

    def _on_quit_shortcut(
        self,
        event: Any = None,
    ) -> str:
        """Handle the Ctrl+Q shortcut."""

        self.request_shutdown()

        return "break"

    def _on_help_shortcut(
        self,
        event: Any = None,
    ) -> str:
        """Handle the F1 help shortcut."""

        try:
            self.show_help()
        except ApplicationError:
            pass

        return "break"

    # ------------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------------

    def request_shutdown(self) -> None:
        """Request application shutdown."""

        if self.state.closing:
            return

        self._shutdown_requested = True

        event = self.emit(
            "before_shutdown",
            source=self,
        )

        if event.cancelled:
            self._shutdown_requested = False

            return

        if self.config.confirm_exit:
            self._confirm_shutdown()
        else:
            self.shutdown()

    def _confirm_shutdown(self) -> None:
        """Ask the user to confirm application shutdown."""

        try:
            from .dialogs import ask_confirmation

            confirmed = ask_confirmation(
                self.root,
                title="Exit Cryptography Toolkit",
                message=(
                    "Are you sure you want to "
                    "exit the Cryptography Toolkit?"
                ),
            )

        except Exception:
            confirmed = True

        if confirmed:
            self.shutdown()
        else:
            self._shutdown_requested = False

    def shutdown(self) -> None:
        """Shutdown the application."""

        if self.state.closed:
            return

        self.state.mark_closing()

        self.emit(
            "shutdown",
            source=self,
        )

        if self.window_manager is not None:
            try:
                self.window_manager.close_all()
            except Exception:
                pass

        if self.root is not None:
            try:
                self.root.quit()
                self.root.destroy()
            except tk.TclError:
                pass

        self.root = None

        self._initialized = False

        self.state.mark_closed()

    def _cleanup_after_initialization_error(
        self,
    ) -> None:
        """Clean up resources after initialization fails."""

        try:
            if self.root is not None:
                self.root.destroy()
        except Exception:
            pass

        self.root = None

        self.window_manager = None
        self.main_window = None
        self.theme_manager = None

        self._initialized = False

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def _require_tkinter() -> None:
        """Ensure Tkinter is available."""

        if tk is None or ttk is None:
            raise ApplicationInitializationError(
                "Tkinter is unavailable. "
                "The GUI cannot be started."
            )

    def update(self) -> None:
        """Process pending Tkinter updates."""

        if self.root is None:
            raise ApplicationStateError(
                "Application root is unavailable."
            )

        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError as error:
            raise ApplicationStateError(
                "Unable to update the application."
            ) from error

    def __enter__(
        self,
    ) -> "CryptographyApplication":
        """Enter the application context."""

        self.start()

        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:
        """Exit the application context."""

        if not self.closed:
            self.shutdown()

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""

        return (
            f"{self.__class__.__name__}("
            f"state={self.state.state!r}, "
            f"initialized={self.initialized}, "
            f"running={self.running}, "
            f"closed={self.closed}"
            f")"
        )

    # ---------------------------------------------------------------------------
# Core Toolkit Integration
# ---------------------------------------------------------------------------


class ToolkitController:
    """
    Integration layer between the GUI and the core toolkit.

    Keeps cryptographic operations separate from the GUI while
    providing a simple interface for the application controller.
    """

    def __init__(
        self,
        application: CryptographyApplication,
    ) -> None:
        """Initialize the toolkit controller."""

        self.application = application

        self.last_result: Any = None

        self.last_error: Exception | None = None

    # ------------------------------------------------------------------
    # Encryption
    # ------------------------------------------------------------------

    def encrypt(
        self,
        text: str,
        cipher: str = "caesar",
        key: Any = 0,
        **kwargs: Any,
    ) -> Any:
        """
        Encrypt text using a supported cipher.

        The core cipher implementation is imported lazily so the
        GUI can still be imported independently during testing.
        """

        if not isinstance(
            text,
            str,
        ):
            raise TypeError(
                "text must be a string."
            )

        try:
            result = self._execute_cipher(
                operation="encrypt",
                text=text,
                cipher=cipher,
                key=key,
                **kwargs,
            )

            self.last_result = result
            self.last_error = None

            self.application.record_encryption()
            self.application.set_status(
                "Encryption completed."
            )

            return result

        except Exception as error:
            self.last_error = error

            self.application.record_error(
                error
            )

            self.application.set_status(
                "Encryption failed."
            )

            raise

    # ------------------------------------------------------------------
    # Decryption
    # ------------------------------------------------------------------

    def decrypt(
        self,
        text: str,
        cipher: str = "caesar",
        key: Any = 0,
        **kwargs: Any,
    ) -> Any:
        """
        Decrypt text using a supported cipher.
        """

        if not isinstance(
            text,
            str,
        ):
            raise TypeError(
                "text must be a string."
            )

        try:
            result = self._execute_cipher(
                operation="decrypt",
                text=text,
                cipher=cipher,
                key=key,
                **kwargs,
            )

            self.last_result = result
            self.last_error = None

            self.application.record_decryption()
            self.application.set_status(
                "Decryption completed."
            )

            return result

        except Exception as error:
            self.last_error = error

            self.application.record_error(
                error
            )

            self.application.set_status(
                "Decryption failed."
            )

            raise

    # ------------------------------------------------------------------
    # Cipher Execution
    # ------------------------------------------------------------------

    def _execute_cipher(
        self,
        operation: str,
        text: str,
        cipher: str,
        key: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Dispatch a cryptographic operation to the cipher package.
        """

        cipher_name = (
            str(cipher)
            .strip()
            .lower()
        )

        if cipher_name == "caesar":
            from cipher.caesar import (
                CaesarCipher,
            )

            cipher_instance = CaesarCipher(
                key
            )

        elif cipher_name == "rot":
            from cipher.rot import (
                ROTCipher,
            )

            cipher_instance = ROTCipher(
                key
            )

        elif cipher_name == "atbash":
            from cipher.atbash import (
                AtbashCipher,
            )

            cipher_instance = AtbashCipher()

        else:
            raise ValueError(
                f"Unsupported cipher: {cipher}"
            )

        method = getattr(
            cipher_instance,
            operation,
            None,
        )

        if method is None:
            raise AttributeError(
                f"Cipher does not support "
                f"{operation}."
            )

        return method(
            text,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    def analyze(
        self,
        text: str,
        analysis_type: str = "frequency",
        **kwargs: Any,
    ) -> Any:
        """
        Perform cryptanalysis using the analysis package.
        """

        if not isinstance(
            text,
            str,
        ):
            raise TypeError(
                "text must be a string."
            )

        analysis_name = (
            str(analysis_type)
            .strip()
            .lower()
        )

        try:
            result = self._execute_analysis(
                text=text,
                analysis_type=analysis_name,
                **kwargs,
            )

            self.last_result = result
            self.last_error = None

            self.application.record_analysis()
            self.application.set_status(
                "Analysis completed."
            )

            return result

        except Exception as error:
            self.last_error = error

            self.application.record_error(
                error
            )

            self.application.set_status(
                "Analysis failed."
            )

            raise

    def _execute_analysis(
        self,
        text: str,
        analysis_type: str,
        **kwargs: Any,
    ) -> Any:
        """Dispatch an analysis operation."""

        if analysis_type == "frequency":
            from analysis.frequency import (
                frequency_analysis,
            )

            return frequency_analysis(
                text,
                **kwargs,
            )

        if analysis_type == "entropy":
            from analysis.entropy import (
                calculate_entropy,
            )

            return calculate_entropy(
                text,
                **kwargs,
            )

        if analysis_type == "ioc":
            from analysis.ioc import (
                calculate_ioc,
            )

            return calculate_ioc(
                text,
                **kwargs,
            )

        if analysis_type == "statistics":
            from analysis.statistics import (
                analyze_statistics,
            )

            return analyze_statistics(
                text,
                **kwargs,
            )

        if analysis_type == "ngrams":
            from analysis.ngrams import (
                analyze_ngrams,
            )

            return analyze_ngrams(
                text,
                **kwargs,
            )

        if analysis_type == "brute_force":
            from analysis.brute_force import (
                brute_force,
            )

            return brute_force(
                text,
                **kwargs,
            )

        raise ValueError(
            f"Unsupported analysis type: "
            f"{analysis_type}"
        )


# ---------------------------------------------------------------------------
# Application Operations
# ---------------------------------------------------------------------------


class ApplicationOperations:
    """
    High-level operations exposed to the GUI.

    This class provides a clean boundary between widgets,
    dialogs, file handling, and the toolkit controller.
    """

    def __init__(
        self,
        application: CryptographyApplication,
    ) -> None:
        """Initialize application operations."""

        self.application = application

        self.toolkit = ToolkitController(
            application
        )

        self.last_input: str = ""

        self.last_output: str = ""

        self.last_operation: str | None = None

        self.last_cipher: str | None = None

        self.last_key: Any = None

    # ------------------------------------------------------------------
    # Encryption
    # ------------------------------------------------------------------

    def encrypt_text(
        self,
        text: str,
        cipher: str,
        key: Any,
        **kwargs: Any,
    ) -> Any:
        """Encrypt text and store operation metadata."""

        self.last_input = text
        self.last_operation = "encrypt"
        self.last_cipher = cipher
        self.last_key = key

        result = self.toolkit.encrypt(
            text,
            cipher=cipher,
            key=key,
            **kwargs,
        )

        self.last_output = str(
            result
        )

        return result

    # ------------------------------------------------------------------
    # Decryption
    # ------------------------------------------------------------------

    def decrypt_text(
        self,
        text: str,
        cipher: str,
        key: Any,
        **kwargs: Any,
    ) -> Any:
        """Decrypt text and store operation metadata."""

        self.last_input = text
        self.last_operation = "decrypt"
        self.last_cipher = cipher
        self.last_key = key

        result = self.toolkit.decrypt(
            text,
            cipher=cipher,
            key=key,
            **kwargs,
        )

        self.last_output = str(
            result
        )

        return result

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    def analyze_text(
        self,
        text: str,
        analysis_type: str,
        **kwargs: Any,
    ) -> Any:
        """Analyze text and store operation metadata."""

        self.last_input = text
        self.last_operation = "analysis"

        result = self.toolkit.analyze(
            text,
            analysis_type=analysis_type,
            **kwargs,
        )

        self.last_output = str(
            result
        )

        return result

    # ------------------------------------------------------------------
    # File Operations
    # ------------------------------------------------------------------

    def read_file(
        self,
        path: str | Path,
    ) -> str:
        """Read text from a file."""

        file_path = Path(
            path
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )
        except UnicodeDecodeError as error:
            raise ValueError(
                "The selected file is not "
                "valid UTF-8 text."
            ) from error

        self.last_input = content

        self.application.set_status(
            f"Loaded {file_path.name}"
        )

        return content

    def write_file(
        self,
        path: str | Path,
        content: str,
    ) -> Path:
        """Write text to a file."""

        file_path = Path(
            path
        )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            str(content),
            encoding="utf-8",
        )

        self.application.set_status(
            f"Saved {file_path.name}"
        )

        return file_path

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_result(
        self,
        path: str | Path,
        result: Any = None,
    ) -> Path:
        """
        Export the current or supplied result.

        The fileio exporter is imported lazily so that the
        application controller remains independently testable.
        """

        if result is None:
            result = self.last_output

        file_path = Path(
            path
        )

        try:
            from fileio.exporters import (
                export_text,
            )

            export_text(
                result,
                file_path,
            )

        except ImportError:
            self.write_file(
                file_path,
                str(result),
            )

        self.application.set_status(
            f"Exported {file_path.name}"
        )

        return file_path

    # ------------------------------------------------------------------
    # Operation State
    # ------------------------------------------------------------------

    def clear_operation(self) -> None:
        """Clear the current operation state."""

        self.last_input = ""
        self.last_output = ""
        self.last_operation = None
        self.last_cipher = None
        self.last_key = None

        self.application.clear_status()

    def get_operation_summary(
        self,
    ) -> dict[str, Any]:
        """Return information about the last operation."""

        return {
            "operation": self.last_operation,
            "cipher": self.last_cipher,
            "key": self.last_key,
            "input": self.last_input,
            "output": self.last_output,
        }


# ---------------------------------------------------------------------------
# GUI Application Context
# ---------------------------------------------------------------------------


@dataclass
class ApplicationContext:
    """
    Shared context passed to GUI components.

    Provides a single object through which widgets and windows
    can access the application controller and toolkit operations.
    """

    application: CryptographyApplication

    operations: ApplicationOperations | None = None

    data: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """Initialize dependent context objects."""

        if self.operations is None:
            self.operations = (
                ApplicationOperations(
                    self.application
                )
            )

    @property
    def config(
        self,
    ) -> ApplicationConfig:
        """Return application configuration."""

        return self.application.config

    @property
    def state(
        self,
    ) -> ApplicationState:
        """Return application state."""

        return self.application.state

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Store contextual data."""

        self.data[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Retrieve contextual data."""

        return self.data.get(
            key,
            default,
        )

    def remove(
        self,
        key: str,
    ) -> Any:
        """Remove and return contextual data."""

        return self.data.pop(
            key,
            None,
        )

    def clear(self) -> None:
        """Clear contextual data."""

        self.data.clear()


# ---------------------------------------------------------------------------
# Application Factory
# ---------------------------------------------------------------------------


def create_application(
    *,
    config: ApplicationConfig | None = None,
    root: Any = None,
    initialize: bool = True,
) -> CryptographyApplication:
    """
    Create a Cryptography Toolkit GUI application.

    Parameters
    ----------
    config:
        Optional application configuration.

    root:
        Optional existing Tkinter root.

    initialize:
        Whether the application should immediately initialize
        its GUI components.
    """

    application = CryptographyApplication(
        config=config,
        root=root,
    )

    if initialize:
        application.initialize()

    return application


def run_application(
    *,
    config: ApplicationConfig | None = None,
    root: Any = None,
) -> CryptographyApplication:
    """
    Create and run the Cryptography Toolkit GUI.

    Returns the application instance after the event loop
    has exited.
    """

    application = create_application(
        config=config,
        root=root,
        initialize=True,
    )

    application.run()

    return application


# ---------------------------------------------------------------------------
# Global Application Reference
# ---------------------------------------------------------------------------


_application: CryptographyApplication | None = None


def get_application() -> CryptographyApplication | None:
    """
    Return the global application instance.

    Returns ``None`` when no global application has been created.
    """

    return _application


def set_application(
    application: CryptographyApplication | None,
) -> None:
    """
    Set the global application instance.
    """

    global _application

    if application is not None and not isinstance(
        application,
        CryptographyApplication,
    ):
        raise TypeError(
            "application must be a "
            "CryptographyApplication instance "
            "or None."
        )

    _application = application


def initialize_application(
    *,
    config: ApplicationConfig | None = None,
    root: Any = None,
) -> CryptographyApplication:
    """
    Initialize and register the global application instance.
    """

    application = create_application(
        config=config,
        root=root,
        initialize=True,
    )

    set_application(
        application
    )

    return application

# ---------------------------------------------------------------------------
# Application Diagnostics
# ---------------------------------------------------------------------------


def get_application_info(
    application: CryptographyApplication | None = None,
) -> dict[str, Any]:
    """
    Return diagnostic information about the application.

    This is useful for debugging, status displays, and
    collecting basic runtime information.
    """

    if application is None:
        application = get_application()

    if application is None:
        return {
            "name": APPLICATION_NAME,
            "version": APPLICATION_VERSION,
            "initialized": False,
            "running": False,
            "closed": True,
            "state": APPLICATION_STATE_CLOSED,
        }

    state = application.state

    return {
        "name": application.config.name,
        "version": application.config.version,
        "author": application.config.author,
        "initialized": application.initialized,
        "running": application.running,
        "closed": application.closed,
        "state": state.state,
        "current_view": state.current_view,
        "status": state.status_message,
        "encryption_count": state.encryption_count,
        "decryption_count": state.decryption_count,
        "analysis_count": state.analysis_count,
        "error_count": state.error_count,
        "theme": application.config.theme,
    }


def is_application_running(
    application: CryptographyApplication | None = None,
) -> bool:
    """Return whether the application is currently running."""

    if application is None:
        application = get_application()

    if application is None:
        return False

    return application.running


def is_application_initialized(
    application: CryptographyApplication | None = None,
) -> bool:
    """Return whether the application has been initialized."""

    if application is None:
        application = get_application()

    if application is None:
        return False

    return application.initialized


# ---------------------------------------------------------------------------
# Application Reset
# ---------------------------------------------------------------------------


def reset_application(
    *,
    destroy: bool = True,
) -> None:
    """
    Reset the global application reference.

    Parameters
    ----------
    destroy:
        If ``True``, attempt to shut down the existing
        application before removing the global reference.
    """

    global _application

    application = _application

    if application is None:
        return

    if destroy and not application.closed:
        try:
            application.shutdown()
        except Exception:
            pass

    _application = None


# ---------------------------------------------------------------------------
# Application Convenience Functions
# ---------------------------------------------------------------------------


def show_main_window(
    application: CryptographyApplication | None = None,
) -> Any:
    """Show the main application window."""

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    if not application.initialized:
        application.initialize()

    return application.show_main()


def show_settings_window(
    application: CryptographyApplication | None = None,
) -> Any:
    """Show the settings window."""

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    if not application.initialized:
        application.initialize()

    return application.show_settings()


def show_about_window(
    application: CryptographyApplication | None = None,
) -> Any:
    """Show the about window."""

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    if not application.initialized:
        application.initialize()

    return application.show_about()


def show_help_window(
    application: CryptographyApplication | None = None,
) -> Any:
    """Show the help window."""

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    if not application.initialized:
        application.initialize()

    return application.show_help()


def show_history_window(
    application: CryptographyApplication | None = None,
) -> Any:
    """Show the history window."""

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    if not application.initialized:
        application.initialize()

    return application.show_history()


def show_analysis_window(
    application: CryptographyApplication | None = None,
) -> Any:
    """Show the analysis window."""

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    if not application.initialized:
        application.initialize()

    return application.show_analysis()


# ---------------------------------------------------------------------------
# Operation Convenience Functions
# ---------------------------------------------------------------------------


def encrypt_text(
    text: str,
    cipher: str = "caesar",
    key: Any = 0,
    *,
    application: CryptographyApplication | None = None,
    **kwargs: Any,
) -> Any:
    """
    Encrypt text through the active application.

    This convenience function allows GUI components to perform
    encryption without manually creating an operations object.
    """

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    operations = ApplicationOperations(
        application
    )

    return operations.encrypt_text(
        text,
        cipher,
        key,
        **kwargs,
    )


def decrypt_text(
    text: str,
    cipher: str = "caesar",
    key: Any = 0,
    *,
    application: CryptographyApplication | None = None,
    **kwargs: Any,
) -> Any:
    """
    Decrypt text through the active application.
    """

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    operations = ApplicationOperations(
        application
    )

    return operations.decrypt_text(
        text,
        cipher,
        key,
        **kwargs,
    )


def analyze_text(
    text: str,
    analysis_type: str = "frequency",
    *,
    application: CryptographyApplication | None = None,
    **kwargs: Any,
) -> Any:
    """
    Perform cryptanalysis through the active application.
    """

    if application is None:
        application = get_application()

    if application is None:
        raise ApplicationStateError(
            "No application instance is available."
        )

    operations = ApplicationOperations(
        application
    )

    return operations.analyze_text(
        text,
        analysis_type,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Application Lifecycle Helpers
# ---------------------------------------------------------------------------


def start_application(
    application: CryptographyApplication | None = None,
) -> CryptographyApplication:
    """
    Start an existing application.

    If no application is supplied, the global application
    instance is used or created automatically.
    """

    if application is None:
        application = get_application()

    if application is None:
        application = initialize_application()

    application.start()

    set_application(
        application
    )

    return application


def stop_application(
    application: CryptographyApplication | None = None,
) -> None:
    """
    Stop the active application.
    """

    if application is None:
        application = get_application()

    if application is None:
        return

    application.shutdown()

    if application is get_application():
        set_application(
            None
        )


def restart_application(
    *,
    config: ApplicationConfig | None = None,
) -> CryptographyApplication:
    """
    Restart the global application.

    The previous application instance is safely shut down
    before a new instance is created.
    """

    reset_application(
        destroy=True
    )

    application = initialize_application(
        config=config,
    )

    application.start()

    return application


# ---------------------------------------------------------------------------
# Application Callback Helpers
# ---------------------------------------------------------------------------


def on_application_event(
    event_name: str,
    callback: Callable[
        [ApplicationEvent],
        Any,
    ],
    application: CryptographyApplication | None = None,
) -> CryptographyApplication:
    """
    Register a callback on the active application.

    Returns the application instance for convenience.
    """

    if application is None:
        application = get_application()

    if application is None:
        application = initialize_application()

    application.bind(
        event_name,
        callback,
    )

    return application


def remove_application_event(
    event_name: str,
    callback: Callable[
        [ApplicationEvent],
        Any,
    ] | None = None,
    application: CryptographyApplication | None = None,
) -> None:
    """Remove an application event callback."""

    if application is None:
        application = get_application()

    if application is None:
        return

    application.unbind(
        event_name,
        callback,
    )


# ---------------------------------------------------------------------------
# Error Handling
# ---------------------------------------------------------------------------


def handle_application_error(
    error: Exception,
    *,
    application: CryptographyApplication | None = None,
    show_dialog: bool = True,
) -> None:
    """
    Handle an application-level error.

    The error is recorded by the application and may optionally
    be displayed through the GUI dialog system.
    """

    if application is None:
        application = get_application()

    if application is not None:
        application.record_error(
            error
        )

        application.set_status(
            f"Error: {error}"
        )

    if not show_dialog:
        return

    if application is None:
        return

    try:
        from .dialogs import show_error

        show_error(
            application.root,
            title="Application Error",
            message=str(error),
        )

    except Exception:
        # Dialog failures should never replace the original
        # application error.
        pass


# ---------------------------------------------------------------------------
# Safe Execution
# ---------------------------------------------------------------------------


def safe_execute(
    callback: Callable[..., Any],
    *args: Any,
    application: CryptographyApplication | None = None,
    show_error: bool = True,
    default: Any = None,
    **kwargs: Any,
) -> Any:
    """
    Execute a callback while safely handling exceptions.

    Returns the callback result when successful. If an exception
    occurs, the error is recorded and ``default`` is returned.
    """

    if not callable(
        callback
    ):
        raise TypeError(
            "callback must be callable."
        )

    try:
        return callback(
            *args,
            **kwargs,
        )

    except Exception as error:
        handle_application_error(
            error,
            application=application,
            show_dialog=show_error,
        )

        return default


# ---------------------------------------------------------------------------
# GUI Availability
# ---------------------------------------------------------------------------


def gui_available() -> bool:
    """
    Return whether Tkinter is available in the current environment.
    """

    return (
        tk is not None
        and ttk is not None
    )


def require_gui() -> None:
    """
    Raise an application error if the GUI is unavailable.
    """

    if not gui_available():
        raise ApplicationInitializationError(
            "Tkinter is unavailable. "
            "The Cryptography Toolkit GUI "
            "cannot be used in this environment."
        )


# ---------------------------------------------------------------------------
# Module-Level Entry Point
# ---------------------------------------------------------------------------


def main() -> int:
    """
    Main entry point for launching the GUI application.

    Returns
    -------
    int
        Process-style exit code.
    """

    try:
        application = initialize_application()

        application.run()

        return 0

    except KeyboardInterrupt:
        return 0

    except ApplicationError:
        return 1

    except Exception:
        return 1

    finally:
        reset_application(
            destroy=False
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Exceptions
    "ApplicationError",
    "ApplicationConfigurationError",
    "ApplicationStateError",
    "ApplicationInitializationError",

    # Constants
    "APPLICATION_NAME",
    "APPLICATION_VERSION",
    "APPLICATION_AUTHOR",
    "APPLICATION_DESCRIPTION",

    "APPLICATION_STATE_CREATED",
    "APPLICATION_STATE_RUNNING",
    "APPLICATION_STATE_PAUSED",
    "APPLICATION_STATE_CLOSING",
    "APPLICATION_STATE_CLOSED",

    "DEFAULT_THEME",
    "DEFAULT_STATUS",

    # Configuration / State
    "ApplicationConfig",
    "ApplicationState",
    "ApplicationEvent",

    # Main Application
    "CryptographyApplication",

    # Toolkit Integration
    "ToolkitController",
    "ApplicationOperations",
    "ApplicationContext",

    # Application Creation
    "create_application",
    "run_application",
    "initialize_application",

    # Global Application
    "get_application",
    "set_application",
    "reset_application",

    # Window Helpers
    "show_main_window",
    "show_settings_window",
    "show_about_window",
    "show_help_window",
    "show_history_window",
    "show_analysis_window",

    # Operation Helpers
    "encrypt_text",
    "decrypt_text",
    "analyze_text",

    # Lifecycle
    "start_application",
    "stop_application",
    "restart_application",

    # Events
    "on_application_event",
    "remove_application_event",

    # Error Handling
    "handle_application_error",
    "safe_execute",

    # Diagnostics
    "get_application_info",
    "is_application_running",
    "is_application_initialized",

    # GUI Availability
    "gui_available",
    "require_gui",

    # Entry Point
    "main",
]


if __name__ == "__main__":
    raise SystemExit(
        main()
    )

