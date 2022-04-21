from controllers.SimulationController import SimulationController
from structures.Box import Box
from structures.BaseParticle import BaseParticle

import numpy as np

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    nparticles = 10
    radii = np.random.random(nparticles) * 0.03
    sim = SimulationController('SimpleMechanics', collision_handler='ContinuousDetection')
    world = Box((0.5, 0.5), (0., 0.), (0.5, 0.5), border_material='wood', fill='vacuum')
    #world.add_elements(particles)
    sim.generate_world(world)
    #sim.initialize_particles(nparticles, radii)

    #p1 = BaseParticle((0.1, 0.4), (-0.05, 0), 0.05, 1)
    #p1.parent = world
    #p2 = BaseParticle((0.29, 0.1), (-0.01, 0), 0.05, 1)
    #sim.particles = [p1]

    world.generate_box_particles(nparticles, world, radii)
    sim.particles = world.particles
    sim.physics.g = 0.

    sim.do_animation(frames=100, save=True)
