# widgets.py
# Reusable GUI widgets for the
# Cryptography Toolkit
#
# Provides shared interface components,
# styling support, validation hooks,
# status display, and widget utilities.


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping


try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # pragma: no cover
    tk = None
    ttk = None


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class WidgetError(Exception):
    """Base exception for GUI widget errors."""

    pass


class WidgetConfigurationError(WidgetError):
    """Raised when a widget is configured incorrectly."""

    pass


class WidgetStateError(WidgetError):
    """Raised when a widget is used in an invalid state."""

    pass


class WidgetValidationError(WidgetError):
    """Raised when widget input validation fails."""

    pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


DEFAULT_PADDING = 8
DEFAULT_BUTTON_WIDTH = 16
DEFAULT_ENTRY_WIDTH = 40
DEFAULT_TEXT_HEIGHT = 12
DEFAULT_TEXT_WIDTH = 60

STATE_NORMAL = "normal"
STATE_DISABLED = "disabled"
STATE_READONLY = "readonly"

ORIENTATION_HORIZONTAL = "horizontal"
ORIENTATION_VERTICAL = "vertical"


# ---------------------------------------------------------------------------
# Widget Configuration
# ---------------------------------------------------------------------------


@dataclass
class WidgetConfig:
    """
    Common configuration shared by toolkit widgets.
    """

    padding: int = DEFAULT_PADDING
    width: int | None = None
    height: int | None = None
    state: str = STATE_NORMAL
    tooltip: str | None = None
    visible: bool = True
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """Validate widget configuration."""

        if not isinstance(self.padding, int):
            raise TypeError(
                "padding must be an integer."
            )

        if self.padding < 0:
            raise ValueError(
                "padding cannot be negative."
            )

        if self.width is not None:
            if not isinstance(self.width, int):
                raise TypeError(
                    "width must be an integer or None."
                )

            if self.width <= 0:
                raise ValueError(
                    "width must be greater than zero."
                )

        if self.height is not None:
            if not isinstance(self.height, int):
                raise TypeError(
                    "height must be an integer or None."
                )

            if self.height <= 0:
                raise ValueError(
                    "height must be greater than zero."
                )

        valid_states = {
            STATE_NORMAL,
            STATE_DISABLED,
            STATE_READONLY,
        }

        if self.state not in valid_states:
            raise ValueError(
                f"Invalid widget state: {self.state}"
            )

        if self.tooltip is not None:
            if not isinstance(
                self.tooltip,
                str,
            ):
                raise TypeError(
                    "tooltip must be a string or None."
                )

        if not isinstance(
            self.visible,
            bool,
        ):
            raise TypeError(
                "visible must be a boolean."
            )


# ---------------------------------------------------------------------------
# Base Widget
# ---------------------------------------------------------------------------


class BaseWidget:
    """
    Base class for reusable Cryptography Toolkit widgets.

    This class provides common functionality for:

    - Widget configuration
    - State management
    - Visibility
    - Metadata
    - Event callbacks
    - Validation
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the base widget."""

        self.parent = parent

        self.config = (
            config
            if config is not None
            else WidgetConfig()
        )

        self._widget: Any = None
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

        self._visible = (
            self.config.visible
        )

        self._state = (
            self.config.state
        )

        self._initialized = False

        self._build_kwargs = dict(
            kwargs
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def widget(self) -> Any:
        """Return the underlying Tkinter widget."""

        return self._widget

    @property
    def state(self) -> str:
        """Return the current widget state."""

        return self._state

    @property
    def visible(self) -> bool:
        """Return whether the widget is visible."""

        return self._visible

    @property
    def initialized(self) -> bool:
        """Return whether the widget has been initialized."""

        return self._initialized

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def build(self) -> Any:
        """
        Build the underlying widget.

        Subclasses should override this method.
        """

        if self._initialized:
            return self._widget

        if tk is None:
            raise WidgetConfigurationError(
                "Tkinter is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._widget = tk.Frame(
            self.parent,
            **self._build_kwargs,
        )

        self._initialized = True

        self._apply_config()

        return self._widget

    def destroy(self) -> None:
        """Destroy the underlying widget."""

        if self._widget is not None:
            try:
                self._widget.destroy()
            except tk.TclError:
                pass

        self._widget = None
        self._initialized = False

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def configure(
        self,
        **options: Any,
    ) -> None:
        """
        Configure the underlying widget.
        """

        if self._widget is None:
            raise WidgetStateError(
                "Widget has not been built."
            )

        try:
            self._widget.configure(
                **options
            )
        except Exception as error:
            raise WidgetConfigurationError(
                f"Unable to configure widget: {error}"
            ) from error

    def _apply_config(self) -> None:
        """Apply the WidgetConfig to the widget."""

        if self._widget is None:
            return

        if self.config.width is not None:
            try:
                self._widget.configure(
                    width=self.config.width
                )
            except (
                tk.TclError,
                AttributeError,
            ):
                pass

        if self.config.height is not None:
            try:
                self._widget.configure(
                    height=self.config.height
                )
            except (
                tk.TclError,
                AttributeError,
            ):
                pass

        self.set_state(
            self.config.state
        )

        if self.config.visible:
            self.show()
        else:
            self.hide()

    # ------------------------------------------------------------------
    # State Management
    # ------------------------------------------------------------------

    def set_state(
        self,
        state: str,
    ) -> None:
        """
        Set the widget state.
        """

        valid_states = {
            STATE_NORMAL,
            STATE_DISABLED,
            STATE_READONLY,
        }

        if state not in valid_states:
            raise WidgetStateError(
                f"Invalid widget state: {state}"
            )

        self._state = state

        if self._widget is None:
            return

        try:
            self._widget.configure(
                state=state
            )
        except (
            tk.TclError,
            AttributeError,
        ):
            # Some Tkinter widgets do not
            # support every state option.
            pass

    def enable(self) -> None:
        """Enable the widget."""

        self.set_state(
            STATE_NORMAL
        )

    def disable(self) -> None:
        """Disable the widget."""

        self.set_state(
            STATE_DISABLED
        )

    def readonly(self) -> None:
        """Set the widget to read-only state."""

        self.set_state(
            STATE_READONLY
        )

    # ------------------------------------------------------------------
    # Visibility
    # ------------------------------------------------------------------

    def show(self) -> None:
        """Display the widget."""

        self._visible = True

        if self._widget is None:
            return

        try:
            self._widget.pack()
        except (
            tk.TclError,
            AttributeError,
        ):
            try:
                self._widget.grid()
            except (
                tk.TclError,
                AttributeError,
            ):
                pass

    def hide(self) -> None:
        """Hide the widget."""

        self._visible = False

        if self._widget is None:
            return

        try:
            self._widget.pack_forget()
        except (
            tk.TclError,
            AttributeError,
        ):
            try:
                self._widget.grid_remove()
            except (
                tk.TclError,
                AttributeError,
            ):
                pass

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Store arbitrary widget metadata."""

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
        """Retrieve widget metadata."""

        return self._metadata.get(
            key,
            default,
        )

    def remove_metadata(
        self,
        key: str,
    ) -> Any:
        """Remove and return widget metadata."""

        return self._metadata.pop(
            key,
            None,
        )

    def metadata(
        self,
    ) -> dict[str, Any]:
        """Return a copy of widget metadata."""

        return dict(
            self._metadata
        )

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def bind_event(
        self,
        event: str,
        callback: Callable[..., Any],
    ) -> None:
        """
        Register a callback for a widget event.
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

    def unbind_event(
        self,
        event: str,
        callback: Callable[..., Any] | None = None,
    ) -> None:
        """
        Remove callbacks from a widget event.

        If callback is None, all callbacks for
        the specified event are removed.
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

    def emit_event(
        self,
        event: str,
        *args: Any,
        **kwargs: Any,
    ) -> list[Any]:
        """
        Execute all callbacks registered for an event.
        """

        results = []

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
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> bool:
        """
        Validate the widget.

        Subclasses can override this method.
        """

        return True

    def require_initialized(self) -> None:
        """Ensure the widget has been built."""

        if not self._initialized:
            raise WidgetStateError(
                "Widget has not been initialized."
            )

    # ------------------------------------------------------------------
    # Utility Methods
    # ------------------------------------------------------------------

    def pack(
        self,
        **kwargs: Any,
    ) -> None:
        """Pack the underlying widget."""

        self.require_initialized()

        self._widget.pack(
            **kwargs
        )

        self._visible = True

    def grid(
        self,
        **kwargs: Any,
    ) -> None:
        """Grid the underlying widget."""

        self.require_initialized()

        self._widget.grid(
            **kwargs
        )

        self._visible = True

    def place(
        self,
        **kwargs: Any,
    ) -> None:
        """Place the underlying widget."""

        self.require_initialized()

        self._widget.place(
            **kwargs
        )

        self._visible = True

    def focus(self) -> None:
        """Give keyboard focus to the widget."""

        self.require_initialized()

        try:
            self._widget.focus_set()
        except (
            tk.TclError,
            AttributeError,
        ):
            pass

    def update(self) -> None:
        """Update the widget and process pending GUI events."""

        self.require_initialized()

        try:
            self._widget.update_idletasks()
        except (
            tk.TclError,
            AttributeError,
        ):
            pass

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""

        return (
            f"{self.__class__.__name__}("
            f"initialized={self.initialized}, "
            f"visible={self.visible}, "
            f"state='{self.state}'"
            f")"
        )

    # ---------------------------------------------------------------------------
# Label Widget
# ---------------------------------------------------------------------------


class LabelWidget(BaseWidget):
    """
    Reusable label widget for displaying text.
    """

    def __init__(
        self,
        parent: Any = None,
        text: str = "",
        *,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a label widget."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        self._text = str(text)

    def build(self) -> Any:
        """Build the label widget."""

        if self._initialized:
            return self._widget

        if tk is None:
            raise WidgetConfigurationError(
                "Tkinter is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._widget = tk.Label(
            self.parent,
            text=self._text,
            **self._build_kwargs,
        )

        self._initialized = True

        self._apply_config()

        return self._widget

    def set_text(
        self,
        text: str,
    ) -> None:
        """Update the label text."""

        self._text = str(text)

        if self._widget is not None:
            self._widget.configure(
                text=self._text
            )

    def get_text(self) -> str:
        """Return the current label text."""

        return self._text


# ---------------------------------------------------------------------------
# Entry Widget
# ---------------------------------------------------------------------------


class EntryWidget(BaseWidget):
    """
    Reusable single-line text input widget.
    """

    def __init__(
        self,
        parent: Any = None,
        value: str = "",
        *,
        config: WidgetConfig | None = None,
        validator: Callable[
            [str],
            bool,
        ] | None = None,
        placeholder: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize an entry widget."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        self._value = str(value)
        self._validator = validator
        self._placeholder = placeholder
        self._placeholder_active = False

    def build(self) -> Any:
        """Build the entry widget."""

        if self._initialized:
            return self._widget

        if tk is None:
            raise WidgetConfigurationError(
                "Tkinter is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._widget = tk.Entry(
            self.parent,
            width=(
                self.config.width
                if self.config.width is not None
                else DEFAULT_ENTRY_WIDTH
            ),
            **self._build_kwargs,
        )

        self._initialized = True

        self._apply_config()

        if self._value:
            self.set_value(
                self._value
            )
        elif self._placeholder:
            self._set_placeholder()

        return self._widget

    def set_value(
        self,
        value: Any,
    ) -> None:
        """Set the entry value."""

        value = str(value)

        if self._validator is not None:
            try:
                valid = self._validator(
                    value
                )
            except Exception as error:
                raise WidgetValidationError(
                    f"Validation failed: {error}"
                ) from error

            if not valid:
                raise WidgetValidationError(
                    "The supplied value is invalid."
                )

        self._value = value
        self._placeholder_active = False

        if self._widget is not None:
            self._widget.delete(
                0,
                tk.END,
            )

            self._widget.insert(
                0,
                value,
            )

    def get_value(self) -> str:
        """Return the current entry value."""

        if self._widget is not None:
            if self._placeholder_active:
                return ""

            self._value = self._widget.get()

        return self._value

    def clear(self) -> None:
        """Clear the entry."""

        self._value = ""

        if self._widget is not None:
            self._widget.delete(
                0,
                tk.END,
            )

            if self._placeholder:
                self._set_placeholder()

    def is_valid(self) -> bool:
        """Return whether the current value is valid."""

        value = self.get_value()

        if self._validator is None:
            return True

        try:
            return bool(
                self._validator(
                    value
                )
            )
        except Exception:
            return False

    def _set_placeholder(self) -> None:
        """Display the placeholder text."""

        if (
            self._widget is None
            or not self._placeholder
        ):
            return

        self._widget.delete(
            0,
            tk.END,
        )

        self._widget.insert(
            0,
            self._placeholder,
        )

        self._placeholder_active = True

    def focus(self) -> None:
        """Focus the entry and remove placeholder text."""

        super().focus()

        if self._placeholder_active:
            self._widget.delete(
                0,
                tk.END,
            )

            self._placeholder_active = False


# ---------------------------------------------------------------------------
# Text Widget
# ---------------------------------------------------------------------------


class TextWidget(BaseWidget):
    """
    Reusable multi-line text editor/display widget.
    """

    def __init__(
        self,
        parent: Any = None,
        text: str = "",
        *,
        config: WidgetConfig | None = None,
        wrap: str = "word",
        readonly: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize a text widget."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        self._text = str(text)
        self._wrap = wrap
        self._readonly = readonly

    def build(self) -> Any:
        """Build the text widget."""

        if self._initialized:
            return self._widget

        if tk is None:
            raise WidgetConfigurationError(
                "Tkinter is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        width = (
            self.config.width
            if self.config.width is not None
            else DEFAULT_TEXT_WIDTH
        )

        height = (
            self.config.height
            if self.config.height is not None
            else DEFAULT_TEXT_HEIGHT
        )

        self._widget = tk.Text(
            self.parent,
            width=width,
            height=height,
            wrap=self._wrap,
            **self._build_kwargs,
        )

        self._initialized = True

        self._apply_config()

        if self._text:
            self.set_text(
                self._text
            )

        if self._readonly:
            self.readonly()

        return self._widget

    def set_text(
        self,
        text: str,
    ) -> None:
        """Replace the text widget contents."""

        self._text = str(text)

        if self._widget is None:
            return

        previous_state = self._widget.cget(
            "state"
        )

        try:
            self._widget.configure(
                state=STATE_NORMAL
            )

            self._widget.delete(
                "1.0",
                tk.END,
            )

            self._widget.insert(
                "1.0",
                self._text,
            )

        finally:
            if self._readonly:
                self._widget.configure(
                    state=STATE_DISABLED
                )
            else:
                self._widget.configure(
                    state=previous_state
                )

    def get_text(self) -> str:
        """Return all text from the widget."""

        if self._widget is not None:
            self._text = self._widget.get(
                "1.0",
                tk.END,
            ).rstrip("\n")

        return self._text

    def append(
        self,
        text: str,
    ) -> None:
        """Append text to the end of the widget."""

        if self._widget is None:
            self._text += str(text)
            return

        previous_state = self._widget.cget(
            "state"
        )

        try:
            self._widget.configure(
                state=STATE_NORMAL
            )

            self._widget.insert(
                tk.END,
                str(text),
            )

        finally:
            if self._readonly:
                self._widget.configure(
                    state=STATE_DISABLED
                )
            else:
                self._widget.configure(
                    state=previous_state
                )

        self._text = self.get_text()

    def clear(self) -> None:
        """Clear all text."""

        self.set_text(
            ""
        )

    def line_count(self) -> int:
        """Return the approximate number of lines."""

        return len(
            self.get_text().splitlines()
        )


# ---------------------------------------------------------------------------
# Button Widget
# ---------------------------------------------------------------------------


class ButtonWidget(BaseWidget):
    """
    Reusable button widget with callback support.
    """

    def __init__(
        self,
        parent: Any = None,
        text: str = "Button",
        *,
        command: Callable[
            ...,
            Any,
        ] | None = None,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a button widget."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        self._text = str(text)
        self._command = command

    def build(self) -> Any:
        """Build the button widget."""

        if self._initialized:
            return self._widget

        if tk is None:
            raise WidgetConfigurationError(
                "Tkinter is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._widget = tk.Button(
            self.parent,
            text=self._text,
            width=(
                self.config.width
                if self.config.width is not None
                else DEFAULT_BUTTON_WIDTH
            ),
            command=self._handle_click,
            **self._build_kwargs,
        )

        self._initialized = True

        self._apply_config()

        return self._widget

    def _handle_click(self) -> None:
        """Handle button clicks."""

        self.emit_event(
            "click"
        )

        if self._command is not None:
            self._command()

    def set_text(
        self,
        text: str,
    ) -> None:
        """Update the button text."""

        self._text = str(text)

        if self._widget is not None:
            self._widget.configure(
                text=self._text
            )

    def get_text(self) -> str:
        """Return the button text."""

        return self._text

    def set_command(
        self,
        command: Callable[
            ...,
            Any,
        ] | None,
    ) -> None:
        """Set the button callback."""

        if command is not None:
            if not callable(
                command
            ):
                raise TypeError(
                    "command must be callable or None."
                )

        self._command = command


# ---------------------------------------------------------------------------
# Checkbutton Widget
# ---------------------------------------------------------------------------


class CheckBoxWidget(BaseWidget):
    """
    Reusable boolean checkbox widget.
    """

    def __init__(
        self,
        parent: Any = None,
        text: str = "",
        value: bool = False,
        *,
        command: Callable[
            [bool],
            Any,
        ] | None = None,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a checkbox widget."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        self._text = str(text)
        self._value = bool(value)
        self._command = command
        self._variable: Any = None

    def build(self) -> Any:
        """Build the checkbox widget."""

        if self._initialized:
            return self._widget

        if tk is None:
            raise WidgetConfigurationError(
                "Tkinter is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._variable = tk.BooleanVar(
            value=self._value
        )

        self._widget = tk.Checkbutton(
            self.parent,
            text=self._text,
            variable=self._variable,
            command=self._handle_toggle,
            **self._build_kwargs,
        )

        self._initialized = True

        self._apply_config()

        return self._widget

    def _handle_toggle(self) -> None:
        """Handle checkbox state changes."""

        self._value = bool(
            self._variable.get()
        )

        self.emit_event(
            "change",
            self._value,
        )

        if self._command is not None:
            self._command(
                self._value
            )

    def set_value(
        self,
        value: bool,
    ) -> None:
        """Set the checkbox state."""

        self._value = bool(
            value
        )

        if self._variable is not None:
            self._variable.set(
                self._value
            )

    def get_value(self) -> bool:
        """Return the current checkbox state."""

        if self._variable is not None:
            self._value = bool(
                self._variable.get()
            )

        return self._value

    def toggle(self) -> bool:
        """Toggle and return the checkbox state."""

        new_value = not self.get_value()

        self.set_value(
            new_value
        )

        return new_value


# ---------------------------------------------------------------------------
# Radio Button Widget
# ---------------------------------------------------------------------------


class RadioGroupWidget(BaseWidget):
    """
    Reusable group of radio buttons.

    All buttons in the group share a single selected value.
    """

    def __init__(
        self,
        parent: Any = None,
        options: Mapping[
            str,
            str,
        ] | None = None,
        value: str | None = None,
        *,
        command: Callable[
            [str],
            Any,
        ] | None = None,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a radio group."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        self._options = dict(
            options or {}
        )

        self._value = value
        self._command = command
        self._variable: Any = None
        self._buttons: dict[
            str,
            Any,
        ] = {}

    def build(self) -> Any:
        """Build the radio button group."""

        if self._initialized:
            return self._widget

        if tk is None:
            raise WidgetConfigurationError(
                "Tkinter is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._widget = tk.Frame(
            self.parent,
            **self._build_kwargs,
        )

        self._variable = tk.StringVar(
            value=(
                self._value
                if self._value is not None
                else ""
            )
        )

        self._initialized = True

        self._build_buttons()

        self._apply_config()

        return self._widget

    def _build_buttons(self) -> None:
        """Create radio buttons from configured options."""

        if self._widget is None:
            return

        for key, label in self._options.items():

            button = tk.Radiobutton(
                self._widget,
                text=label,
                value=key,
                variable=self._variable,
                command=self._handle_change,
            )

            button.pack(
                anchor="w",
                padx=self.config.padding,
                pady=2,
            )

            self._buttons[key] = button

    def _handle_change(self) -> None:
        """Handle radio selection changes."""

        self._value = self._variable.get()

        self.emit_event(
            "change",
            self._value,
        )

        if self._command is not None:
            self._command(
                self._value
            )

    def set_value(
        self,
        value: str,
    ) -> None:
        """Select a radio button."""

        if value not in self._options:
            raise ValueError(
                f"Unknown radio option: {value}"
            )

        self._value = value

        if self._variable is not None:
            self._variable.set(
                value
            )

    def get_value(self) -> str:
        """Return the selected value."""

        if self._variable is not None:
            self._value = (
                self._variable.get()
            )

        return self._value or ""

    def add_option(
        self,
        key: str,
        label: str,
    ) -> None:
        """Add a new radio option."""

        if not key:
            raise ValueError(
                "Radio option key cannot be empty."
            )

        self._options[key] = label

        if self._initialized:
            self.destroy()
            self.build()

    def remove_option(
        self,
        key: str,
    ) -> None:
        """Remove a radio option."""

        self._options.pop(
            key,
            None,
        )

        if self._value == key:
            self._value = None

        if self._initialized:
            self.destroy()
            self.build()

    # ---------------------------------------------------------------------------
# Combo Box Widget
# ---------------------------------------------------------------------------


class ComboBoxWidget(BaseWidget):
    """
    Reusable drop-down selection widget.
    """

    def __init__(
        self,
        parent: Any = None,
        options: list[str] | tuple[str, ...] | None = None,
        value: str | None = None,
        *,
        command: Callable[
            [str],
            Any,
        ] | None = None,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a combo box."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        self._options = list(
            options or []
        )

        self._value = value
        self._command = command
        self._variable: Any = None

    def build(self) -> Any:
        """Build the combo box."""

        if self._initialized:
            return self._widget

        if ttk is None:
            raise WidgetConfigurationError(
                "Tkinter ttk is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._variable = tk.StringVar(
            value=(
                self._value
                if self._value is not None
                else ""
            )
        )

        self._widget = ttk.Combobox(
            self.parent,
            textvariable=self._variable,
            values=self._options,
            state=STATE_READONLY,
            **self._build_kwargs,
        )

        self._widget.bind(
            "<<ComboboxSelected>>",
            self._handle_change,
        )

        self._initialized = True

        self._apply_config()

        return self._widget

    def _handle_change(
        self,
        event: Any = None,
    ) -> None:
        """Handle combo box selection changes."""

        self._value = self._variable.get()

        self.emit_event(
            "change",
            self._value,
        )

        if self._command is not None:
            self._command(
                self._value
            )

    def set_value(
        self,
        value: str,
    ) -> None:
        """Set the selected value."""

        if value not in self._options:
            raise ValueError(
                f"Unknown combo box value: {value}"
            )

        self._value = value

        if self._variable is not None:
            self._variable.set(
                value
            )

    def get_value(self) -> str:
        """Return the selected value."""

        if self._variable is not None:
            self._value = (
                self._variable.get()
            )

        return self._value or ""

    def set_options(
        self,
        options: list[str] | tuple[str, ...],
    ) -> None:
        """Replace all available options."""

        self._options = list(
            options
        )

        if self._widget is not None:
            self._widget["values"] = (
                self._options
            )

    def add_option(
        self,
        option: str,
    ) -> None:
        """Add an option."""

        option = str(
            option
        )

        if option not in self._options:
            self._options.append(
                option
            )

            if self._widget is not None:
                self._widget["values"] = (
                    self._options
                )

    def remove_option(
        self,
        option: str,
    ) -> None:
        """Remove an option."""

        if option in self._options:
            self._options.remove(
                option
            )

            if self._widget is not None:
                self._widget["values"] = (
                    self._options
                )

            if self._value == option:
                self._value = None
                self._variable.set("")


# ---------------------------------------------------------------------------
# Spin Box Widget
# ---------------------------------------------------------------------------


class SpinBoxWidget(BaseWidget):
    """
    Reusable numeric spin box widget.
    """

    def __init__(
        self,
        parent: Any = None,
        value: int = 0,
        *,
        minimum: int = 0,
        maximum: int = 100,
        increment: int = 1,
        command: Callable[
            [int],
            Any,
        ] | None = None,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a spin box."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        if minimum > maximum:
            raise ValueError(
                "minimum cannot be greater than maximum."
            )

        if increment <= 0:
            raise ValueError(
                "increment must be greater than zero."
            )

        self._minimum = minimum
        self._maximum = maximum
        self._increment = increment
        self._value = value
        self._command = command
        self._variable: Any = None

    def build(self) -> Any:
        """Build the spin box."""

        if self._initialized:
            return self._widget

        if ttk is None:
            raise WidgetConfigurationError(
                "Tkinter ttk is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._value = max(
            self._minimum,
            min(
                self._maximum,
                self._value,
            ),
        )

        self._variable = tk.IntVar(
            value=self._value
        )

        self._widget = tk.Spinbox(
            self.parent,
            from_=self._minimum,
            to=self._maximum,
            increment=self._increment,
            textvariable=self._variable,
            command=self._handle_change,
            **self._build_kwargs,
        )

        self._initialized = True

        self._apply_config()

        return self._widget

    def _handle_change(self) -> None:
        """Handle spin box value changes."""

        self._read_value()

        self.emit_event(
            "change",
            self._value,
        )

        if self._command is not None:
            self._command(
                self._value
            )

    def _read_value(self) -> None:
        """Read and normalize the current value."""

        try:
            value = int(
                self._variable.get()
            )
        except (
            ValueError,
            tk.TclError,
        ):
            value = self._minimum

        self._value = max(
            self._minimum,
            min(
                self._maximum,
                value,
            ),
        )

        if self._variable is not None:
            self._variable.set(
                self._value
            )

    def set_value(
        self,
        value: int,
    ) -> None:
        """Set the numeric value."""

        if not isinstance(
            value,
            int,
        ):
            raise TypeError(
                "Spin box value must be an integer."
            )

        if not (
            self._minimum
            <= value
            <= self._maximum
        ):
            raise ValueError(
                "Spin box value is outside "
                "the allowed range."
            )

        self._value = value

        if self._variable is not None:
            self._variable.set(
                value
            )

    def get_value(self) -> int:
        """Return the current numeric value."""

        if self._variable is not None:
            self._read_value()

        return self._value

    def set_range(
        self,
        minimum: int,
        maximum: int,
    ) -> None:
        """Update the allowed numeric range."""

        if minimum > maximum:
            raise ValueError(
                "minimum cannot be greater than maximum."
            )

        self._minimum = minimum
        self._maximum = maximum

        self._value = max(
            minimum,
            min(
                maximum,
                self._value,
            ),
        )

        if self._widget is not None:
            self._widget.configure(
                from_=minimum,
                to=maximum,
            )

        if self._variable is not None:
            self._variable.set(
                self._value
            )


# ---------------------------------------------------------------------------
# Progress Bar Widget
# ---------------------------------------------------------------------------


class ProgressWidget(BaseWidget):
    """
    Reusable progress bar widget.
    """

    def __init__(
        self,
        parent: Any = None,
        value: float = 0.0,
        *,
        maximum: float = 100.0,
        mode: str = "determinate",
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a progress widget."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        if maximum <= 0:
            raise ValueError(
                "maximum must be greater than zero."
            )

        if mode not in {
            "determinate",
            "indeterminate",
        }:
            raise ValueError(
                "mode must be 'determinate' "
                "or 'indeterminate'."
            )

        self._maximum = float(
            maximum
        )

        self._value = max(
            0.0,
            min(
                float(value),
                self._maximum,
            ),
        )

        self._mode = mode

    def build(self) -> Any:
        """Build the progress bar."""

        if ttk is None:
            raise WidgetConfigurationError(
                "Tkinter ttk is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._widget = ttk.Progressbar(
            self.parent,
            maximum=self._maximum,
            mode=self._mode,
            value=self._value,
            **self._build_kwargs,
        )

        self._initialized = True

        self._apply_config()

        return self._widget

    def set_value(
        self,
        value: float,
    ) -> None:
        """Set the progress value."""

        self._value = max(
            0.0,
            min(
                float(value),
                self._maximum,
            ),
        )

        if self._widget is not None:
            self._widget["value"] = (
                self._value
            )

    def get_value(self) -> float:
        """Return the current progress value."""

        if self._widget is not None:
            self._value = float(
                self._widget["value"]
            )

        return self._value

    def set_maximum(
        self,
        maximum: float,
    ) -> None:
        """Update the progress maximum."""

        if maximum <= 0:
            raise ValueError(
                "maximum must be greater than zero."
            )

        self._maximum = float(
            maximum
        )

        self._value = min(
            self._value,
            self._maximum,
        )

        if self._widget is not None:
            self._widget["maximum"] = (
                self._maximum
            )
            self._widget["value"] = (
                self._value
            )

    def reset(self) -> None:
        """Reset progress to zero."""

        self.set_value(
            0
        )

    def start(
        self,
        interval: int = 50,
    ) -> None:
        """Start indeterminate progress animation."""

        self.require_initialized()

        if self._mode != "indeterminate":
            return

        self._widget.start(
            interval
        )

    def stop(self) -> None:
        """Stop indeterminate progress animation."""

        self.require_initialized()

        if self._mode != "indeterminate":
            return

        self._widget.stop()


# ---------------------------------------------------------------------------
# Status Label Widget
# ---------------------------------------------------------------------------


class StatusWidget(LabelWidget):
    """
    Label specialized for displaying application status.
    """

    STATUS_INFO = "info"
    STATUS_SUCCESS = "success"
    STATUS_WARNING = "warning"
    STATUS_ERROR = "error"

    def __init__(
        self,
        parent: Any = None,
        text: str = "",
        *,
        status: str = STATUS_INFO,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a status widget."""

        super().__init__(
            parent,
            text=text,
            config=config,
            **kwargs,
        )

        self._status = status

        self._validate_status(
            status
        )

    def _validate_status(
        self,
        status: str,
    ) -> None:
        """Validate a status level."""

        valid_statuses = {
            self.STATUS_INFO,
            self.STATUS_SUCCESS,
            self.STATUS_WARNING,
            self.STATUS_ERROR,
        }

        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status: {status}"
            )

    def set_status(
        self,
        text: str,
        status: str = STATUS_INFO,
    ) -> None:
        """Update the status message."""

        self._validate_status(
            status
        )

        self._status = status

        self.set_text(
            text
        )

        if self._widget is not None:
            self._widget.configure(
                relief="flat"
            )

    def get_status(self) -> str:
        """Return the current status type."""

        return self._status

    def info(
        self,
        text: str,
    ) -> None:
        """Display an informational message."""

        self.set_status(
            text,
            self.STATUS_INFO,
        )

    def success(
        self,
        text: str,
    ) -> None:
        """Display a success message."""

        self.set_status(
            text,
            self.STATUS_SUCCESS,
        )

    def warning(
        self,
        text: str,
    ) -> None:
        """Display a warning message."""

        self.set_status(
            text,
            self.STATUS_WARNING,
        )

    def error(
        self,
        text: str,
    ) -> None:
        """Display an error message."""

        self.set_status(
            text,
            self.STATUS_ERROR,
        )


# ---------------------------------------------------------------------------
# Scrollable Frame
# ---------------------------------------------------------------------------


class ScrollableFrame(BaseWidget):
    """
    Reusable vertically scrollable frame.

    Useful for large forms, settings panels,
    analysis results, and other dynamic content.
    """

    def __init__(
        self,
        parent: Any = None,
        *,
        config: WidgetConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the scrollable frame."""

        super().__init__(
            parent,
            config=config,
            **kwargs,
        )

        self.canvas: Any = None
        self.scrollbar: Any = None
        self.content_frame: Any = None
        self._window_id: Any = None

    def build(self) -> Any:
        """Build the scrollable frame."""

        if self._initialized:
            return self._widget

        if tk is None:
            raise WidgetConfigurationError(
                "Tkinter is unavailable."
            )

        if self.parent is None:
            raise WidgetConfigurationError(
                "A parent widget is required."
            )

        self._widget = tk.Frame(
            self.parent,
            **self._build_kwargs,
        )

        self.canvas = tk.Canvas(
            self._widget,
            highlightthickness=0,
        )

        self.scrollbar = ttk.Scrollbar(
            self._widget,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.content_frame = tk.Frame(
            self.canvas
        )

        self._window_id = (
            self.canvas.create_window(
                (0, 0),
                window=self.content_frame,
                anchor="nw",
            )
        )

        self.canvas.configure(
            yscrollcommand=(
                self.scrollbar.set
            )
        )

        self.content_frame.bind(
            "<Configure>",
            self._on_content_configure,
        )

        self.canvas.bind(
            "<Configure>",
            self._on_canvas_configure,
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.scrollbar.pack(
            side="right",
            fill="y",
        )

        self._initialized = True

        self._apply_config()

        return self._widget

    def _on_content_configure(
        self,
        event: Any = None,
    ) -> None:
        """Update the scrollable region."""

        if self.canvas is None:
            return

        self.canvas.configure(
            scrollregion=self.canvas.bbox(
                "all"
            )
        )

    def _on_canvas_configure(
        self,
        event: Any = None,
    ) -> None:
        """Keep the content frame width synchronized."""

        if (
            self.canvas is None
            or self._window_id is None
        ):
            return

        self.canvas.itemconfigure(
            self._window_id,
            width=self.canvas.winfo_width(),
        )

    def scroll_to_top(self) -> None:
        """Scroll to the top."""

        self.require_initialized()

        self.canvas.yview_moveto(
            0
        )

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom."""

        self.require_initialized()

        self.canvas.yview_moveto(
            1
        )


# ---------------------------------------------------------------------------
# Widget Factory
# ---------------------------------------------------------------------------


def create_widget(
    widget_type: str,
    parent: Any,
    **kwargs: Any,
) -> BaseWidget:
    """
    Create a widget from a widget type name.
    """

    widget_map = {
        "label": LabelWidget,
        "entry": EntryWidget,
        "text": TextWidget,
        "button": ButtonWidget,
        "checkbox": CheckBoxWidget,
        "radio": RadioGroupWidget,
        "combobox": ComboBoxWidget,
        "spinbox": SpinBoxWidget,
        "progress": ProgressWidget,
        "status": StatusWidget,
        "scrollable": ScrollableFrame,
    }

    normalized = (
        widget_type.strip().lower()
        if isinstance(
            widget_type,
            str,
        )
        else ""
    )

    if normalized not in widget_map:
        raise ValueError(
            f"Unknown widget type: {widget_type}"
        )

    widget_class = widget_map[
        normalized
    ]

    return widget_class(
        parent,
        **kwargs,
    )


def validate_widget(
    widget: BaseWidget,
) -> bool:
    """
    Validate a widget instance.
    """

    if not isinstance(
        widget,
        BaseWidget,
    ):
        return False

    try:
        return bool(
            widget.validate()
        )
    except Exception:
        return False


def widget_available() -> bool:
    """
    Return whether Tkinter is available.
    """

    return (
        tk is not None
        and ttk is not None
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Exceptions
    "WidgetError",
    "WidgetConfigurationError",
    "WidgetStateError",
    "WidgetValidationError",

    # Constants
    "DEFAULT_PADDING",
    "DEFAULT_BUTTON_WIDTH",
    "DEFAULT_ENTRY_WIDTH",
    "DEFAULT_TEXT_HEIGHT",
    "DEFAULT_TEXT_WIDTH",

    "STATE_NORMAL",
    "STATE_DISABLED",
    "STATE_READONLY",

    "ORIENTATION_HORIZONTAL",
    "ORIENTATION_VERTICAL",

    # Configuration
    "WidgetConfig",

    # Base
    "BaseWidget",

    # Widgets
    "LabelWidget",
    "EntryWidget",
    "TextWidget",
    "ButtonWidget",
    "CheckBoxWidget",
    "RadioGroupWidget",
    "ComboBoxWidget",
    "SpinBoxWidget",
    "ProgressWidget",
    "StatusWidget",
    "ScrollableFrame",

    # Factory / Utilities
    "create_widget",
    "validate_widget",
    "widget_available",
]

