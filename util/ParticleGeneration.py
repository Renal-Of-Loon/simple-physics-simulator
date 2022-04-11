import numpy as np
from typing import Union, Sequence
from collections.abc import Iterable

from structures.BaseParticle import BaseParticle
from .Overlaps import is_radial_overlap


def _guarantee_radii_sequence(radius, amount):
    if not isinstance(radius, Iterable) and isinstance(radius, (float, int)):

        def generate_radii(num_particles, r):
            for _ in range(num_particles):
                yield r
        radius = generate_radii(amount, radius)

    return radius


def generate_particles_in_box(number_particles: int, parent, radius: Union[float, Sequence[float], np.ndarray] = 0.01):
    # TODO: Add a positions option
    # TODO: Add a velocity option
    # If we do not have an iterable list/whatever of radii make a generator to make N particles of same size
    radius = _guarantee_radii_sequence(radius, number_particles)

    parent_size = parent.half_lengths * 2.

    # Generate all of our particles
    for i, rad in enumerate(radius):
        # Currently, all positions are generated at random
        while True:
            overlaps = False
            # Dumb way to get min and max
            # Really just avoiding hardcoding it atm

            # Place the particle somewhere pseudo-random
            x, y = rad + (1 - 2 * rad) * (np.random.random(2) * parent_size)

            # Generate speed between 0. and 1.0 m/s
            # Generate direction between [0, 2pi)
            vr = 0.2 * np.random.random()
            vphi = 2 * np.pi * np.random.random()

            # Convert to cartesian
            vx, vy = vr * np.array([np.cos(vphi), np.sin(vphi)])

            particle = BaseParticle((x, y), (vx, vy), rad, mass=rad)
            # print(particle.position)

            for child in parent.particles:
                overlaps = is_radial_overlap(particle, child)
                if overlaps:
                    break

            if not overlaps:
                parent.particles.append(particle)
                break
