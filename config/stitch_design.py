"""Design System tokens from Google Stitch project 'Minimalist Business Showcase'.

This module centralizes all design tokens (colors, typography, spacing, shapes, shadows)
extracted from the Stitch project. These tokens are used to generate CSS variables
via utils/stitch_sync.py and can be imported directly in Python for server-side rendering.
"""

from dataclasses import dataclass





@dataclass(frozen=True)
class ColorPalette:
    """Complete color palette from Stitch design system."""


    primary: str = "#1B4332"
    primary_container: str = "#1B4332"
    on_primary: str = "#FFFFFF"
    on_primary_container: str = "#86AF99"
    primary_fixed: str = "#C1ECD4"
    primary_fixed_dim: str = "#A5D0B9"
    on_primary_fixed: str = "#002114"
    on_primary_fixed_variant: str = "#274E3D"


    secondary: str = "#2D6A4F"
    secondary_container: str = "#AEEECB"
    on_secondary: str = "#FFFFFF"
    on_secondary_container: str = "#316E52"
    secondary_fixed: str = "#B1F0CE"
    secondary_fixed_dim: str = "#95D4B3"
    on_secondary_fixed: str = "#002114"
    on_secondary_fixed_variant: str = "#0E5138"


    tertiary: str = "#E07A5F"
    tertiary_container: str = "#6D230F"
    on_tertiary: str = "#FFFFFF"
    on_tertiary_container: str = "#F3896D"
    tertiary_fixed: str = "#FFDBD2"
    tertiary_fixed_dim: str = "#FFB4A1"
    on_tertiary_fixed: str = "#3C0800"
    on_tertiary_fixed_variant: str = "#7C2E19"


    surface: str = "#F9FAF7"
    surface_bright: str = "#F9FAF7"
    surface_dim: str = "#D9DAD7"
    surface_container_lowest: str = "#FFFFFF"
    surface_container_low: str = "#F3F4F1"
    surface_container: str = "#EDEEEB"
    surface_container_high: str = "#E7E8E6"
    surface_container_highest: str = "#E2E3E0"
    on_surface: str = "#191C1B"
    on_surface_variant: str = "#414844"


    background: str = "#F9FAF7"
    on_background: str = "#191C1B"


    outline: str = "#717973"
    outline_variant: str = "#C1C8C2"


    error: str = "#BA1A1A"
    on_error: str = "#FFFFFF"
    error_container: str = "#FFDAD6"
    on_error_container: str = "#93000A"


    inverse_surface: str = "#2E312F"
    inverse_on_surface: str = "#F0F1EE"
    inverse_primary: str = "#A5D0B9"


    surface_tint: str = "#3F6653"


    surface_variant: str = "#E2E3E0"


    neutral_base: str = "#F3F4F1"
    neutral_border: str = "#E5E7EB"
    neutral_card: str = "#FFFFFF"
    neutral_secondary_bg: str = "#F8F9FA"






@dataclass(frozen=True)
class TypographyScale:
    """Typography scale from Stitch - Plus Jakarta Sans."""

    font_family: str = "Plus Jakarta Sans"
    font_family_fallback: str = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"


    display_lg: dict[str, str] | None = None
    display_lg_mobile: dict[str, str] | None = None


    headline_xl: dict[str, str] | None = None
    headline_xl_mobile: dict[str, str] | None = None
    headline_lg: dict[str, str] | None = None
    headline_lg_mobile: dict[str, str] | None = None
    headline_md: dict[str, str] | None = None
    headline_sm: dict[str, str] | None = None


    body_lg: dict[str, str] | None = None
    body_md: dict[str, str] | None = None
    body_sm: dict[str, str] | None = None


    label_lg: dict[str, str] | None = None
    label_md: dict[str, str] | None = None
    label_sm: dict[str, str] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "display_lg", {
            "font_size": "52px", "line_height": "60px",
            "letter_spacing": "-0.03em", "font_weight": "800"
        })
        object.__setattr__(self, "display_lg_mobile", {
            "font_size": "36px", "line_height": "44px",
            "letter_spacing": "-0.02em", "font_weight": "800"
        })
        object.__setattr__(self, "headline_xl", {
            "font_size": "40px", "line_height": "48px",
            "letter_spacing": "-0.02em", "font_weight": "700"
        })
        object.__setattr__(self, "headline_xl_mobile", {
            "font_size": "30px", "line_height": "38px",
            "letter_spacing": "-0.015em", "font_weight": "700"
        })
        object.__setattr__(self, "headline_lg", {
            "font_size": "32px", "line_height": "40px",
            "letter_spacing": "-0.015em", "font_weight": "700"
        })
        object.__setattr__(self, "headline_lg_mobile", {
            "font_size": "24px", "line_height": "32px",
            "letter_spacing": "-0.01em", "font_weight": "600"
        })
        object.__setattr__(self, "headline_md", {
            "font_size": "22px", "line_height": "30px",
            "letter_spacing": "-0.01em", "font_weight": "600"
        })
        object.__setattr__(self, "headline_sm", {
            "font_size": "18px", "line_height": "26px",
            "letter_spacing": "-0.005em", "font_weight": "600"
        })
        object.__setattr__(self, "body_lg", {
            "font_size": "17px", "line_height": "28px",
            "letter_spacing": "0em", "font_weight": "400"
        })
        object.__setattr__(self, "body_md", {
            "font_size": "15px", "line_height": "24px",
            "letter_spacing": "0em", "font_weight": "400"
        })
        object.__setattr__(self, "body_sm", {
            "font_size": "13px", "line_height": "20px",
            "letter_spacing": "0.005em", "font_weight": "400"
        })
        object.__setattr__(self, "label_lg", {
            "font_size": "14px", "line_height": "20px",
            "letter_spacing": "0.01em", "font_weight": "600"
        })
        object.__setattr__(self, "label_md", {
            "font_size": "12px", "line_height": "16px",
            "letter_spacing": "0.03em", "font_weight": "600"
        })
        object.__setattr__(self, "label_sm", {
            "font_size": "10px", "line_height": "14px",
            "letter_spacing": "0.06em", "font_weight": "700"
        })






@dataclass(frozen=True)
class SpacingScale:
    """Spacing scale from Stitch."""


    space_xs: str = "0.25rem"
    space_sm: str = "0.5rem"
    space_md: str = "1rem"
    space_lg: str = "1.5rem"
    space_xl: str = "2.5rem"


    gutter: str = "1.5rem"
    gutter_mobile: str = "1rem"
    margin: str = "3rem"
    margin_mobile: str = "1.25rem"


    container_max: str = "1280px"

    @property
    def scale(self) -> dict[str, str]:
        """Return all spacing as a dictionary."""
        return {
            "xs": self.space_xs,
            "sm": self.space_sm,
            "md": self.space_md,
            "lg": self.space_lg,
            "xl": self.space_xl,
        }






@dataclass(frozen=True)
class BorderRadius:
    """Border radius scale from Stitch (Roundness level 2)."""

    none: str = "0"
    sm: str = "0.25rem"
    base: str = "0.5rem"
    md: str = "0.75rem"
    lg: str = "1rem"
    xl: str = "1.5rem"
    full: str = "9999px"






@dataclass(frozen=True)
class Shadows:
    """Shadow system from Stitch (tinted with primary color)."""


    base: str = "0 1px 3px rgba(27, 67, 50, 0.04), 0 1px 2px rgba(27, 67, 50, 0.02)"


    hover: str = "0 12px 28px -4px rgba(27, 67, 50, 0.08), 0 4px 10px -2px rgba(27, 67, 50, 0.03)"


    focus_ring: str = "0 0 0 3px rgba(45, 106, 79, 0.2)"






@dataclass(frozen=True)
class Breakpoints:
    """Responsive breakpoints from Stitch layout system."""

    mobile: str = "768px"
    tablet: str = "1199px"
    desktop: str = "1200px"

    @property
    def media_queries(self) -> dict[str, str]:
        return {
            "mobile": f"(max-width: {self.mobile})",
            "tablet": f"(min-width: {self.mobile}) and (max-width: {self.tablet})",
            "desktop": f"(min-width: {self.desktop})",
        }






@dataclass(frozen=True)
class ButtonVariants:
    """Button style variants."""

    primary: dict[str, str] | None = None
    cta: dict[str, str] | None = None
    secondary: dict[str, str] | None = None
    tertiary: dict[str, str] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "primary", {
            "bg": "var(--color-primary)",
            "color": "var(--color-on-primary)",
            "border": "none",
            "hover_bg": "var(--color-secondary)",
            "transition": "all 200ms ease-out",
        })
        object.__setattr__(self, "cta", {
            "bg": "var(--color-tertiary)",
            "color": "var(--color-on-tertiary)",
            "border": "none",
            "hover_bg": "#D46A4F",
            "transition": "all 200ms ease-out",
        })
        object.__setattr__(self, "secondary", {
            "bg": "transparent",
            "color": "var(--color-primary)",
            "border": "1.5px solid var(--color-secondary)",
            "hover_bg": "rgba(45, 106, 79, 0.08)",
            "transition": "all 200ms ease-out",
        })
        object.__setattr__(self, "tertiary", {
            "bg": "transparent",
            "color": "var(--color-primary)",
            "border": "none",
            "hover_bg": "var(--color-surface-container)",
            "transition": "all 200ms ease-out",
        })


@dataclass(frozen=True)
class CardVariants:
    """Card style variants."""

    default: dict[str, str] | None = None
    elevated: dict[str, str] | None = None
    interactive: dict[str, str] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "default", {
            "bg": "var(--color-surface-container-lowest)",
            "border": "1px solid var(--color-outline-variant)",
            "radius": "var(--radius-lg)",
            "padding": "var(--space-lg)",
        })
        object.__setattr__(self, "elevated", {
            "bg": "var(--color-surface-container-lowest)",
            "border": "1px solid var(--color-outline-variant)",
            "radius": "var(--radius-lg)",
            "padding": "var(--space-lg)",
            "shadow": "var(--shadow-base)",
        })
        object.__setattr__(self, "interactive", {
            "bg": "var(--color-surface-container-lowest)",
            "border": "1px solid var(--color-outline-variant)",
            "radius": "var(--radius-lg)",
            "padding": "var(--space-lg)",
            "shadow": "var(--shadow-base)",
            "transition": "transform 200ms ease-out, box-shadow 200ms ease-out",
            "hover_transform": "translateY(-3px)",
            "hover_shadow": "var(--shadow-hover)",
        })







colors = ColorPalette()
typography = TypographyScale()
spacing = SpacingScale()
radius = BorderRadius()
shadows = Shadows()
breakpoints = Breakpoints()
buttons = ButtonVariants()
cards = CardVariants()


ALL_TOKENS = {
    "colors": colors.__dict__,
    "typography": {k: v for k, v in typography.__dict__.items() if not k.startswith("_")},
    "spacing": spacing.__dict__,
    "radius": radius.__dict__,
    "shadows": shadows.__dict__,
    "breakpoints": breakpoints.__dict__,
    "buttons": buttons.__dict__,
    "cards": cards.__dict__,
}


def get_css_variables() -> str:
    """Generate CSS custom properties (variables) from all tokens.

    Returns a string of CSS variable declarations ready to be placed in :root.
    """
    lines = [":root {"]


    for key, value in colors.__dict__.items():
        if not key.startswith("_"):
            css_key = key.replace("_", "-")
            lines.append(f"  --color-{css_key}: {value};")


    for key, value in spacing.__dict__.items():
        if not key.startswith("_"):
            css_key = key.replace("_", "-")
            lines.append(f"  --space-{css_key}: {value};")


    for key, value in radius.__dict__.items():
        if not key.startswith("_"):
            lines.append(f"  --radius-{key}: {value};")


    for key, value in shadows.__dict__.items():
        if not key.startswith("_"):
            css_key = key.replace("_", "-")
            lines.append(f"  --shadow-{css_key}: {value};")


    for key, value in breakpoints.__dict__.items():
        if not key.startswith("_") and key != "media_queries":
            lines.append(f"  --bp-{key}: {value};")


    lines.append(f"  --font-family: '{typography.font_family}', {typography.font_family_fallback};")
    lines.append("  --font-family-mono: 'Geist Mono', 'JetBrains Mono', monospace;")


    lines.append(f"  --container-max: {spacing.container_max};")

    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":

    print(get_css_variables())
