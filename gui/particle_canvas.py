"""Animated particle background using Tkinter Canvas.

Particles move randomly and connect with nearby particles to create
a modern "constellation" effect.
"""

import tkinter as tk
import random
import math


class ParticleCanvas(tk.Canvas):
    """Canvas with animated moving particles."""

    def __init__(self, parent, num_particles: int = 25, width: int = 640, height: int = 420, **kwargs):
        super().__init__(parent, width=width, height=height, bg="#0f172a", highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.particles = []

        for _ in range(num_particles):
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            dx = random.uniform(-1.5, 1.5)
            dy = random.uniform(-1.5, 1.5)
            r = 3
            self.particles.append([x, y, dx, dy, r])

        self.after(30, self.animate)

    def animate(self):
        """Update particle positions and redraw frame."""
        self.delete("all")

        # Draw connections first
        for i, p1 in enumerate(self.particles):
            for j, p2 in enumerate(self.particles[i + 1 :], start=i + 1):
                dist = math.dist((p1[0], p1[1]), (p2[0], p2[1]))
                if dist < 100:  # draw line if close
                    opacity = max(0, 150 - int(dist))  # fade with distance
                    color = f"#38bdf8{opacity:02x}" if opacity > 30 else "#38bdf8"
                    self.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=1)

        # Update and draw particles
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]

            # Bounce from walls
            if p[0] <= 0 or p[0] >= self.width:
                p[2] *= -1
            if p[1] <= 0 or p[1] >= self.height:
                p[3] *= -1

            self.create_oval(
                p[0] - p[4],
                p[1] - p[4],
                p[0] + p[4],
                p[1] + p[4],
                fill="#38bdf8",
                outline="",
            )

        self.after(30, self.animate)

