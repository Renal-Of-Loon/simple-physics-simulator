import numpy as np
from itertools import combinations

from .SimulationController import particle_overlap


class PhysicsController:
    """
    Controller class to deal with physics interactions
    """
    def __init__(self, physics_type: str):
        self.physics = physics_type

    def check_collisions(self, particles: list):
        # Very slow and inefficient way of finding particle overlaps
        particle_pairs = combinations(range(len(particles)), 2)

        for i, j in particle_pairs:
            if particle_overlap(particles[i], particles[j]):
                self.handle_particle_collisions(particles[i], particles[j])

    def handle_particle_collisions(self, particle1, particle2):

        if self.physics == 'SimpleMechanics':
            # Use simple elastic collisions
            # Use center of mass reference frame
            # v_{cm} = (m_1*v1 + m_2*v_2) / (m1 + m2)
            # v_{n,f} = -v_n + 2*v_{cm}
            velocity_center_mass = (particle1.mass * particle1.velocity + particle2.mass * particle2.velocity) \
                                   / (particle1.mass + particle2.mass)

            particle1.velocity = -1 * particle1.velocity + 2 * velocity_center_mass
            particle2.velocity = -1 * particle2.velocity + 2 * velocity_center_mass

            return particle1, particle2
