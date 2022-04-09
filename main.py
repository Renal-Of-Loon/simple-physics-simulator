from controllers.SimulationController import SimulationController


import numpy as np

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #sim = SimulationController(1.0)
    #sim.initialize_particles(2, 0.01)

    #p1 = BaseParticle(0.1, 0.1, 5, 0, mass=4)
    #p2 = BaseParticle(0.1, 0.1, 0, 0, mass=2)

    #phys = PhysicsController('SimpleMechanics')
    #p1f, p2f = phys.handle_particle_collisions(p1, p2)

    #print(p1f.velocity, p2f.velocity, p1f.color)

    nparticles = 5
    radii = np.random.random(nparticles) * 0.03
    sim = SimulationController(1.0, 'SimpleMechanics')
    #world = create_square(borders='wood', fill='vacuum')
    #particles = generate_random_particles(nparticles, radii)
    #world.add_elements(particles)
    #sim.make_world(world)
    sim.initialize_particles(nparticles, radii)

    sim.do_animation(frames=200, save=True)
