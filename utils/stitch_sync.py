"""Sync design tokens from Stitch (config/stitch_design.py) to CSS variables."""

from pathlib import Path

from config.stitch_design import get_css_variables


def sync_tokens() -> None:
    """Generate CSS variables file from Stitch design tokens."""
    project_root = Path(__file__).parent.parent
    css_dir = project_root / "public" / "css"
    css_dir.mkdir(parents=True, exist_ok=True)

    output_file = css_dir / "design-tokens.css"

    css_content = f"""/*
 * Design Tokens - Auto-generated from config/stitch_design.py
 * Source: Google Stitch project "Minimalist Business Showcase" (Green Tech)
 * DO NOT EDIT MANUALLY - Run `python -m utils.stitch_sync` to regenerate
 */

{get_css_variables()}

/* Additional utility classes for common patterns */
:root {{
  /* Focus styles */
  --focus-ring: 0 0 0 3px rgba(45, 106, 79, 0.3);
  --focus-ring-error: 0 0 0 3px rgba(186, 26, 26, 0.3);

  /* Transitions */
  --transition-fast: 150ms ease-out;
  --transition-base: 200ms ease-out;
  --transition-slow: 300ms ease-out;

  /* Z-index scale */
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-modal-backdrop: 300;
  --z-modal: 400;
  --z-tooltip: 500;
  --z-toast: 600;
}}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {{
  *,
  *::before,
  *::after {{
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }}
}}

/* High contrast mode */
@media (prefers-contrast: high) {{
  :root {{
    --color-outline-variant: var(--color-outline);
    --shadow-base: 0 0 0 1px var(--color-outline);
    --shadow-hover: 0 0 0 2px var(--color-primary);
  }}
}}

/* Print styles */
@media print {{
  .no-print {{
    display: none !important;
  }}
  .print-only {{
    display: block !important;
  }}
  a {{
    text-decoration: none;
    color: var(--color-primary) !important;
  }}
}}
"""

    output_file.write_text(css_content, encoding="utf-8")
    print(f"✅ Design tokens synced to {output_file.relative_to(project_root)}")


if __name__ == "__main__":
    sync_tokens()
