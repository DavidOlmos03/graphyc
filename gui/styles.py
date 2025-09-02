"""UI styles for the application using tkinter.ttk.

Defines modern colors, hover effects and fonts.
"""

from tkinter import font
from tkinter import ttk
from typing import Any


def configure_styles(root: Any) -> None:
    """
    Configure ttk styles and custom fonts for a modern look.

    Parameters
    ----------
    root : Any
        The root Tk instance.
    """
    style = ttk.Style(root)

    # Use a clean theme
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Define fonts
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=11, family="Segoe UI")

    heading_font = font.Font(root=root, family="Segoe UI", size=14, weight="bold")

    # General frame
    style.configure(
        "TFrame",
        background="#1e293b",  # dark slate
    )

    # Card style (white panel)
    style.configure(
        "Card.TFrame",
        background="#f8fafc",
        relief="flat",
        borderwidth=1,
    )

    # Labels
    style.configure(
        "TLabel",
        background="#1e293b",
        foreground="#f8fafc",
        font=default_font,
    )

    style.configure(
        "Header.TLabel",
        font=heading_font,
        background="#1e293b",
        foreground="#38bdf8",  # cyan accent
    )

    # Buttons
    style.configure(
        "TButton",
        padding=(10, 6),
        relief="flat",
        background="#38bdf8",
        foreground="#1e293b",
        font=default_font,
    )

    style.map(
        "TButton",
        background=[
            ("active", "#0ea5e9"),  # darker cyan
            ("pressed", "#0369a1"),
        ],
        foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
    )

    # Dropdown (OptionMenu)
    style.configure(
        "TMenubutton",
        padding=(8, 4),
        background="#334155",
        foreground="#f8fafc",
        relief="flat",
    )

