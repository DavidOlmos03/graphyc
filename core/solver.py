"""Solver and plotting utilities.

This module computes the feasible region on a grid and plots it using matplotlib.
It does not perform exact linear-programming vertex enumeration — it visualizes
the feasible set over a bounded grid for educational/visual purposes.
"""

from typing import Iterable, Tuple, List, Optional
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

from .restrictions import Restriction
from dataclasses import dataclass
from tkinter import messagebox


@dataclass
class ObjectiveFunction:
    """Data class to store objective function parameters."""
    coeff_x1: float
    coeff_x2: float
    optimization_type: str  # "max" or "min"

class Solver:
    """Solver for visualizing the feasible region of linear constraints."""

    def __init__(self, x_range: Tuple[float, float] = (0.0, 50.0), resolution: int = 500) -> None:
        """
        Initialize solver parameters.

        Parameters
        ----------
        x_range : Tuple[float, float]
            (min, max) for both x1 and x2 axes.
        resolution : int
            Number of points per axis used in the grid.
        """
        self.x_min, self.x_max = x_range
        self.resolution = int(resolution)


    def _grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """Create a mesh grid for the visualization."""
        x1 = np.linspace(self.x_min, self.x_max, self.resolution)
        x2 = np.linspace(self.x_min, self.x_max, self.resolution)
        return np.meshgrid(x1, x2)

    def plot_feasible_region(self, restrictions: Iterable[Restriction],
                             objective_function: Optional[ObjectiveFunction] = None) -> None:
        """
        Plot the feasible region defined by the restrictions and optionally find optimal solution.
        
        Parameters
        ----------
        restrictions : List[Restriction]
            List of linear restrictions.
        objective_function : Optional[ObjectiveFunction]
            Objective function to optimize.
        """
        # Create the plot
        plt.figure(figsize=(10, 8))
        x = np.linspace(0, 50, 500)
        y = np.linspace(0, 50, 500)
        X, Y = np.meshgrid(x, y)
        
        # Start with all points being feasible
        feasible = np.ones_like(X, dtype=bool)
        
        # Process each restriction
        for r in restrictions:
            # Plot the boundary line
            if r.b != 0:
                y_line = (r.c - r.a * x) / r.b
                plt.plot(x, y_line, label=f"{r.a}x1 + {r.b}x2 {r.op} {r.c}")
            
            # Update feasible region
            if r.op == "≤":
                feasible &= (r.a * X + r.b * Y <= r.c)
            else:  # "≥"
                feasible &= (r.a * X + r.b * Y >= r.c)
        
        # Plot feasible region
        plt.imshow(feasible, extent=(0, 50, 0, 50), origin='lower', 
                  alpha=0.3, cmap="Greens")
        
        # If objective function is provided, find and plot optimal solution
        if objective_function:
            self._find_and_plot_optimal(restrictions, objective_function, plt)
        
        plt.xlim(0, 50)
        plt.ylim(0, 50)
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.title("Feasible Region" + (" with Optimal Solution" if objective_function else ""))
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def _find_and_plot_optimal(self, restrictions: List[Restriction], 
                              objective_function: ObjectiveFunction, plt) -> None:
        """
        Find and plot the optimal solution for the given objective function.
        
        Parameters
        ----------
        restrictions : List[Restriction]
            List of linear restrictions.
        objective_function : ObjectiveFunction
            Objective function to optimize.
        plt : matplotlib.pyplot
            Plot object to add the optimal solution.
        """
        # Prepare coefficients for linprog
        if objective_function.optimization_type == "max":
            c = [-objective_function.coeff_x1, -objective_function.coeff_x2]  # Negative for maximization
        else:
            c = [objective_function.coeff_x1, objective_function.coeff_x2]  # Positive for minimization
        
        # Prepare constraint matrices
        A_ub = []
        b_ub = []
        
        for r in restrictions:
            if r.op == "≤":
                A_ub.append([r.a, r.b])
                b_ub.append(r.c)
            else:  # "≥"
                A_ub.append([-r.a, -r.b])  # Multiply by -1 to convert to ≤
                b_ub.append(-r.c)
        
        # Bounds (x1, x2 >= 0)
        bounds = [(0, None), (0, None)]
        
        # Solve the linear programming problem
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        
        if result.success:
            x_opt, y_opt = result.x
            z_opt = objective_function.coeff_x1 * x_opt + objective_function.coeff_x2 * y_opt
            
            # Plot optimal point
            plt.plot(x_opt, y_opt, 'ro', markersize=10)
            plt.annotate(f'Optimal: ({x_opt:.2f}, {y_opt:.2f})\nZ = {z_opt:.2f}', 
                        (x_opt, y_opt), 
                        xytext=(10, 10), 
                        textcoords='offset points',
                        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7),
                        arrowprops=dict(arrowstyle="->"))
            
            # Show result in message box
            messagebox.showinfo("Optimal Solution", 
                               f"Optimal point: ({x_opt:.2f}, {y_opt:.2f})\n"
                               f"Optimal Z value: {z_opt:.2f}")
        else:
            messagebox.showwarning("Solution Not Found", 
                                  "No optimal solution found. The problem may be unbounded or infeasible.")
