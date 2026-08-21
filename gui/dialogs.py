# dialogs.py
# Dialog windows and user interaction utilities
# for the Cryptography Toolkit GUI
#
# Provides reusable message dialogs, confirmation
# dialogs, input dialogs, file dialogs, and
# cryptography-specific user prompts.


from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Sequence


try:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import simpledialog
    from tkinter import ttk
except ImportError:  # pragma: no cover
    tk = None
    filedialog = None
    messagebox = None
    simpledialog = None
    ttk = None


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class DialogError(Exception):
    """Base exception for GUI dialog errors."""

    pass


class DialogConfigurationError(DialogError):
    """Raised when a dialog is configured incorrectly."""

    pass


class DialogStateError(DialogError):
    """Raised when a dialog is used in an invalid state."""

    pass


class DialogValidationError(DialogError):
    """Raised when dialog input validation fails."""

    pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


DIALOG_INFO = "info"
DIALOG_WARNING = "warning"
DIALOG_ERROR = "error"
DIALOG_SUCCESS = "success"

RESULT_OK = "ok"
RESULT_CANCEL = "cancel"
RESULT_YES = "yes"
RESULT_NO = "no"
RESULT_RETRY = "retry"
RESULT_ABORT = "abort"

DEFAULT_DIALOG_WIDTH = 420
DEFAULT_DIALOG_HEIGHT = 220

DEFAULT_DIALOG_PADDING = 12

FILE_MODE_OPEN = "open"
FILE_MODE_SAVE = "save"
FILE_MODE_DIRECTORY = "directory"


# ---------------------------------------------------------------------------
# Dialog Result
# ---------------------------------------------------------------------------


@dataclass
class DialogResult:
    """
    Represents the result returned by a dialog.

    Attributes
    ----------
    result:
        Result identifier such as ``ok``, ``cancel``,
        ``yes``, or ``no``.

    value:
        Optional value returned by the dialog.

    accepted:
        Whether the dialog action was accepted.

    cancelled:
        Whether the dialog was cancelled.

    metadata:
        Additional information associated with
        the result.
    """

    result: str = RESULT_CANCEL
    value: Any = None
    accepted: bool = False
    cancelled: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @classmethod
    def ok(
        cls,
        value: Any = None,
        **metadata: Any,
    ) -> "DialogResult":
        """Create a successful result."""

        return cls(
            result=RESULT_OK,
            value=value,
            accepted=True,
            cancelled=False,
            metadata=metadata,
        )

    @classmethod
    def cancel(
        cls,
        **metadata: Any,
    ) -> "DialogResult":
        """Create a cancelled result."""

        return cls(
            result=RESULT_CANCEL,
            accepted=False,
            cancelled=True,
            metadata=metadata,
        )

    @classmethod
    def yes(
        cls,
        value: Any = None,
        **metadata: Any,
    ) -> "DialogResult":
        """Create a positive confirmation result."""

        return cls(
            result=RESULT_YES,
            value=value,
            accepted=True,
            cancelled=False,
            metadata=metadata,
        )

    @classmethod
    def no(
        cls,
        value: Any = None,
        **metadata: Any,
    ) -> "DialogResult":
        """Create a negative confirmation result."""

        return cls(
            result=RESULT_NO,
            value=value,
            accepted=False,
            cancelled=False,
            metadata=metadata,
        )

    def is_success(self) -> bool:
        """Return whether the result represents success."""

        return self.accepted

    def is_cancelled(self) -> bool:
        """Return whether the dialog was cancelled."""

        return self.cancelled

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Retrieve metadata from the result."""

        return self.metadata.get(
            key,
            default,
        )


# ---------------------------------------------------------------------------
# Dialog Configuration
# ---------------------------------------------------------------------------


@dataclass
class DialogConfig:
    """
    Shared configuration for toolkit dialogs.
    """

    title: str = "Cryptography Toolkit"

    width: int = DEFAULT_DIALOG_WIDTH
    height: int = DEFAULT_DIALOG_HEIGHT

    resizable: bool = True

    modal: bool = True

    center: bool = True

    padding: int = DEFAULT_DIALOG_PADDING

    destroy_on_close: bool = True

    grab_set: bool = True

    transient: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """Validate dialog configuration."""

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

        if not isinstance(
            self.width,
            int,
        ):
            raise TypeError(
                "width must be an integer."
            )

        if self.width <= 0:
            raise ValueError(
                "width must be greater than zero."
            )

        if not isinstance(
            self.height,
            int,
        ):
            raise TypeError(
                "height must be an integer."
            )

        if self.height <= 0:
            raise ValueError(
                "height must be greater than zero."
            )

        if self.padding < 0:
            raise ValueError(
                "padding cannot be negative."
            )


# ---------------------------------------------------------------------------
# Dialog Utilities
# ---------------------------------------------------------------------------


def tkinter_available() -> bool:
    """
    Return whether Tkinter dialog functionality
    is available.
    """

    return (
        tk is not None
        and messagebox is not None
        and filedialog is not None
    )


def require_tkinter() -> None:
    """
    Ensure Tkinter is available.

    Raises
    ------
    DialogConfigurationError
        If Tkinter cannot be imported.
    """

    if not tkinter_available():
        raise DialogConfigurationError(
            "Tkinter is unavailable."
        )


def normalize_title(
    title: str | None,
    default: str = "Cryptography Toolkit",
) -> str:
    """
    Normalize a dialog title.
    """

    if title is None:
        return default

    title = str(
        title
    ).strip()

    return title or default


# ---------------------------------------------------------------------------
# Base Dialog
# ---------------------------------------------------------------------------


class BaseDialog:
    """
    Base class for reusable GUI dialogs.

    Provides common functionality for:

    - Dialog creation
    - Modal behavior
    - Window positioning
    - Result management
    - Dialog lifecycle
    - Validation
    - Callback handling
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        config: DialogConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the base dialog."""

        self.parent = parent

        self.config = (
            config
            if config is not None
            else DialogConfig()
        )

        self._build_kwargs = dict(
            kwargs
        )

        self._window: Any = None

        self._result: DialogResult | None = None

        self._initialized = False
        self._closed = False

        self._callbacks: dict[
            str,
            list[Callable[..., Any]],
        ] = {}

        self._metadata: dict[
            str,
            Any,
        ] = dict(
            self.config.metadata
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def window(self) -> Any:
        """Return the underlying dialog window."""

        return self._window

    @property
    def result(self) -> DialogResult | None:
        """Return the current dialog result."""

        return self._result

    @property
    def initialized(self) -> bool:
        """Return whether the dialog has been created."""

        return self._initialized

    @property
    def closed(self) -> bool:
        """Return whether the dialog has been closed."""

        return self._closed

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def build(self) -> Any:
        """
        Build the dialog window.

        Subclasses should extend or override this method
        when adding custom dialog content.
        """

        require_tkinter()

        if self._initialized:
            return self._window

        self._window = tk.Toplevel(
            self.parent
        )

        self._window.title(
            self.config.title
        )

        self._window.geometry(
            f"{self.config.width}"
            f"x"
            f"{self.config.height}"
        )

        self._window.protocol(
            "WM_DELETE_WINDOW",
            self.cancel,
        )

        self._configure_window()

        self._initialized = True
        self._closed = False

        return self._window

    def _configure_window(self) -> None:
        """Apply standard window configuration."""

        if self._window is None:
            return

        self._window.resizable(
            self.config.resizable,
            self.config.resizable,
        )

        if self.config.transient:
            try:
                self._window.transient(
                    self.parent
                )
            except tk.TclError:
                pass

        if self.config.center:
            self.center()

    def show(self) -> DialogResult:
        """
        Display the dialog and wait for its result.
        """

        if not self._initialized:
            self.build()

        if self.config.modal:
            self.make_modal()

        self.emit(
            "show",
            self,
        )

        if self._window is not None:
            try:
                self._window.deiconify()
                self._window.lift()
            except tk.TclError:
                pass

        if self.parent is not None:
            try:
                self.parent.wait_window(
                    self._window
                )
            except tk.TclError:
                pass

        if self._result is None:
            self._result = DialogResult.cancel()

        return self._result

    def close(
        self,
        result: DialogResult | None = None,
    ) -> DialogResult:
        """
        Close the dialog.

        Parameters
        ----------
        result:
            Optional result to store before closing.
        """

        if result is not None:
            self._result = result

        if self._result is None:
            self._result = DialogResult.cancel()

        self._closed = True

        self.emit(
            "close",
            self._result,
        )

        if self._window is not None:
            try:
                if self.config.destroy_on_close:
                    self._window.destroy()
                else:
                    self._window.withdraw()
            except tk.TclError:
                pass

        self._initialized = False

        return self._result

    def cancel(self) -> DialogResult:
        """Cancel and close the dialog."""

        result = DialogResult.cancel()

        return self.close(
            result
        )

    # ------------------------------------------------------------------
    # Modal Behavior
    # ------------------------------------------------------------------

    def make_modal(self) -> None:
        """Configure the dialog as modal."""

        if self._window is None:
            raise DialogStateError(
                "Dialog has not been built."
            )

        if self.config.grab_set:
            try:
                self._window.grab_set()
            except tk.TclError:
                pass

        if self.config.transient:
            try:
                self._window.transient(
                    self.parent
                )
            except tk.TclError:
                pass

    def release_modal(self) -> None:
        """Release the dialog's modal grab."""

        if self._window is None:
            return

        try:
            self._window.grab_release()
        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    # Positioning
    # ------------------------------------------------------------------

    def center(self) -> None:
        """Center the dialog relative to its parent."""

        if self._window is None:
            return

        try:
            self._window.update_idletasks()

            width = self._window.winfo_width()
            height = self._window.winfo_height()

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
                    self._window.winfo_screenwidth()
                )

                screen_height = (
                    self._window.winfo_screenheight()
                )

                x = (
                    screen_width
                    - width
                ) // 2

                y = (
                    screen_height
                    - height
                ) // 2

            self._window.geometry(
                f"{width}x{height}"
                f"+{max(0, x)}"
                f"+{max(0, y)}"
            )

        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> bool:
        """
        Validate dialog state.

        Subclasses can override this method.
        """

        return True

    def validate_or_raise(self) -> None:
        """Validate the dialog or raise an exception."""

        try:
            valid = self.validate()
        except Exception as error:
            raise DialogValidationError(
                f"Dialog validation failed: {error}"
            ) from error

        if not valid:
            raise DialogValidationError(
                "Dialog validation failed."
            )

    # ------------------------------------------------------------------
    # Results
    # ------------------------------------------------------------------

    def set_result(
        self,
        result: DialogResult,
    ) -> None:
        """Set the current dialog result."""

        if not isinstance(
            result,
            DialogResult,
        ):
            raise TypeError(
                "result must be a DialogResult."
            )

        self._result = result

    def get_result(
        self,
    ) -> DialogResult:
        """Return the current result."""

        if self._result is None:
            return DialogResult.cancel()

        return self._result

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def bind(
        self,
        event: str,
        callback: Callable[..., Any],
    ) -> None:
        """
        Register a callback for a dialog event.
        """

        if not isinstance(
            event,
            str,
        ):
            raise TypeError(
                "event must be a string."
            )

        if not event.strip():
            raise ValueError(
                "event cannot be empty."
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
        callback: Callable[..., Any] | None = None,
    ) -> None:
        """
        Remove dialog event callbacks.

        If callback is None, all callbacks for the
        event are removed.
        """

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
        """
        Execute callbacks registered for an event.
        """

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
    # Metadata
    # ------------------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Store dialog metadata."""

        if not isinstance(
            key,
            str,
        ):
            raise TypeError(
                "Metadata key must be a string."
            )

        key = key.strip()

        if not key:
            raise ValueError(
                "Metadata key cannot be empty."
            )

        self._metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Retrieve dialog metadata."""

        return self._metadata.get(
            key,
            default,
        )

    def metadata(
        self,
    ) -> dict[str, Any]:
        """Return a copy of all dialog metadata."""

        return dict(
            self._metadata
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def require_initialized(self) -> None:
        """Ensure that the dialog has been built."""

        if not self._initialized:
            raise DialogStateError(
                "Dialog has not been initialized."
            )

    def focus(self) -> None:
        """Give focus to the dialog."""

        self.require_initialized()

        try:
            self._window.focus_set()
        except tk.TclError:
            pass

    def update(self) -> None:
        """Process pending GUI updates."""

        self.require_initialized()

        try:
            self._window.update_idletasks()
        except tk.TclError:
            pass

    def __enter__(self) -> "BaseDialog":
        """Enter a dialog context manager."""

        self.build()

        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:
        """Close the dialog context manager."""

        if not self._closed:
            self.close()

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""

        return (
            f"{self.__class__.__name__}("
            f"initialized={self.initialized}, "
            f"closed={self.closed}, "
            f"result={self.result!r}"
            f")"
        )


# ---------------------------------------------------------------------------
# Message Dialog Helpers
# ---------------------------------------------------------------------------


def show_info(
    parent: Any,
    title: str,
    message: str,
) -> None:
    """
    Display an informational message box.
    """

    require_tkinter()

    messagebox.showinfo(
        normalize_title(title),
        str(message),
        parent=parent,
    )


def show_success(
    parent: Any,
    title: str,
    message: str,
) -> None:
    """
    Display a success message box.
    """

    require_tkinter()

    messagebox.showinfo(
        normalize_title(title),
        str(message),
        parent=parent,
    )


def show_warning(
    parent: Any,
    title: str,
    message: str,
) -> None:
    """
    Display a warning message box.
    """

    require_tkinter()

    messagebox.showwarning(
        normalize_title(title),
        str(message),
        parent=parent,
    )


def show_error(
    parent: Any,
    title: str,
    message: str,
) -> None:
    """
    Display an error message box.
    """

    require_tkinter()

    messagebox.showerror(
        normalize_title(title),
        str(message),
        parent=parent,
    )


# ---------------------------------------------------------------------------
# Confirmation Dialog Helpers
# ---------------------------------------------------------------------------


def ask_yes_no(
    parent: Any,
    title: str,
    message: str,
) -> bool:
    """
    Ask the user a yes/no question.

    Returns True when the user selects Yes.
    """

    require_tkinter()

    return bool(
        messagebox.askyesno(
            normalize_title(title),
            str(message),
            parent=parent,
        )
    )


def ask_ok_cancel(
    parent: Any,
    title: str,
    message: str,
) -> bool:
    """
    Ask the user for OK/Cancel confirmation.

    Returns True when OK is selected.
    """

    require_tkinter()

    return bool(
        messagebox.askokcancel(
            normalize_title(title),
            str(message),
            parent=parent,
        )
    )


def ask_retry_cancel(
    parent: Any,
    title: str,
    message: str,
) -> bool:
    """
    Ask the user whether to retry or cancel.

    Returns True when Retry is selected.
    """

    require_tkinter()

    return bool(
        messagebox.askretrycancel(
            normalize_title(title),
            str(message),
            parent=parent,
        )
    )


# ---------------------------------------------------------------------------
# Input Dialog Helpers
# ---------------------------------------------------------------------------


def ask_string(
    parent: Any,
    title: str,
    prompt: str,
    *,
    initialvalue: str | None = None,
) -> str | None:
    """
    Ask the user for a string value.
    """

    require_tkinter()

    return simpledialog.askstring(
        normalize_title(title),
        str(prompt),
        parent=parent,
        initialvalue=initialvalue,
    )


def ask_integer(
    parent: Any,
    title: str,
    prompt: str,
    *,
    initialvalue: int | None = None,
    minvalue: int | None = None,
    maxvalue: int | None = None,
) -> int | None:
    """
    Ask the user for an integer.
    """

    require_tkinter()

    return simpledialog.askinteger(
        normalize_title(title),
        str(prompt),
        parent=parent,
        initialvalue=initialvalue,
        minvalue=minvalue,
        maxvalue=maxvalue,
    )


def ask_float(
    parent: Any,
    title: str,
    prompt: str,
    *,
    initialvalue: float | None = None,
    minvalue: float | None = None,
    maxvalue: float | None = None,
) -> float | None:
    """
    Ask the user for a floating-point value.
    """

    require_tkinter()

    return simpledialog.askfloat(
        normalize_title(title),
        str(prompt),
        parent=parent,
        initialvalue=initialvalue,
        minvalue=minvalue,
        maxvalue=maxvalue,
    )

# ---------------------------------------------------------------------------
# File Dialog Helpers
# ---------------------------------------------------------------------------


def ask_open_file(
    parent: Any,
    title: str = "Open File",
    *,
    initialdir: str | Path | None = None,
    initialfile: str | None = None,
    filetypes: Sequence[
        tuple[str, str]
    ] | None = None,
    defaultextension: str | None = None,
    multiple: bool = False,
) -> str | tuple[str, ...] | None:
    """
    Display a file-open dialog.

    Parameters
    ----------
    parent:
        Parent GUI window.

    title:
        Dialog title.

    initialdir:
        Directory shown when the dialog opens.

    initialfile:
        Initial filename.

    filetypes:
        File type filters.

    defaultextension:
        Default file extension.

    multiple:
        Whether multiple files may be selected.

    Returns
    -------
    str | tuple[str, ...] | None
        Selected file path(s), or None when cancelled.
    """

    require_tkinter()

    options: dict[str, Any] = {
        "parent": parent,
        "title": title,
    }

    if initialdir is not None:
        options["initialdir"] = str(
            initialdir
        )

    if initialfile is not None:
        options["initialfile"] = initialfile

    if filetypes is not None:
        options["filetypes"] = list(
            filetypes
        )

    if defaultextension is not None:
        options["defaultextension"] = (
            defaultextension
        )

    if multiple:
        return filedialog.askopenfilenames(
            **options
        )

    selected = filedialog.askopenfilename(
        **options
    )

    return selected or None


def ask_save_file(
    parent: Any,
    title: str = "Save File",
    *,
    initialdir: str | Path | None = None,
    initialfile: str | None = None,
    filetypes: Sequence[
        tuple[str, str]
    ] | None = None,
    defaultextension: str | None = None,
) -> str | None:
    """
    Display a file-save dialog.

    Returns the selected destination path,
    or None when cancelled.
    """

    require_tkinter()

    options: dict[str, Any] = {
        "parent": parent,
        "title": title,
    }

    if initialdir is not None:
        options["initialdir"] = str(
            initialdir
        )

    if initialfile is not None:
        options["initialfile"] = initialfile

    if filetypes is not None:
        options["filetypes"] = list(
            filetypes
        )

    if defaultextension is not None:
        options["defaultextension"] = (
            defaultextension
        )

    selected = filedialog.asksaveasfilename(
        **options
    )

    return selected or None


def ask_directory(
    parent: Any,
    title: str = "Select Directory",
    *,
    initialdir: str | Path | None = None,
    mustexist: bool = True,
) -> str | None:
    """
    Display a directory-selection dialog.

    Returns the selected directory,
    or None when cancelled.
    """

    require_tkinter()

    options: dict[str, Any] = {
        "parent": parent,
        "title": title,
        "mustexist": mustexist,
    }

    if initialdir is not None:
        options["initialdir"] = str(
            initialdir
        )

    selected = filedialog.askdirectory(
        **options
    )

    return selected or None


# ---------------------------------------------------------------------------
# File Dialog Result Helpers
# ---------------------------------------------------------------------------


def open_file_result(
    parent: Any,
    title: str = "Open File",
    **kwargs: Any,
) -> DialogResult:
    """
    Open a file-selection dialog and return
    the result as a DialogResult.
    """

    selected = ask_open_file(
        parent,
        title,
        **kwargs,
    )

    if not selected:
        return DialogResult.cancel()

    return DialogResult.ok(
        value=selected
    )


def save_file_result(
    parent: Any,
    title: str = "Save File",
    **kwargs: Any,
) -> DialogResult:
    """
    Open a save-file dialog and return
    the result as a DialogResult.
    """

    selected = ask_save_file(
        parent,
        title,
        **kwargs,
    )

    if not selected:
        return DialogResult.cancel()

    return DialogResult.ok(
        value=selected
    )


def directory_result(
    parent: Any,
    title: str = "Select Directory",
    **kwargs: Any,
) -> DialogResult:
    """
    Open a directory-selection dialog and return
    the result as a DialogResult.
    """

    selected = ask_directory(
        parent,
        title,
        **kwargs,
    )

    if not selected:
        return DialogResult.cancel()

    return DialogResult.ok(
        value=selected
    )


# ---------------------------------------------------------------------------
# File Type Presets
# ---------------------------------------------------------------------------


TEXT_FILETYPES = (
    ("Text Files", "*.txt"),
    ("All Files", "*.*"),
)


JSON_FILETYPES = (
    ("JSON Files", "*.json"),
    ("All Files", "*.*"),
)


PYTHON_FILETYPES = (
    ("Python Files", "*.py"),
    ("All Files", "*.*"),
)


CRYPTO_FILETYPES = (
    (
        "Text Files",
        "*.txt",
    ),
    (
        "Encrypted Files",
        "*.enc",
    ),
    (
        "JSON Files",
        "*.json",
    ),
    (
        "All Files",
        "*.*",
    ),
)


REPORT_FILETYPES = (
    (
        "Text Reports",
        "*.txt",
    ),
    (
        "Markdown Reports",
        "*.md",
    ),
    (
        "HTML Files",
        "*.html",
    ),
    (
        "JSON Files",
        "*.json",
    ),
    (
        "All Files",
        "*.*",
    ),
)


# ---------------------------------------------------------------------------
# Text Input Dialog
# ---------------------------------------------------------------------------


class TextInputDialog(BaseDialog):
    """
    Dialog for collecting a text value from the user.

    Supports:

    - Labels
    - Single-line text entry
    - Initial values
    - Required input
    - Custom validation
    - OK/Cancel actions
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        prompt: str = "Enter a value:",
        initial_value: str = "",
        required: bool = False,
        validator: Callable[
            [str],
            bool,
        ] | None = None,
        validator_message: str = (
            "The entered value is invalid."
        ),
        config: DialogConfig | None = None,
    ) -> None:
        """Initialize the text input dialog."""

        super().__init__(
            parent,
            config=config,
        )

        self.prompt = prompt
        self.initial_value = initial_value

        self.required = required
        self.validator = validator
        self.validator_message = (
            validator_message
        )

        self.entry: Any = None
        self.error_label: Any = None

        self._value = initial_value

    def build(self) -> Any:
        """Build the text input dialog."""

        window = super().build()

        if ttk is None:
            raise DialogConfigurationError(
                "ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=self.config.padding,
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

        prompt_label = ttk.Label(
            container,
            text=self.prompt,
        )

        prompt_label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 8),
        )

        self.entry = ttk.Entry(
            container,
        )

        self.entry.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.entry.insert(
            0,
            self.initial_value,
        )

        self.error_label = ttk.Label(
            container,
            text="",
        )

        self.error_label.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(8, 0),
        )

        button_frame = ttk.Frame(
            container,
        )

        button_frame.grid(
            row=3,
            column=0,
            sticky="e",
            pady=(12, 0),
        )

        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
        )

        cancel_button.pack(
            side="right",
            padx=(8, 0),
        )

        ok_button = ttk.Button(
            button_frame,
            text="OK",
            command=self.accept,
        )

        ok_button.pack(
            side="right",
        )

        self.entry.bind(
            "<Return>",
            self._on_enter,
        )

        self.entry.bind(
            "<Escape>",
            self._on_escape,
        )

        self.focus()

        self.entry.selection_range(
            0,
            tk.END,
        )

        return window

    def _on_enter(
        self,
        event: Any = None,
    ) -> str:
        """Handle the Enter key."""

        self.accept()

        return "break"

    def _on_escape(
        self,
        event: Any = None,
    ) -> str:
        """Handle the Escape key."""

        self.cancel()

        return "break"

    def get_value(self) -> str:
        """Return the current input value."""

        if self.entry is None:
            return self._value

        return self.entry.get()

    def validate(self) -> bool:
        """Validate the entered text."""

        value = self.get_value()

        if self.required and not value.strip():
            self.show_validation_error(
                "This field is required."
            )

            return False

        if self.validator is not None:
            try:
                valid = self.validator(
                    value
                )
            except Exception as error:
                self.show_validation_error(
                    str(error)
                )

                return False

            if not valid:
                self.show_validation_error(
                    self.validator_message
                )

                return False

        self.clear_validation_error()

        return True

    def show_validation_error(
        self,
        message: str,
    ) -> None:
        """Display a validation error."""

        if self.error_label is not None:
            self.error_label.configure(
                text=message
            )

    def clear_validation_error(self) -> None:
        """Clear the validation error."""

        if self.error_label is not None:
            self.error_label.configure(
                text=""
            )

    def accept(self) -> DialogResult:
        """Accept the entered value."""

        if not self.validate():
            return DialogResult.cancel()

        self._value = self.get_value()

        result = DialogResult.ok(
            value=self._value
        )

        return self.close(
            result
        )


# ---------------------------------------------------------------------------
# Password Input Dialog
# ---------------------------------------------------------------------------


class PasswordInputDialog(TextInputDialog):
    """
    Specialized text input dialog for passwords,
    keys, and other sensitive values.
    """

    def build(self) -> Any:
        """Build the password input dialog."""

        window = super().build()

        if self.entry is not None:
            self.entry.configure(
                show="*"
            )

        return window


# ---------------------------------------------------------------------------
# Multiline Text Dialog
# ---------------------------------------------------------------------------


class MultilineTextDialog(BaseDialog):
    """
    Dialog for entering or editing multiline text.

    Useful for:

    - Plaintext messages
    - Ciphertext
    - Notes
    - Encryption keys
    - Sample data
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        title: str = "Text Input",
        prompt: str = "Enter text:",
        initial_value: str = "",
        required: bool = False,
        validator: Callable[
            [str],
            bool,
        ] | None = None,
        validator_message: str = (
            "The entered text is invalid."
        ),
        height: int = 280,
        width: int = 520,
    ) -> None:
        """Initialize the multiline text dialog."""

        config = DialogConfig(
            title=title,
            width=width,
            height=height,
        )

        super().__init__(
            parent,
            config=config,
        )

        self.prompt = prompt
        self.initial_value = initial_value

        self.required = required
        self.validator = validator
        self.validator_message = (
            validator_message
        )

        self.text_widget: Any = None
        self.error_label: Any = None

    def build(self) -> Any:
        """Build the multiline text dialog."""

        window = super().build()

        if ttk is None or tk is None:
            raise DialogConfigurationError(
                "Tkinter/ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=self.config.padding,
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

        prompt_label = ttk.Label(
            container,
            text=self.prompt,
        )

        prompt_label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 8),
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
            undo=True,
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

        self.text_widget.insert(
            "1.0",
            self.initial_value,
        )

        self.error_label = ttk.Label(
            container,
            text="",
        )

        self.error_label.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(8, 0),
        )

        button_frame = ttk.Frame(
            container,
        )

        button_frame.grid(
            row=3,
            column=0,
            sticky="e",
            pady=(12, 0),
        )

        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
        )

        cancel_button.pack(
            side="right",
            padx=(8, 0),
        )

        ok_button = ttk.Button(
            button_frame,
            text="OK",
            command=self.accept,
        )

        ok_button.pack(
            side="right",
        )

        self.text_widget.bind(
            "<Control-Return>",
            self._on_accept,
        )

        self.text_widget.bind(
            "<Escape>",
            self._on_escape,
        )

        self.focus()

        return window

    def _on_accept(
        self,
        event: Any = None,
    ) -> str:
        """Handle Ctrl+Enter."""

        self.accept()

        return "break"

    def _on_escape(
        self,
        event: Any = None,
    ) -> str:
        """Handle Escape."""

        self.cancel()

        return "break"

    def get_value(self) -> str:
        """Return the entered multiline text."""

        if self.text_widget is None:
            return ""

        return self.text_widget.get(
            "1.0",
            "end-1c",
        )

    def validate(self) -> bool:
        """Validate the multiline input."""

        value = self.get_value()

        if self.required and not value.strip():
            self.show_validation_error(
                "This field is required."
            )

            return False

        if self.validator is not None:
            try:
                valid = self.validator(
                    value
                )
            except Exception as error:
                self.show_validation_error(
                    str(error)
                )

                return False

            if not valid:
                self.show_validation_error(
                    self.validator_message
                )

                return False

        self.clear_validation_error()

        return True

    def show_validation_error(
        self,
        message: str,
    ) -> None:
        """Display a validation error."""

        if self.error_label is not None:
            self.error_label.configure(
                text=message
            )

    def clear_validation_error(self) -> None:
        """Clear validation errors."""

        if self.error_label is not None:
            self.error_label.configure(
                text=""
            )

    def accept(self) -> DialogResult:
        """Accept the entered text."""

        if not self.validate():
            return DialogResult.cancel()

        return self.close(
            DialogResult.ok(
                value=self.get_value()
            )
        )

    # ---------------------------------------------------------------------------
# Confirmation Dialog
# ---------------------------------------------------------------------------


class ConfirmationDialog(BaseDialog):
    """
    Reusable yes/no confirmation dialog.

    Useful for destructive or irreversible actions such as:

    - Deleting files
    - Clearing history
    - Overwriting encrypted files
    - Resetting settings
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        title: str = "Confirm Action",
        message: str = "Are you sure?",
        confirm_text: str = "Yes",
        cancel_text: str = "No",
        destructive: bool = False,
    ) -> None:
        """Initialize the confirmation dialog."""

        config = DialogConfig(
            title=title,
            width=420,
            height=190,
        )

        super().__init__(
            parent,
            config=config,
        )

        self.message = message
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        self.destructive = destructive

    def build(self) -> Any:
        """Build the confirmation dialog."""

        window = super().build()

        if ttk is None:
            raise DialogConfigurationError(
                "ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=self.config.padding,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        container.columnconfigure(
            0,
            weight=1,
        )

        message_label = ttk.Label(
            container,
            text=self.message,
            wraplength=380,
            justify="left",
        )

        message_label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 20),
        )

        button_frame = ttk.Frame(
            container,
        )

        button_frame.grid(
            row=1,
            column=0,
            sticky="e",
        )

        cancel_button = ttk.Button(
            button_frame,
            text=self.cancel_text,
            command=self.cancel,
        )

        cancel_button.pack(
            side="right",
            padx=(8, 0),
        )

        confirm_button = ttk.Button(
            button_frame,
            text=self.confirm_text,
            command=self.confirm,
        )

        confirm_button.pack(
            side="right",
        )

        self.focus()

        return window

    def confirm(self) -> DialogResult:
        """Confirm the requested action."""

        return self.close(
            DialogResult.yes()
        )


# ---------------------------------------------------------------------------
# Selection Dialog
# ---------------------------------------------------------------------------


class SelectionDialog(BaseDialog):
    """
    Dialog for selecting one item from a collection.
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        title: str = "Select Item",
        prompt: str = "Select an item:",
        items: Sequence[Any] = (),
        initial_index: int = 0,
        height: int = 300,
    ) -> None:
        """Initialize the selection dialog."""

        config = DialogConfig(
            title=title,
            width=420,
            height=height,
        )

        super().__init__(
            parent,
            config=config,
        )

        self.prompt = prompt
        self.items = list(items)
        self.initial_index = initial_index

        self.listbox: Any = None

    def build(self) -> Any:
        """Build the selection dialog."""

        window = super().build()

        if ttk is None or tk is None:
            raise DialogConfigurationError(
                "Tkinter/ttk is unavailable."
            )

        container = ttk.Frame(
            window,
            padding=self.config.padding,
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

        prompt_label = ttk.Label(
            container,
            text=self.prompt,
        )

        prompt_label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 8),
        )

        list_frame = ttk.Frame(
            container,
        )

        list_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        list_frame.columnconfigure(
            0,
            weight=1,
        )

        list_frame.rowconfigure(
            0,
            weight=1,
        )

        self.listbox = tk.Listbox(
            list_frame,
            exportselection=False,
        )

        self.listbox.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.listbox.yview,
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        self.listbox.configure(
            yscrollcommand=scrollbar.set
        )

        for item in self.items:
            self.listbox.insert(
                tk.END,
                str(item),
            )

        if self.items:
            index = min(
                max(
                    self.initial_index,
                    0,
                ),
                len(self.items) - 1,
            )

            self.listbox.selection_set(
                index
            )

            self.listbox.activate(
                index
            )

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
            text="Cancel",
            command=self.cancel,
        ).pack(
            side="right",
            padx=(8, 0),
        )

        ttk.Button(
            button_frame,
            text="Select",
            command=self.accept,
        ).pack(
            side="right",
        )

        self.listbox.bind(
            "<Double-Button-1>",
            self._on_double_click,
        )

        self.listbox.bind(
            "<Return>",
            self._on_return,
        )

        self.listbox.bind(
            "<Escape>",
            self._on_escape,
        )

        self.focus()

        return window

    def get_selection(self) -> Any:
        """Return the currently selected item."""

        if self.listbox is None:
            return None

        selection = self.listbox.curselection()

        if not selection:
            return None

        index = selection[0]

        if index >= len(self.items):
            return None

        return self.items[index]

    def accept(self) -> DialogResult:
        """Accept the selected item."""

        selection = self.get_selection()

        if selection is None:
            return DialogResult.cancel()

        return self.close(
            DialogResult.ok(
                value=selection,
                index=self.listbox.curselection()[0],
            )
        )

    def _on_double_click(
        self,
        event: Any = None,
    ) -> str:
        """Accept a double-click selection."""

        self.accept()

        return "break"

    def _on_return(
        self,
        event: Any = None,
    ) -> str:
        """Accept the current selection."""

        self.accept()

        return "break"

    def _on_escape(
        self,
        event: Any = None,
    ) -> str:
        """Cancel the dialog."""

        self.cancel()

        return "break"


# ---------------------------------------------------------------------------
# Cipher Key Dialog
# ---------------------------------------------------------------------------


class CipherKeyDialog(TextInputDialog):
    """
    Dialog for collecting a cipher key.

    Supports optional validation and a minimum/maximum
    key length.
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        title: str = "Cipher Key",
        prompt: str = "Enter the cipher key:",
        initial_value: str = "",
        min_length: int | None = None,
        max_length: int | None = None,
        password: bool = False,
    ) -> None:
        """Initialize the cipher key dialog."""

        self.min_length = min_length
        self.max_length = max_length
        self.password = password

        super().__init__(
            parent,
            prompt=prompt,
            initial_value=initial_value,
            required=True,
            validator=self._validate_key,
            validator_message="Invalid cipher key.",
            config=DialogConfig(
                title=title,
                width=420,
                height=210,
            ),
        )

    def _validate_key(
        self,
        value: str,
    ) -> bool:
        """Validate the cipher key."""

        if not value:
            return False

        if (
            self.min_length is not None
            and len(value) < self.min_length
        ):
            self.validator_message = (
                f"Key must contain at least "
                f"{self.min_length} characters."
            )

            return False

        if (
            self.max_length is not None
            and len(value) > self.max_length
        ):
            self.validator_message = (
                f"Key cannot contain more than "
                f"{self.max_length} characters."
            )

            return False

        return True

    def build(self) -> Any:
        """Build the cipher key dialog."""

        window = super().build()

        if self.password and self.entry is not None:
            self.entry.configure(
                show="*"
            )

        return window


# ---------------------------------------------------------------------------
# Cipher Text Dialog
# ---------------------------------------------------------------------------


class CipherTextDialog(MultilineTextDialog):
    """
    Dialog specialized for entering plaintext or ciphertext.
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        title: str = "Cipher Text",
        prompt: str = "Enter text:",
        initial_value: str = "",
        required: bool = True,
    ) -> None:
        """Initialize the cipher text dialog."""

        super().__init__(
            parent,
            title=title,
            prompt=prompt,
            initial_value=initial_value,
            required=required,
            width=620,
            height=360,
        )


# ---------------------------------------------------------------------------
# File Selection Dialog
# ---------------------------------------------------------------------------


class FileSelectionDialog:
    """
    High-level file selection interface for the GUI.

    Provides a single object-oriented interface around
    Tkinter's native file dialogs.
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        initial_directory: str | Path | None = None,
    ) -> None:
        """Initialize the file selection helper."""

        self.parent = parent

        self.initial_directory = (
            Path(initial_directory)
            if initial_directory is not None
            else None
        )

    def open(
        self,
        *,
        title: str = "Open File",
        filetypes: Sequence[
            tuple[str, str]
        ] | None = None,
        multiple: bool = False,
    ) -> str | tuple[str, ...] | None:
        """Open one or more files."""

        return ask_open_file(
            self.parent,
            title,
            initialdir=self.initial_directory,
            filetypes=filetypes,
            multiple=multiple,
        )

    def save(
        self,
        *,
        title: str = "Save File",
        filetypes: Sequence[
            tuple[str, str]
        ] | None = None,
        defaultextension: str | None = None,
    ) -> str | None:
        """Select a save destination."""

        return ask_save_file(
            self.parent,
            title,
            initialdir=self.initial_directory,
            filetypes=filetypes,
            defaultextension=defaultextension,
        )

    def directory(
        self,
        *,
        title: str = "Select Directory",
    ) -> str | None:
        """Select a directory."""

        return ask_directory(
            self.parent,
            title,
            initialdir=self.initial_directory,
        )

    def open_text(
        self,
        *,
        title: str = "Open Text File",
        multiple: bool = False,
    ) -> str | tuple[str, ...] | None:
        """Open text files."""

        return self.open(
            title=title,
            filetypes=TEXT_FILETYPES,
            multiple=multiple,
        )

    def save_text(
        self,
        *,
        title: str = "Save Text File",
    ) -> str | None:
        """Select a text-file destination."""

        return self.save(
            title=title,
            filetypes=TEXT_FILETYPES,
            defaultextension=".txt",
        )

    def open_encrypted(
        self,
        *,
        title: str = "Open Encrypted File",
        multiple: bool = False,
    ) -> str | tuple[str, ...] | None:
        """Open encrypted or cryptography-related files."""

        return self.open(
            title=title,
            filetypes=CRYPTO_FILETYPES,
            multiple=multiple,
        )

    def save_report(
        self,
        *,
        title: str = "Save Report",
    ) -> str | None:
        """Select a report destination."""

        return self.save(
            title=title,
            filetypes=REPORT_FILETYPES,
        )


# ---------------------------------------------------------------------------
# Convenience Dialog Functions
# ---------------------------------------------------------------------------


def ask_text(
    parent: Any,
    *,
    title: str = "Text Input",
    prompt: str = "Enter text:",
    initial_value: str = "",
    required: bool = False,
) -> DialogResult:
    """
    Show a text input dialog and return its result.
    """

    dialog = TextInputDialog(
        parent,
        prompt=prompt,
        initial_value=initial_value,
        required=required,
        config=DialogConfig(
            title=title,
        ),
    )

    return dialog.show()


def ask_password(
    parent: Any,
    *,
    title: str = "Password",
    prompt: str = "Enter password:",
    required: bool = True,
) -> DialogResult:
    """
    Show a password input dialog.
    """

    dialog = PasswordInputDialog(
        parent,
        prompt=prompt,
        required=required,
        config=DialogConfig(
            title=title,
        ),
    )

    return dialog.show()


def ask_multiline(
    parent: Any,
    *,
    title: str = "Text Input",
    prompt: str = "Enter text:",
    initial_value: str = "",
    required: bool = False,
) -> DialogResult:
    """
    Show a multiline text dialog.
    """

    dialog = MultilineTextDialog(
        parent,
        title=title,
        prompt=prompt,
        initial_value=initial_value,
        required=required,
    )

    return dialog.show()


def ask_confirmation(
    parent: Any,
    *,
    title: str = "Confirm Action",
    message: str = "Are you sure?",
    destructive: bool = False,
) -> bool:
    """
    Show a confirmation dialog.

    Returns True when the user confirms.
    """

    dialog = ConfirmationDialog(
        parent,
        title=title,
        message=message,
        destructive=destructive,
    )

    result = dialog.show()

    return result.result == RESULT_YES


def ask_selection(
    parent: Any,
    items: Sequence[Any],
    *,
    title: str = "Select Item",
    prompt: str = "Select an item:",
) -> DialogResult:
    """
    Show a selection dialog.
    """

    dialog = SelectionDialog(
        parent,
        title=title,
        prompt=prompt,
        items=items,
    )

    return dialog.show()


def ask_cipher_key(
    parent: Any,
    *,
    title: str = "Cipher Key",
    prompt: str = "Enter the cipher key:",
    initial_value: str = "",
    min_length: int | None = None,
    max_length: int | None = None,
    password: bool = False,
) -> DialogResult:
    """
    Show a cipher-key input dialog.
    """

    dialog = CipherKeyDialog(
        parent,
        title=title,
        prompt=prompt,
        initial_value=initial_value,
        min_length=min_length,
        max_length=max_length,
        password=password,
    )

    return dialog.show()


def ask_cipher_text(
    parent: Any,
    *,
    title: str = "Cipher Text",
    prompt: str = "Enter text:",
    initial_value: str = "",
) -> DialogResult:
    """
    Show a cipher-text input dialog.
    """

    dialog = CipherTextDialog(
        parent,
        title=title,
        prompt=prompt,
        initial_value=initial_value,
    )

    return dialog.show()


# ---------------------------------------------------------------------------
# Application-Specific Message Helpers
# ---------------------------------------------------------------------------


def show_encryption_success(
    parent: Any,
    *,
    message: str = (
        "The message was encrypted successfully."
    ),
) -> None:
    """Display an encryption success message."""

    show_success(
        parent,
        "Encryption Successful",
        message,
    )


def show_decryption_success(
    parent: Any,
    *,
    message: str = (
        "The message was decrypted successfully."
    ),
) -> None:
    """Display a decryption success message."""

    show_success(
        parent,
        "Decryption Successful",
        message,
    )


def show_file_saved(
    parent: Any,
    path: str | Path,
) -> None:
    """Display a file-saved notification."""

    show_success(
        parent,
        "File Saved",
        f"File saved successfully:\n{path}",
    )


def show_file_open_error(
    parent: Any,
    error: Exception | str,
) -> None:
    """Display a file-open error."""

    show_error(
        parent,
        "File Error",
        f"Unable to open the selected file.\n\n"
        f"Reason: {error}",
    )


def show_encryption_error(
    parent: Any,
    error: Exception | str,
) -> None:
    """Display an encryption error."""

    show_error(
        parent,
        "Encryption Error",
        f"Encryption failed.\n\n"
        f"Reason: {error}",
    )


def show_decryption_error(
    parent: Any,
    error: Exception | str,
) -> None:
    """Display a decryption error."""

    show_error(
        parent,
        "Decryption Error",
        f"Decryption failed.\n\n"
        f"Reason: {error}",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Exceptions
    "DialogError",
    "DialogConfigurationError",
    "DialogStateError",
    "DialogValidationError",

    # Constants
    "DIALOG_INFO",
    "DIALOG_WARNING",
    "DIALOG_ERROR",
    "DIALOG_SUCCESS",

    "RESULT_OK",
    "RESULT_CANCEL",
    "RESULT_YES",
    "RESULT_NO",
    "RESULT_RETRY",
    "RESULT_ABORT",

    "DEFAULT_DIALOG_WIDTH",
    "DEFAULT_DIALOG_HEIGHT",
    "DEFAULT_DIALOG_PADDING",

    "FILE_MODE_OPEN",
    "FILE_MODE_SAVE",
    "FILE_MODE_DIRECTORY",

    # Result / Configuration
    "DialogResult",
    "DialogConfig",

    # Base Dialog
    "BaseDialog",

    # Availability / Utilities
    "tkinter_available",
    "require_tkinter",
    "normalize_title",

    # Message Dialogs
    "show_info",
    "show_success",
    "show_warning",
    "show_error",

    # Confirmation Dialogs
    "ask_yes_no",
    "ask_ok_cancel",
    "ask_retry_cancel",

    # Input Dialogs
    "ask_string",
    "ask_integer",
    "ask_float",

    # File Dialogs
    "ask_open_file",
    "ask_save_file",
    "ask_directory",

    "open_file_result",
    "save_file_result",
    "directory_result",

    # File Type Presets
    "TEXT_FILETYPES",
    "JSON_FILETYPES",
    "PYTHON_FILETYPES",
    "CRYPTO_FILETYPES",
    "REPORT_FILETYPES",

    # Dialog Classes
    "TextInputDialog",
    "PasswordInputDialog",
    "MultilineTextDialog",
    "ConfirmationDialog",
    "SelectionDialog",
    "CipherKeyDialog",
    "CipherTextDialog",
    "FileSelectionDialog",

    # Convenience Functions
    "ask_text",
    "ask_password",
    "ask_multiline",
    "ask_confirmation",
    "ask_selection",
    "ask_cipher_key",
    "ask_cipher_text",

    # Application Messages
    "show_encryption_success",
    "show_decryption_success",
    "show_file_saved",
    "show_file_open_error",
    "show_encryption_error",
    "show_decryption_error",
]

