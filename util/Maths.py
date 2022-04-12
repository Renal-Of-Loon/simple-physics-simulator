import numpy as np


def cart2pol(coordinates):
    x, y = coordinates
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(coordinates):
    rho, phi = coordinates
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def magnitude(vector):
    return np.sqrt((vector * vector).sum(axis=0))
