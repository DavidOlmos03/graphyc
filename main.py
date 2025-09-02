"""Entry point for MetodoGraficoApp.

This module creates the main Tkinter application window and starts the main loop.
"""

from gui.app_window import AppWindow


def main() -> None:
    """Create and run the application window."""
    app = AppWindow()
    app.run()


if __name__ == "__main__":
    main()

