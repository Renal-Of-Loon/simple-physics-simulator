import numpy as np
from itertools import combinations
from scipy import constants

from util.Overlaps import is_radial_overlap
from util.Maths import magnitude


class PhysicsController:
    """
    Controller class to deal with physics interactions
    """
    def __init__(self, physics_type: str, collision_detection: str = 'PairWise',
                 collision_handler: str = 'DiscreteDetection'):
        self.physics_type = physics_type
        self.collision_detection = collision_detection
        self.collision_handler = collision_handler
        self._gravity_acceleration = np.array((0, -0.1 * constants.g))  # m/s^2

        # Set epsilon for ensuring non-zero values in some cases
        self.epsilon = np.finfo(float).eps

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

        # After each child has been "moved forward in time" check to see if we got a collision
        # This detect also calls collision handler, function name unclear I guess
        self.detect_collisions(construct.particles)

        return construct

    def handle_particle_collisions(self, particle1, particle2):
        if self.collision_handler == 'DiscreteDetection':
            self.perform_deflection(particle1, particle2)

        if self.collision_handler == 'ContinuousDetection':
            print('Not yet implementing, no collision handled.')
            self.perform_deflection(particle1, particle2)
            # Use binary search to trace back until we get within a given precision of two particles
            # just entering in contact.
            # Is finding time required to be equidistant to COM valid?

    def detect_collisions(self, particles: list):
        # Sweep and prune
        # Uniform grid partition
        # K-D Tree space partition
        # Object Partition
        #   Bounding Volume Hierarchies

        if self.collision_detection == 'PairWise':
            # Very slow and inefficient way of finding particle overlaps
            particle_pairs = combinations(range(len(particles)), 2)

            for i, j in particle_pairs:
                if is_radial_overlap(particles[i], particles[j]):
                    self.handle_particle_collisions(particles[i], particles[j])

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

    def parent_collision_regression(self, entity, pos_index, dt, wall_position):
        # God I hate how this is implemented, please don't leave it like this
        # TODO: fix this garbage

        # We want to use before and after position, make an equation governing time vs position
        # basically time = slope * position + intercept
        # Here our slope(s) will be time vs x and time vs y
        # We use dt as our "rise" (from rise over run) since it's already the time interval
        slope = (dt - 0) / (entity.position[pos_index] - entity.previous_position[pos_index])
        intercept = dt - slope * entity.position[pos_index]

        if np.abs(entity.previous_position[pos_index] - (wall_position + entity.radius)) < np.abs(entity.previous_position[pos_index] - (wall_position - entity.radius)):
            wall_intercept = wall_position + entity.radius
        else:
            wall_intercept = wall_position - entity.radius
        time_to_wall = slope * wall_intercept + intercept

        # With time_to_wall we can determine coordinates at impact
        position_impact = entity.previous_position[pos_index] + entity.velocity[pos_index] * time_to_wall

        # Now we flip the velocity
        # Weird way of determining in which axis we hit wall
        # If the difference between wall and calculated position is smaller than a small value (i.e they are almost
        # identical within rounding issues), velocity needs to flip
        #wall_sign_flip = np.where(np.abs(position_impact - wall_position) < 0.001, -1, 0)
        entity.velocity[pos_index] = -1 * entity.velocity[pos_index] #wall_sign_flip * entity.velocity

        # And now we let the particle "finish" it's run
        entity.position[pos_index] = position_impact + entity.velocity[pos_index] * (dt - time_to_wall)

    def handle_parent_collision(self, entity, dt):
        parent = entity.parent
        parent_xlim = np.array([parent.x - parent.hlx, parent.x + parent.hlx])
        parent_ylim = np.array([parent.y - parent.hly, parent.y + parent.hly])

        if self.collision_handler == 'ContinuousDetection':
            # For now let's deal with wall physics here
            if entity.x - entity.radius <= parent_xlim[0]:
                # If we passed the x = 0 wall, bounce back
                self.parent_collision_regression(entity, 0, dt, 0)
            if entity.x + entity.radius >= parent_xlim[1]:
                # If we passed the x = 1 wall...
                self.parent_collision_regression(entity, 0, dt, 1)

            if entity.y - entity.radius <= parent_ylim[0]:
                self.parent_collision_regression(entity, 1, dt, 0)
            if entity.y + entity.radius >= parent_ylim[1]:
                self.parent_collision_regression(entity, 1, dt, 1)

        if self.collision_handler == 'DiscreteDetection':
            # For now let's deal with wall physics here
            if entity.x - entity.radius <= parent_xlim[0]:
                # If we passed the x = 0 wall, bounce back
                entity.x = entity.radius
                entity.vx = -1. * entity.vx
            if entity.x + entity.radius >= parent_xlim[1]:
                # If we passed the x = 1 wall...
                entity.x = 1. - entity.radius
                entity.vx = -1. * entity.vx

            if entity.y - entity.radius <= parent_ylim[0]:
                entity.y = entity.radius
                entity.vy = -1. * entity.vy
            if entity.y + entity.radius >= parent_ylim[1]:
                entity.y = 1. - entity.radius
                entity.vy = -1. * entity.vy
        return entity

    def iterate_position(self, entity, dt):
        if self.physics_type == 'SimpleMechanics':
            entity.previous_position = np.copy(entity.position)
            entity.position += entity.velocity * dt# + 0.5 * self.g * dt ** 2

            # print(self.velocity, dt)
            # print(f"After velocity move: {self.position}")

            self.handle_parent_collision(entity, dt)

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
