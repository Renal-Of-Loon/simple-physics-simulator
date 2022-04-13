import numpy as np
from typing import Sequence, Union
import matplotlib as mpl

from .BaseConstruct import BaseConstruct
from util.Maths import magnitude

POSITION_PRECISION = 1e-4


class BaseParticle(BaseConstruct):
    """
    Class representing the base of any particle
    """

    def __init__(self, position, velocity, radius=0.01, mass=1, parent=None, styles=None):
        """
        Init for BaseParticle
        :param x: relative position in x (meters)
        :param y: relative position in y (meters)
        :param vx: velocity vector in x (m/s)
        :param vy: velocity vector in y (m/s)
        :param radius: radius of particle (m)
        :parma mass :mass of particle (kg)
        """

        # Init position and styles
        super().__init__(position, velocity, parent, styles)

        # Set basic position, velocity, and radius values
        self._radius = radius

        self.mass = mass
        self.energy = 0.0

    # Define useful getter and setters
    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        assert value > 0.
        self._radius = value

    def draw(self, ax):
        circle = mpl.patches.Circle(xy=self.position, radius=self.radius, **self.styles)
        ax.add_patch(circle)

        #ax.text(self.x, self.y, str(self.vy))

        return circle
