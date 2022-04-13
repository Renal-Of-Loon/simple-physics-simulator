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
    def __init__(self, physics_type: str) -> None:
        """
        Initialize the controller a square world of sides=world_size
        :param physics_type: String describing the physics to work with
        """

        self.world = None
        self.number_particles = None
        self.particles = []
        self.circles = []

        self.MAX_ITERATIONS = 20
        # Set an epsilon to ensure non-zero but almost 0 in some cases
        self.epsilon = sys.float_info.epsilon

        self.physics = PhysicsController(physics_type)

    def generate_world(self, world):
        self.world = world

    #def step_forward(self, dt: float) -> None:
    #    """
    #    Method to describe the moving forward by increment of time
    #    :param dt: time increment (seconds)
    #    :return: None
    #    """
    #    for i, particle in enumerate(self.particles):
    #        print(f"Moving particle {i}")
    #        self.particles[i] = self.physics.iterate_position(particle, dt)
    #        #particle.move(dt)
    #
    #    self.physics.handle_possible_collisions(self.particles)

    def init(self):
        """Initialize the Matplotlib animation."""

        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.ax))
        return self.circles

    def advance_animation(self, dt):
        """Advance the animation by dt, returning the updated Circles list."""

        #self.physics.increment_construct(self.world, dt)
        ##Loop over everything and assign to old self.circles
        #self.draw_world()

        for i, p in enumerate(self.particles):
            #if i == 0:
            #    print(f"Particle {i}:\nPosition: {p.position}\nVelocity: {p.velocity}")

            self.physics.iterate_position(p, dt)
            self.circles[i].center = p.position

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
