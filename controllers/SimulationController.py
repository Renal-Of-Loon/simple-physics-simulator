import sys
import numpy as np
from typing import Union, Sequence
from collections.abc import Iterable

from structures.BaseParticle import BaseParticle


def particle_overlap(particle1: BaseParticle, particle2: BaseParticle) -> bool:
    return np.hypot(*(particle1.position - particle2.position)) < particle1.radius + particle2.radius


class SimulationController:
    def __init__(self, world_size: float) -> None:
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
                # Dumb way to get min and max
                # Really just avoiding hardcoding it atm
                minimum, maximum = self.world

                # Place the particle somewhere pseudo-random
                x, y = rad + (1 - 2 * rad) * (np.random.random(2) * maximum)

                # Generate speed between 0.1 and 1.0 m/s
                # Generate direction between [0, 2pi)
                vr = 0.1 * np.random.random() + self.epsilon
                vphi = 2 * np.pi * np.random.random()

                # Convert to cartesian
                vx, vy = vr * np.array([np.cos(vphi), np.sin(vphi)])

                particle = BaseParticle(x, y, vx, vy, rad)

                for p in self.particles:
                    if particle_overlap(particle, p):
                        break

                self.particles.append(particle)
                break

