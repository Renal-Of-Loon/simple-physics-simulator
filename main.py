from controllers.SimulationController import SimulationController
from structures.Box import Box

import numpy as np

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    nparticles = 5
    radii = np.random.random(nparticles) * 0.03
    sim = SimulationController('SimpleMechanics')
    world = Box((0., 0.), (0., 0.), (0.5, 0.5), border_material='wood', fill='vacuum')
    #world.add_elements(particles)
    #sim.make_world(world)
    #sim.initialize_particles(nparticles, radii)
    world.generate_box_particles(nparticles, world, radii)
    sim.particles = world.particles

    sim.do_animation(frames=200, save=True)
