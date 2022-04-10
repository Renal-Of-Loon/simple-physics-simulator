from controllers.SimulationController import SimulationController
from structures.Box import Box

import numpy as np

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    nparticles = 5
    radii = np.random.random(nparticles) * 0.03
    sim = SimulationController(1.0, 'SimpleMechanics')
    world = Box((0., 0.), (0., 0.), (1., 1.), border_material='wood', fill='vacuum')
    #particles = generate_random_particles(nparticles, radii)
    #world.add_elements(particles)
    #sim.make_world(world)
    sim.initialize_particles(nparticles, radii)

    sim.do_animation(frames=200, save=True)
