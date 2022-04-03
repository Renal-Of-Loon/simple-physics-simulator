from structures.BaseParticle import BaseParticle
from controllers.SimulationController import SimulationController
from controllers.PhysicsController import PhysicsController
import numpy as np

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #sim = SimulationController(1.0)
    #sim.initialize_particles(2, 0.01)

    p1 = BaseParticle(0.1, 0.1, 5, 0, mass=4)
    p2 = BaseParticle(0.1, 0.1, 0, 0, mass=2)

    phys = PhysicsController('SimpleMechanics')
    p1f, p2f = phys.handle_particle_collisions(p1, p2)

    print(p1f.velocity, p2f.velocity)
