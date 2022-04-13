import numpy as np
from itertools import combinations
from scipy import constants

from util.Overlaps import is_radial_overlap
from util.Maths import magnitude


class PhysicsController:
    """
    Controller class to deal with physics interactions
    """
    def __init__(self, physics_type: str, collision_detection: str = 'PairWise', collision_handler: str = 'AfterStep'):
        self.physics_type = physics_type
        self.collision_detection = collision_detection
        self.collision_handler = collision_handler
        self._gravity_acceleration = np.array((0, -0.1 * constants.g))  # m/s^2

    @property
    def g(self):
        return self._gravity_acceleration

    @g.setter
    def g(self, value) -> None:
        self._gravity_acceleration = value

    def increment_construct(self, construct, dt):

        # TODO: Check if static, if not move & check collisions

        if len(construct.children) > 0:
            for child_construct in construct.children:
                self.increment_construct(child_construct, dt)

        if len(construct.particles) > 0:
            self.increment_particles(construct, dt)

    def increment_particles(self, construct, dt):
        for i, p in enumerate(construct.particles):
            #if i == 0:
            #    print(f"Particle {i}:\nPosition: {p.position}\nVelocity: {p.velocity}")

            self.iterate_position(p, dt)

        self.handle_possible_collisions(construct.particles)
        return construct

    def handle_possible_collisions(self, particles: list):
        if self.collision_detection == 'PairWise':
            # Very slow and inefficient way of finding particle overlaps
            particle_pairs = combinations(range(len(particles)), 2)

            for i, j in particle_pairs:
                if is_radial_overlap(particles[i], particles[j]):
                    self.perform_deflection(particles[i], particles[j])

    def perform_deflection(self, particle1, particle2):
        # for shorter equation writing
        x1 = particle1.position
        x2 = particle2.position
        v1 = particle1.velocity
        v2 = particle2.velocity
        m1 = particle1.mass
        m2 = particle2.mass

        if self.physics_type == 'SimpleMechanics':
            # See https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects
            # For details on how these equations came about

            particle1.velocity = v1 - ((2 * m2) / (m1 + m2)) * (
                        np.dot((v1 - v2), (x1 - x2)) / (magnitude(x1 - x2) ** 2)) * (x1 - x2)
            particle2.velocity = v2 - ((2 * m1) / (m2 + m1)) * (
                        np.dot((v2 - v1), (x2 - x1)) / (magnitude(x2 - x1) ** 2)) * (x2 - x1)

            return particle1, particle2

    def handle_parent_collision(self, entity):
        if self.physics_type == 'SimpleMechanics':
            parent = entity.parent
            parent_xlim = np.array([parent.x - parent.hlx, parent.x + parent.hlx])
            parent_ylim = np.array([parent.y - parent.hly, parent.y + parent.hly])
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
                entity.y = entity.radius
                entity.vy = -1. * entity.vy
            if entity.y + entity.radius >= 1:
                entity.y = 1. - entity.radius
                entity.vy = -1. * entity.vy

        return entity

    def iterate_position(self, entity, dt):
        if self.physics_type == 'SimpleMechanics':
            entity.previous_position = entity.position
            entity.position += entity.velocity * dt + 0.5 * self.g * dt ** 2

            # print(self.velocity, dt)
            # print(f"After velocity move: {self.position}")

            self.handle_parent_collision(entity)

            # We adjust velocity after boundary displacement to avoid increasing energy in the system magically
            # If not we are making the "first" increment after impact bigger than before impact
            # Velocity is update when gravity is involved
            # if np.any(np.abs(initial_position - self.position) < POSITION_PRECISION):
            # Acceleration only matters if we've actually *moved*
            entity.velocity += self.g * dt

            entity.energy = self.compute_energy(entity)

            return entity

    def compute_energy(self, entity):
        # E_k = 1/2 * m * v^2
        # E_p = m * g * h

        kinetic = 0.5 * entity.mass * (magnitude(entity.velocity) ** 2)
        potential = entity.mass * self.g * entity.y

        return kinetic + potential
