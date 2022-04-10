import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation
from typing import Union, Sequence
from collections.abc import Iterable

from structures.BaseParticle import BaseParticle
from controllers.PhysicsController import PhysicsController


class SimulationController:
    def __init__(self, world_size: float, physics_type: str) -> None:
        """
        Initialize the controller a square world of sides=world_size
        :param world_size: Length of the square world
        """

        self.world = self.generate_world(world_size)
        self.number_particles = None
        self.particles = []

        self.MAX_ITERATIONS = 20
        # Set an epsilon to ensure non-zero but almost 0 in some cases
        self.epsilon = sys.float_info.epsilon

        self.physics = PhysicsController(physics_type)

    @staticmethod
    def generate_world(world_size: float) -> np.ndarray:
        # Currently, a useless function
        return np.array([0, world_size])

    def initialize_particles(self, number_particles: int, radius: Union[float, Sequence[float], np.ndarray] = 0.01):
        # TODO: Add a positions option
        # TODO: Add a velocity option
        # If we do not have an iterable list/whatever of radii make a generator to make N particles of same size
        if not isinstance(radius, Iterable) and isinstance(radius, (float, int)):

            def generate_radii(num_particles, r):
                for _ in range(num_particles):
                    yield r
            radius = generate_radii(number_particles, radius)

        self.number_particles = number_particles

        # Generate all of our particles
        for i, rad in enumerate(radius):
            # Currently, all positions are generated at random
            while True:
                overlaps = False
                # Dumb way to get min and max
                # Really just avoiding hardcoding it atm
                minimum, maximum = self.world

                # Place the particle somewhere pseudo-random
                x, y = rad + (1 - 2 * rad) * (np.random.random(2) * maximum)

                # Generate speed between 0.1 and 1.0 m/s
                # Generate direction between [0, 2pi)
                vr = 0.2 * np.random.random() + self.epsilon
                vphi = 2 * np.pi * np.random.random()

                # Convert to cartesian
                vx, vy = vr * np.array([np.cos(vphi), np.sin(vphi)])

                particle = BaseParticle((x, y), (vx, vy), rad, mass=rad)
                #print(particle.position)

                for p in self.particles:
                    if self.physics.is_overlap(particle, p):
                        overlaps = True
                        break

                if not overlaps:
                    self.particles.append(particle)
                    break

    def step_forward(self, dt: float) -> None:
        """
        Method to describe the moving forward by increment of time
        :param dt: time increment (seconds)
        :return: None
        """
        for i, particle in enumerate(self.particles):
            print(f"Moving particle {i}")
            particle.move(dt)

        self.physics.handle_possible_collisions(self.particles)

    def init(self):
        """Initialize the Matplotlib animation."""

        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.ax))
        return self.circles

    def advance_animation(self, dt):
        """Advance the animation by dt, returning the updated Circles list."""

        for i, p in enumerate(self.particles):
            #if i == 0:
            #    print(f"Particle {i}:\nPosition: {p.position}\nVelocity: {p.velocity}")

            p.move(dt)
            self.circles[i].center = p.position
            #if len(self.ax.texts) > 1:
            #    del self.ax.texts[1]
            #    del self.ax.texts[0]
            #self.ax.text(p.x, p.y, str(p.vy))

        self.physics.handle_possible_collisions(self.particles)
        return self.circles

    def animate(self, i):
        """The function passed to Matplotlib's FuncAnimation routine."""

        self.advance_animation(0.1)
        return self.circles

    def do_animation(self, frames=800, save=False):
        fig, self.ax = plt.subplots()
        for s in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[s].set_linewidth(2)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])

        anim = animation.FuncAnimation(fig, self.animate, init_func=self.init,
                                       frames=frames, interval=2, blit=True)
        if save:
            writer = animation.PillowWriter(fps=100, bitrate=1800)
            anim.save('animations/collision.gif', writer=writer)
        else:
            plt.show()
