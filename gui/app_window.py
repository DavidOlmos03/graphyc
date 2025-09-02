"""Main application window (Tkinter) for MetodoGraficoApp.

This module builds the GUI, connects user actions to the business logic and
keeps the interface responsive.
"""

from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Optional

from core.restrictions import RestrictionManager, Restriction
from core.solver import Solver, ObjectiveFunction
from .styles import configure_styles
from .particle_canvas import ParticleCanvas


@dataclass
class EntryRow:
    """Container to store widget references for a restriction row."""
    entry_a: tk.Entry
    sign_a_var: tk.StringVar
    entry_b: tk.Entry
    op_var: tk.StringVar
    entry_c: tk.Entry

@dataclass
class ObjetiveFunction:
    """Data class to store objetive function parameters"""
    coeff_x1: float
    coeff_x2: float
    optimization_type: str #max or min

class AppWindow:
    """Encapsulates the Tk application window and interactions."""

    def __init__(self) -> None:
        """Initialize the window, styles and core managers."""
        self.root = tk.Tk()
        self.root.title("Solver Gráfico de Programación Lineal")
        self.root.geometry("740x420")
        self.root.resizable(False, False)

        configure_styles(self.root)

        # Core components
        self.restriction_manager = RestrictionManager()
        self.solver = Solver()
        self.objetive_function: Optional[ObjetiveFunction] = None

        # UI containers
        # Background particle canvas
        self.particle_bg = ParticleCanvas(self.root, num_particles=30, width=640, height=420)
        self.particle_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Foreground frame (content above particles)
        self.main_frame = ttk.Frame(self.root, padding=12, style="Card.TFrame")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Objetive Function Frame
        self.obj_frame = ttk.Frame(self.main_frame)
        self.obj_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.obj_frame, text="Objective Function:", style="Header.TLabel").grid(
            row=0, column=0, sticky="w", columnspan=5
        )

        ttk.Label(self.obj_frame, text="Z =").grid(row=1, column=0, padx=(0, 5))
        
        self.obj_x1_entry = ttk.Entry(self.obj_frame, width=6)
        self.obj_x1_entry.insert(0, "1")
        self.obj_x1_entry.grid(row=1, column=1, padx=2)
        
        ttk.Label(self.obj_frame, text="x1 +").grid(row=1, column=2, padx=2)
        
        self.obj_x2_entry = ttk.Entry(self.obj_frame, width=6)
        self.obj_x2_entry.insert(0, "1")
        self.obj_x2_entry.grid(row=1, column=3, padx=2)
        
        ttk.Label(self.obj_frame, text="x2").grid(row=1, column=4, padx=2)
        
        self.obj_type_var = tk.StringVar(value="max")
        obj_type_menu = ttk.OptionMenu(self.obj_frame, self.obj_type_var, "max", "max", "min")
        obj_type_menu.grid(row=1, column=5, padx=5)

        # Restrictions frame
        self.rows_frame = ttk.Frame(self.main_frame)
        self.rows_frame.pack(fill=tk.X, pady=(4, 8))

        header = ttk.Label(self.rows_frame, text="X1  (+/-)  X2   (≤/≥)   Rs", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=5, sticky="w", padx=(2, 2), pady=(0, 8))

        self.entry_rows: List[EntryRow] = []

        # Add two default restrictions
        self.add_restriction_row()
        self.add_restriction_row()

        # Buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=(6, 0))

        add_btn = ttk.Button(buttons_frame, text="+ Add constraint", command=self.add_restriction_row)
        add_btn.pack(side=tk.LEFT, padx=(0, 6))

        plot_btn = ttk.Button(buttons_frame, text="Plot Feasible Region", command=self.on_plot)
        plot_btn.pack(side=tk.LEFT)

        # Informational label
        note_label = ttk.Label(
            self.main_frame,
            text="Use numbers for coefficients. Use +/- to apply sign to second coefficient.",
            style="TLabel",
        )
        note_label.pack(fill=tk.X, pady=(10, 0))

    def add_restriction_row(self, a: str = "", sign1: str = "+", b: str = "", op: str = "≤", c: str = "") -> None:
        """
        Add a UI row with entries to define a linear restriction.

        Parameters
        ----------
        a : str
            Value for coefficient a (x1).
        sign1 : str
            Sign for second term; stored as menu selection.
        b : str
            Value for coefficient b (x2).
        op : str
            Inequality operator symbol - '≤' or '≥'.
        c : str
            Right-hand side constant.
        """
        row_index = len(self.entry_rows) + 1

        entry_a = tk.Entry(self.rows_frame, width=6)
        entry_a.insert(0, str(a))
        entry_a.grid(row=row_index, column=0, padx=2, pady=2)

        sign_a_var = tk.StringVar(self.rows_frame)
        sign_a_var.set(sign1)
        sign_menu = ttk.OptionMenu(self.rows_frame, sign_a_var, sign1, "+", "-")
        sign_menu.grid(row=row_index, column=1, padx=2)

        entry_b = tk.Entry(self.rows_frame, width=6)
        entry_b.insert(0, str(b))
        entry_b.grid(row=row_index, column=2, padx=2)

        op_var = tk.StringVar(self.rows_frame)
        op_var.set(op)
        op_menu = ttk.OptionMenu(self.rows_frame, op_var, op, "≤", "≥")
        op_menu.grid(row=row_index, column=3, padx=2)

        entry_c = tk.Entry(self.rows_frame, width=6)
        entry_c.insert(0, str(c))
        entry_c.grid(row=row_index, column=4, padx=2)

        self.entry_rows.append(EntryRow(entry_a, sign_a_var, entry_b, op_var, entry_c))
    def collect_objective_function(self) -> None:
        """Read objective function values from UI."""
        try:
            coeff_x1 = float(self.obj_x1_entry.get().strip())
            coeff_x2 = float(self.obj_x2_entry.get().strip())
            opt_type = self.obj_type_var.get().strip()
            
            self.objective_function = ObjectiveFunction(
                coeff_x1=coeff_x1,
                coeff_x2=coeff_x2,
                optimization_type=opt_type
            )
        except ValueError:
            raise ValueError("Objective function coefficients must be numeric.")


    def collect_restrictions(self) -> None:
        """Read UI rows and update the restriction manager with current values."""
        self.restriction_manager.clear()
        for row in self.entry_rows:
            a_text = row.entry_a.get().strip()
            b_text = row.entry_b.get().strip()
            c_text = row.entry_c.get().strip()
            sign = row.sign_a_var.get().strip()
            op = row.op_var.get().strip()

            # Skip blank rows
            if not (a_text or b_text or c_text):
                continue

            try:
                a_val = float(a_text) if a_text != "" else 0.0
                b_val = float(b_text) if b_text != "" else 0.0
                c_val = float(c_text) if c_text != "" else 0.0
            except ValueError:
                raise ValueError("All coefficients must be numeric or empty.")

            # Apply sign to the second coefficient when sign is '-'
            if sign == "-":
                b_val = -abs(b_val)
            else:
                b_val = abs(b_val)

            restriction = Restriction(a=a_val, b=b_val, op=op, c=c_val)
            self.restriction_manager.add(restriction)
    
    def on_plot(self) -> None:
        """Handle the plot action: collect restrictions and ask solver to draw."""
        try:
            # Collect objective function
            self.collect_objective_function()
            
            # Collect restrictions
            self.collect_restrictions()
            restrictions = self.restriction_manager.get_all()
            
            if not restrictions:
                messagebox.showinfo("No constraints", "Please add at least one constraint before plotting.")
                return

            # Plot with objective function
            self.solver.plot_feasible_region(
                restrictions, 
                self.objective_function
            )
            
        except Exception as exc:  # pylint: disable=broad-except
            messagebox.showerror("Error", f"An error occurred: {exc}")
    def run(self) -> None:
        """Start the Tk main loop."""
        self.root.mainloop()
