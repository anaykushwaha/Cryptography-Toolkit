# themes.py
# Theme and styling management for the
# Cryptography Toolkit GUI
#
# Provides centralized color palettes,
# fonts, widget styling, theme definitions,
# and theme management utilities.


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # pragma: no cover
    tk = None
    ttk = None


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ThemeError(Exception):
    """Base exception for GUI theme errors."""

    pass


class ThemeNotFoundError(ThemeError):
    """Raised when a requested theme does not exist."""

    pass


class ThemeConfigurationError(ThemeError):
    """Raised when a theme is configured incorrectly."""

    pass


# ---------------------------------------------------------------------------
# Color Palettes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ColorPalette:
    """
    Defines the colors used throughout a GUI theme.
    """

    background: str
    foreground: str

    surface: str
    surface_alt: str

    primary: str
    secondary: str
    accent: str

    success: str
    warning: str
    error: str
    info: str

    border: str
    disabled: str

    input_background: str
    input_foreground: str

    selection_background: str
    selection_foreground: str

    button_background: str
    button_foreground: str

    button_hover: str

    def as_dict(self) -> dict[str, str]:
        """Return the palette as a dictionary."""

        return {
            "background": self.background,
            "foreground": self.foreground,
            "surface": self.surface,
            "surface_alt": self.surface_alt,
            "primary": self.primary,
            "secondary": self.secondary,
            "accent": self.accent,
            "success": self.success,
            "warning": self.warning,
            "error": self.error,
            "info": self.info,
            "border": self.border,
            "disabled": self.disabled,
            "input_background": self.input_background,
            "input_foreground": self.input_foreground,
            "selection_background": (
                self.selection_background
            ),
            "selection_foreground": (
                self.selection_foreground
            ),
            "button_background": (
                self.button_background
            ),
            "button_foreground": (
                self.button_foreground
            ),
            "button_hover": self.button_hover,
        }


# ---------------------------------------------------------------------------
# Font Definitions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FontSet:
    """
    Defines the fonts used by the GUI.
    """

    family: str = "Segoe UI"

    normal_size: int = 10
    small_size: int = 9
    large_size: int = 12
    title_size: int = 20
    heading_size: int = 14
    monospace_size: int = 10

    normal_weight: str = "normal"
    heading_weight: str = "bold"

    monospace_family: str = "Consolas"

    def normal(self) -> tuple[str, int, str]:
        """Return the standard font definition."""

        return (
            self.family,
            self.normal_size,
            self.normal_weight,
        )

    def small(self) -> tuple[str, int, str]:
        """Return the small font definition."""

        return (
            self.family,
            self.small_size,
            self.normal_weight,
        )

    def large(self) -> tuple[str, int, str]:
        """Return the large font definition."""

        return (
            self.family,
            self.large_size,
            self.normal_weight,
        )

    def title(self) -> tuple[str, int, str]:
        """Return the title font definition."""

        return (
            self.family,
            self.title_size,
            self.heading_weight,
        )

    def heading(self) -> tuple[str, int, str]:
        """Return the heading font definition."""

        return (
            self.family,
            self.heading_size,
            self.heading_weight,
        )

    def monospace(self) -> tuple[str, int, str]:
        """Return the monospace font definition."""

        return (
            self.monospace_family,
            self.monospace_size,
            self.normal_weight,
        )


# ---------------------------------------------------------------------------
# Theme Definition
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ThemeDefinition:
    """
    Complete definition of a GUI theme.
    """

    name: str
    palette: ColorPalette
    fonts: FontSet = field(
        default_factory=FontSet
    )

    description: str = ""

    ttk_theme: str = "clam"

    border_width: int = 1
    relief: str = "flat"

    padding: int = 8

    def __post_init__(self) -> None:
        """Validate the theme definition."""

        if not self.name.strip():
            raise ThemeConfigurationError(
                "Theme name cannot be empty."
            )

        if self.border_width < 0:
            raise ThemeConfigurationError(
                "border_width cannot be negative."
            )

        if self.padding < 0:
            raise ThemeConfigurationError(
                "padding cannot be negative."
            )

    def as_dict(self) -> dict[str, Any]:
        """Return the complete theme as a dictionary."""

        return {
            "name": self.name,
            "palette": self.palette.as_dict(),
            "fonts": {
                "family": self.fonts.family,
                "normal_size": (
                    self.fonts.normal_size
                ),
                "small_size": (
                    self.fonts.small_size
                ),
                "large_size": (
                    self.fonts.large_size
                ),
                "title_size": (
                    self.fonts.title_size
                ),
                "heading_size": (
                    self.fonts.heading_size
                ),
                "monospace_size": (
                    self.fonts.monospace_size
                ),
                "monospace_family": (
                    self.fonts.monospace_family
                ),
            },
            "description": self.description,
            "ttk_theme": self.ttk_theme,
            "border_width": self.border_width,
            "relief": self.relief,
            "padding": self.padding,
        }


# ---------------------------------------------------------------------------
# Default Palettes
# ---------------------------------------------------------------------------


LIGHT_PALETTE = ColorPalette(
    background="#F5F7FA",
    foreground="#1F2937",

    surface="#FFFFFF",
    surface_alt="#E5E7EB",

    primary="#2563EB",
    secondary="#4B5563",
    accent="#7C3AED",

    success="#16A34A",
    warning="#D97706",
    error="#DC2626",
    info="#0284C7",

    border="#D1D5DB",
    disabled="#9CA3AF",

    input_background="#FFFFFF",
    input_foreground="#111827",

    selection_background="#2563EB",
    selection_foreground="#FFFFFF",

    button_background="#2563EB",
    button_foreground="#FFFFFF",

    button_hover="#1D4ED8",
)


DARK_PALETTE = ColorPalette(
    background="#111827",
    foreground="#F9FAFB",

    surface="#1F2937",
    surface_alt="#374151",

    primary="#3B82F6",
    secondary="#9CA3AF",
    accent="#8B5CF6",

    success="#22C55E",
    warning="#F59E0B",
    error="#EF4444",
    info="#38BDF8",

    border="#4B5563",
    disabled="#6B7280",

    input_background="#1F2937",
    input_foreground="#F9FAFB",

    selection_background="#3B82F6",
    selection_foreground="#FFFFFF",

    button_background="#2563EB",
    button_foreground="#FFFFFF",

    button_hover="#1D4ED8",
)


HIGH_CONTRAST_PALETTE = ColorPalette(
    background="#000000",
    foreground="#FFFFFF",

    surface="#000000",
    surface_alt="#1A1A1A",

    primary="#00FFFF",
    secondary="#FFFFFF",
    accent="#FFFF00",

    success="#00FF00",
    warning="#FFFF00",
    error="#FF0000",
    info="#00FFFF",

    border="#FFFFFF",
    disabled="#808080",

    input_background="#000000",
    input_foreground="#FFFFFF",

    selection_background="#FFFFFF",
    selection_foreground="#000000",

    button_background="#000000",
    button_foreground="#FFFFFF",

    button_hover="#333333",
)


# ---------------------------------------------------------------------------
# Default Themes
# ---------------------------------------------------------------------------


LIGHT_THEME = ThemeDefinition(
    name="light",
    palette=LIGHT_PALETTE,
    fonts=FontSet(),
    description=(
        "Clean light theme for everyday use."
    ),
)


DARK_THEME = ThemeDefinition(
    name="dark",
    palette=DARK_PALETTE,
    fonts=FontSet(),
    description=(
        "Dark theme designed for comfortable "
        "extended use."
    ),
)


HIGH_CONTRAST_THEME = ThemeDefinition(
    name="high_contrast",
    palette=HIGH_CONTRAST_PALETTE,
    fonts=FontSet(
        normal_size=11,
        small_size=10,
        large_size=13,
        title_size=22,
        heading_size=15,
        monospace_size=11,
    ),
    description=(
        "High-contrast theme designed for "
        "maximum visual readability."
    ),
)


DEFAULT_THEMES: dict[
    str,
    ThemeDefinition,
] = {
    "light": LIGHT_THEME,
    "dark": DARK_THEME,
    "high_contrast": HIGH_CONTRAST_THEME,
}


# ---------------------------------------------------------------------------
# Theme Registry
# ---------------------------------------------------------------------------


class ThemeRegistry:
    """
    Registry containing all available GUI themes.

    The registry allows themes to be registered,
    removed, retrieved, and enumerated without
    coupling the rest of the application to a
    specific theme implementation.
    """

    def __init__(
        self,
        themes: Mapping[
            str,
            ThemeDefinition,
        ] | None = None,
    ) -> None:
        """Initialize the theme registry."""

        self._themes: dict[
            str,
            ThemeDefinition,
        ] = {}

        if themes is not None:
            for name, theme in themes.items():
                self.register(
                    name,
                    theme,
                )

    def register(
        self,
        name: str,
        theme: ThemeDefinition,
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Register a theme.

        Parameters
        ----------
        name:
            Name used to identify the theme.

        theme:
            ThemeDefinition instance.

        overwrite:
            Whether an existing theme may be replaced.
        """

        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "Theme name must be a string."
            )

        name = name.strip().lower()

        if not name:
            raise ValueError(
                "Theme name cannot be empty."
            )

        if not isinstance(
            theme,
            ThemeDefinition,
        ):
            raise TypeError(
                "theme must be a ThemeDefinition."
            )

        if (
            name in self._themes
            and not overwrite
        ):
            raise ThemeConfigurationError(
                f"Theme '{name}' already exists."
            )

        self._themes[name] = theme

    def unregister(
        self,
        name: str,
    ) -> ThemeDefinition:
        """
        Remove and return a registered theme.
        """

        name = name.strip().lower()

        if name not in self._themes:
            raise ThemeNotFoundError(
                f"Theme '{name}' does not exist."
            )

        return self._themes.pop(
            name
        )

    def get(
        self,
        name: str,
    ) -> ThemeDefinition:
        """
        Retrieve a theme by name.
        """

        name = name.strip().lower()

        try:
            return self._themes[name]
        except KeyError as error:
            raise ThemeNotFoundError(
                f"Theme '{name}' does not exist."
            ) from error

    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether a theme exists."""

        return (
            name.strip().lower()
            in self._themes
        )

    def names(self) -> tuple[str, ...]:
        """Return all registered theme names."""

        return tuple(
            self._themes.keys()
        )

    def themes(
        self,
    ) -> dict[
        str,
        ThemeDefinition,
    ]:
        """Return a copy of the registered themes."""

        return dict(
            self._themes
        )

    def clear(self) -> None:
        """Remove all registered themes."""

        self._themes.clear()


# ---------------------------------------------------------------------------
# Default Registry
# ---------------------------------------------------------------------------


theme_registry = ThemeRegistry(
    DEFAULT_THEMES
)


# ---------------------------------------------------------------------------
# Theme Manager
# ---------------------------------------------------------------------------


class ThemeManager:
    """
    Manages the currently active GUI theme.

    Responsible for:

    - Theme selection
    - Theme registration
    - Tkinter style configuration
    - Widget style application
    """

    def __init__(
        self,
        root: Any = None,
        registry: ThemeRegistry | None = None,
        default_theme: str = "dark",
    ) -> None:
        """Initialize the theme manager."""

        self.root = root

        self.registry = (
            registry
            if registry is not None
            else theme_registry
        )

        if not self.registry.exists(
            default_theme
        ):
            raise ThemeNotFoundError(
                f"Theme '{default_theme}' does not exist."
            )

        self._current_theme = (
            default_theme
        )

        self._style: Any = None

        if ttk is not None:
            self._style = ttk.Style(
                self.root
            )

    @property
    def current_theme(self) -> str:
        """Return the current theme name."""

        return self._current_theme

    @property
    def theme(self) -> ThemeDefinition:
        """Return the active theme definition."""

        return self.registry.get(
            self._current_theme
        )

    @property
    def palette(self) -> ColorPalette:
        """Return the active color palette."""

        return self.theme.palette

    @property
    def fonts(self) -> FontSet:
        """Return the active font set."""

        return self.theme.fonts

    def set_theme(
        self,
        name: str,
    ) -> ThemeDefinition:
        """
        Set and apply a theme.
        """

        if not self.registry.exists(
            name
        ):
            raise ThemeNotFoundError(
                f"Theme '{name}' does not exist."
            )

        self._current_theme = (
            name.strip().lower()
        )

        self.apply()

        return self.theme

    def register_theme(
        self,
        name: str,
        theme: ThemeDefinition,
        *,
        overwrite: bool = False,
    ) -> None:
        """Register a new theme."""

        self.registry.register(
            name,
            theme,
            overwrite=overwrite,
        )

    def get_theme(
        self,
        name: str,
    ) -> ThemeDefinition:
        """Retrieve a theme."""

        return self.registry.get(
            name
        )

    def available_themes(
        self,
    ) -> tuple[str, ...]:
        """Return all available themes."""

        return self.registry.names()

    def apply(self) -> None:
        """
        Apply the current theme to the GUI.
        """

        if tk is None or ttk is None:
            raise ThemeConfigurationError(
                "Tkinter is unavailable."
            )

        if self.root is None:
            raise ThemeConfigurationError(
                "A root window is required."
            )

        palette = self.palette
        fonts = self.fonts

        self._configure_ttk(
            palette,
            fonts,
        )

        self._configure_root(
            palette,
            fonts,
        )

    def _configure_root(
        self,
        palette: ColorPalette,
        fonts: FontSet,
    ) -> None:
        """Configure the root window."""

        self.root.configure(
            background=palette.background
        )

        try:
            self.root.option_add(
                "*Font",
                fonts.normal(),
            )
        except tk.TclError:
            pass

    def _configure_ttk(
        self,
        palette: ColorPalette,
        fonts: FontSet,
    ) -> None:
        """Configure ttk widget styles."""

        if self._style is None:
            return

        try:
            self._style.theme_use(
                self.theme.ttk_theme
            )
        except tk.TclError:
            pass

        self._style.configure(
            ".",
            background=palette.background,
            foreground=palette.foreground,
            font=fonts.normal(),
        )

        self._style.configure(
            "TFrame",
            background=palette.background,
        )

        self._style.configure(
            "TLabel",
            background=palette.background,
            foreground=palette.foreground,
        )

        self._style.configure(
            "TButton",
            background=palette.button_background,
            foreground=palette.button_foreground,
            padding=palette.padding
            if hasattr(
                palette,
                "padding",
            )
            else 8,
        )

        self._style.configure(
            "TEntry",
            fieldbackground=(
                palette.input_background
            ),
            foreground=(
                palette.input_foreground
            ),
        )

        self._style.configure(
            "TCombobox",
            fieldbackground=(
                palette.input_background
            ),
            foreground=(
                palette.input_foreground
            ),
        )

        self._style.configure(
            "Horizontal.TProgressbar",
            background=palette.primary,
            troughcolor=palette.surface_alt,
        )

    def palette_dict(self) -> dict[str, str]:
        """Return the current palette as a dictionary."""

        return self.palette.as_dict()

    def font_dict(
        self,
    ) -> dict[str, tuple[str, int, str]]:
        """Return all standard font definitions."""

        return {
            "normal": self.fonts.normal(),
            "small": self.fonts.small(),
            "large": self.fonts.large(),
            "title": self.fonts.title(),
            "heading": self.fonts.heading(),
            "monospace": self.fonts.monospace(),
        }

    # ---------------------------------------------------------------------------
# Theme Utility Functions
# ---------------------------------------------------------------------------


def get_theme(
    name: str,
) -> ThemeDefinition:
    """
    Retrieve a theme from the default registry.
    """

    return theme_registry.get(
        name
    )


def register_theme(
    name: str,
    theme: ThemeDefinition,
    *,
    overwrite: bool = False,
) -> None:
    """
    Register a theme in the default registry.
    """

    theme_registry.register(
        name,
        theme,
        overwrite=overwrite,
    )


def remove_theme(
    name: str,
) -> ThemeDefinition:
    """
    Remove a theme from the default registry.
    """

    return theme_registry.unregister(
        name
    )


def theme_exists(
    name: str,
) -> bool:
    """
    Return whether a theme exists.
    """

    return theme_registry.exists(
        name
    )


def available_themes() -> tuple[str, ...]:
    """
    Return all available theme names.
    """

    return theme_registry.names()


def create_theme(
    name: str,
    palette: ColorPalette,
    *,
    fonts: FontSet | None = None,
    description: str = "",
    ttk_theme: str = "clam",
    border_width: int = 1,
    relief: str = "flat",
    padding: int = 8,
    register: bool = True,
    overwrite: bool = False,
) -> ThemeDefinition:
    """
    Create a new theme definition.

    Parameters
    ----------
    name:
        Name of the new theme.

    palette:
        Color palette used by the theme.

    fonts:
        Font configuration. Uses FontSet defaults
        when omitted.

    description:
        Human-readable theme description.

    ttk_theme:
        Base ttk theme.

    border_width:
        Default border width.

    relief:
        Default widget relief style.

    padding:
        Default widget padding.

    register:
        Whether the theme should be added to the
        global theme registry.

    overwrite:
        Whether an existing theme with the same
        name may be replaced.
    """

    if fonts is None:
        fonts = FontSet()

    theme = ThemeDefinition(
        name=name,
        palette=palette,
        fonts=fonts,
        description=description,
        ttk_theme=ttk_theme,
        border_width=border_width,
        relief=relief,
        padding=padding,
    )

    if register:
        register_theme(
            name,
            theme,
            overwrite=overwrite,
        )

    return theme


# ---------------------------------------------------------------------------
# Theme Inspection
# ---------------------------------------------------------------------------


def describe_theme(
    name: str,
) -> str:
    """
    Return a human-readable description of a theme.
    """

    theme = get_theme(
        name
    )

    description = (
        theme.description
        if theme.description
        else "No description available."
    )

    return (
        f"Theme: {theme.name}\n"
        f"Description: {description}\n"
        f"TTK Theme: {theme.ttk_theme}\n"
        f"Border Width: {theme.border_width}\n"
        f"Padding: {theme.padding}"
    )


def compare_themes(
    first: str,
    second: str,
) -> dict[str, Any]:
    """
    Compare two registered themes.

    Returns a dictionary containing the properties
    that differ between the two themes.
    """

    first_theme = get_theme(
        first
    )

    second_theme = get_theme(
        second
    )

    differences: dict[str, Any] = {}

    if first_theme.palette != second_theme.palette:
        differences["palette"] = {
            first_theme.name: (
                first_theme.palette.as_dict()
            ),
            second_theme.name: (
                second_theme.palette.as_dict()
            ),
        }

    if first_theme.fonts != second_theme.fonts:
        differences["fonts"] = {
            first_theme.name: first_theme.fonts,
            second_theme.name: second_theme.fonts,
        }

    if (
        first_theme.ttk_theme
        != second_theme.ttk_theme
    ):
        differences["ttk_theme"] = {
            first_theme.name: (
                first_theme.ttk_theme
            ),
            second_theme.name: (
                second_theme.ttk_theme
            ),
        }

    if (
        first_theme.border_width
        != second_theme.border_width
    ):
        differences["border_width"] = {
            first_theme.name: (
                first_theme.border_width
            ),
            second_theme.name: (
                second_theme.border_width
            ),
        }

    if (
        first_theme.relief
        != second_theme.relief
    ):
        differences["relief"] = {
            first_theme.name: (
                first_theme.relief
            ),
            second_theme.name: (
                second_theme.relief
            ),
        }

    if (
        first_theme.padding
        != second_theme.padding
    ):
        differences["padding"] = {
            first_theme.name: (
                first_theme.padding
            ),
            second_theme.name: (
                second_theme.padding
            ),
        }

    return differences


# ---------------------------------------------------------------------------
# Theme Selection Helpers
# ---------------------------------------------------------------------------


def get_default_theme() -> ThemeDefinition:
    """
    Return the default application theme.
    """

    return DARK_THEME


def get_light_theme() -> ThemeDefinition:
    """
    Return the standard light theme.
    """

    return LIGHT_THEME


def get_dark_theme() -> ThemeDefinition:
    """
    Return the standard dark theme.
    """

    return DARK_THEME


def get_high_contrast_theme() -> ThemeDefinition:
    """
    Return the high-contrast theme.
    """

    return HIGH_CONTRAST_THEME


# ---------------------------------------------------------------------------
# Color Helpers
# ---------------------------------------------------------------------------


def get_color(
    theme: str,
    color_name: str,
    default: str | None = None,
) -> str | None:
    """
    Retrieve a specific color from a theme.

    Parameters
    ----------
    theme:
        Registered theme name.

    color_name:
        Palette attribute name.

    default:
        Value returned when the color does not exist.
    """

    theme_definition = get_theme(
        theme
    )

    palette = theme_definition.palette

    if not hasattr(
        palette,
        color_name,
    ):
        return default

    return getattr(
        palette,
        color_name,
    )


def get_font(
    theme: str,
    font_name: str,
) -> tuple[str, int, str]:
    """
    Retrieve a standard font definition.
    """

    theme_definition = get_theme(
        theme
    )

    fonts = theme_definition.fonts

    font_methods = {
        "normal": fonts.normal,
        "small": fonts.small,
        "large": fonts.large,
        "title": fonts.title,
        "heading": fonts.heading,
        "monospace": fonts.monospace,
    }

    if font_name not in font_methods:
        raise ThemeConfigurationError(
            f"Unknown font: {font_name}"
        )

    return font_methods[
        font_name
    ]()


# ---------------------------------------------------------------------------
# Theme Manager Factory
# ---------------------------------------------------------------------------


def create_theme_manager(
    root: Any = None,
    *,
    default_theme: str = "dark",
    registry: ThemeRegistry | None = None,
) -> ThemeManager:
    """
    Create a configured ThemeManager.
    """

    return ThemeManager(
        root=root,
        registry=registry,
        default_theme=default_theme,
    )


# ---------------------------------------------------------------------------
# Theme Validation
# ---------------------------------------------------------------------------


def validate_theme(
    theme: ThemeDefinition,
) -> bool:
    """
    Validate a theme definition.

    Returns True when the theme is valid.
    """

    if not isinstance(
        theme,
        ThemeDefinition,
    ):
        return False

    try:
        if not theme.name.strip():
            return False

        if not isinstance(
            theme.palette,
            ColorPalette,
        ):
            return False

        if not isinstance(
            theme.fonts,
            FontSet,
        ):
            return False

        if theme.border_width < 0:
            return False

        if theme.padding < 0:
            return False

    except (
        AttributeError,
        TypeError,
        ValueError,
    ):
        return False

    return True


def validate_palette(
    palette: ColorPalette,
) -> bool:
    """
    Validate a color palette.
    """

    if not isinstance(
        palette,
        ColorPalette,
    ):
        return False

    values = palette.as_dict()

    return all(
        isinstance(
            value,
            str,
        )
        and bool(
            value.strip()
        )
        for value in values.values()
    )


# ---------------------------------------------------------------------------
# Theme Reset
# ---------------------------------------------------------------------------


def reset_default_themes() -> None:
    """
    Reset the global registry to the built-in themes.

    This removes custom themes and restores the
    standard light, dark, and high-contrast themes.
    """

    theme_registry.clear()

    for name, theme in DEFAULT_THEMES.items():
        theme_registry.register(
            name,
            theme,
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    # Exceptions
    "ThemeError",
    "ThemeNotFoundError",
    "ThemeConfigurationError",

    # Data Classes
    "ColorPalette",
    "FontSet",
    "ThemeDefinition",

    # Palettes
    "LIGHT_PALETTE",
    "DARK_PALETTE",
    "HIGH_CONTRAST_PALETTE",

    # Themes
    "LIGHT_THEME",
    "DARK_THEME",
    "HIGH_CONTRAST_THEME",
    "DEFAULT_THEMES",

    # Registry
    "ThemeRegistry",
    "theme_registry",

    # Manager
    "ThemeManager",

    # Theme Functions
    "get_theme",
    "register_theme",
    "remove_theme",
    "theme_exists",
    "available_themes",
    "create_theme",

    # Inspection
    "describe_theme",
    "compare_themes",

    # Default Theme Helpers
    "get_default_theme",
    "get_light_theme",
    "get_dark_theme",
    "get_high_contrast_theme",

    # Color / Font Helpers
    "get_color",
    "get_font",

    # Manager Factory
    "create_theme_manager",

    # Validation
    "validate_theme",
    "validate_palette",

    # Reset
    "reset_default_themes",
]

