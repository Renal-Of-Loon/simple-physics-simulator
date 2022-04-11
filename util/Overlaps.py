import numpy as np

from structures.BaseParticle import BaseParticle


def is_radial_overlap(particle1: BaseParticle, particle2: BaseParticle) -> bool:
    return np.hypot(*(particle1.position - particle2.position)) < particle1.radius + particle2.radius
