import numpy as np
from itertools import combinations

from util.Overlaps import is_radial_overlap


class PhysicsController:
    """
    Controller class to deal with physics interactions
    """
    def __init__(self, physics_type: str):
        self.physics = physics_type

    def increment_construct(self, construct):

        # TODO: Check if static, if not move & check collisions

        if len(construct.children) > 0:
            for child_construct in construct.children:
                self.increment_construct(child_construct)

        if len(construct.particles) > 0:
            self.increment_particles(construct)

    def handle_possible_collisions(self, particles: list):
        # Very slow and inefficient way of finding particle overlaps
        particle_pairs = combinations(range(len(particles)), 2)

        for i, j in particle_pairs:
            if is_radial_overlap(particles[i], particles[j]):
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

            # Now move them *out* of each other
            """
            center = np.mean([particle1.position, particle2.position], axis=0)

            if particle1.x <= particle2.x:
                particle1.x = center[0] - particle1.radius
                particle2.x = center[0] + particle2.radius
            else:
                particle1.x = center[0] + particle1.radius
                particle2.x = center[0] - particle2.radius

            if particle1.y <= particle2.y:
                particle1.y = center[1] - particle1.radius
                particle2.y = center[1] + particle2.radius
            else:
                particle1.y = center[1] + particle1.radius
                particle2.y = center[1] - particle2.radius
            """

            return particle1, particle2

    def iterate_position(self, entity, dt):
        if self.physics == 'SimpleMechanics':
            initial_position = entity.position
            # New position = velocity * time interval
            entity.position += entity.velocity * dt + 0.5 * entity.g * dt ** 2

            # print(self.velocity, dt)
            # print(f"After velocity move: {self.position}")

            # For now let's deal with wall physics here
            # Walls are assumed to be at 0m and 1m in both x and y
            if entity.x - entity.radius < 0:
                # If we passed the x = 0 wall, bounce back
                entity.x = entity.radius
                entity.vx = -1. * entity.vx
            if entity.x + entity.radius > 1:
                # If we passed the x = 1 wall...
                entity.x = 1. - entity.radius
                entity.vx = -1. * entity.vx

            if entity.y - entity.radius <= 0:
                # print(f"Reached floor, adjusting\nFrom: Position: {self.position}; Velocity: {self.velocity}")
                # print(self.vy)
                # print(-1. * self.vy)
                entity.y = entity.radius
                entity.vy = -1. * entity.vy
                # print(f"To: Position: {self.position}; Velocity: {self.velocity}")
            if entity.y + entity.radius >= 1:
                # print(f"Reached ceil, adjusting\nFrom: Position: {self.position}; Velocity: {self.velocity}")
                entity.y = 1. - entity.radius
                entity.vy = -1. * entity.vy
                # print(self.velocity, self.vy)
                # print(-1. * self.vy)
                # print(f"To: Position: {self.position}; Velocity: {self.velocity}")

            # We adjust velocity after boundary displacement to avoid increasing energy in the system magically
            # If not we are making the "first" increment after impact bigger than before impact
            # Velocity is update when gravity is involved
            # if np.any(np.abs(initial_position - self.position) < POSITION_PRECISION):
            # Acceleration only matters if we've actually *moved*
            entity.velocity += entity.g * dt

            entity.compute_energy()

            return entity
