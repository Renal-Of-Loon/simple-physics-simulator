import numpy as np
from scipy import constants
from typing import Sequence, Union


class BaseConstruct:
    """
        Class representing the base of any construct/object
    """

    def __init__(self, x, y, parent, styles=None):
        """
        Init for BaseParticle
        :param x: relative position in x (meters)
        :param y: relative position in y (meters)
        """

        # Set basic position, velocity, and radius values
        self._position = np.array((x, y))
        self._gravity_acceleration = np.array((0, -0.1 * constants.g))  # m/s^2

        self.parent = parent
        self.children = {}

        if styles is None:
            self.styles = {'color': np.random.rand(3,), 'edgecolor': None}
        else:
            self.styles = styles

    # Define useful getter and setters
    @property
    def x(self) -> float:
        return self._position[0]

    @x.setter
    def x(self, value: float) -> None:
        self._position[0] = value

    @property
    def y(self) -> float:
        return self._position[1]

    @y.setter
    def y(self, value: float) -> None:
        self._position[1] = value

    @property
    def position(self) -> np.ndarray:
        return self._position

    @position.setter
    def position(self, value: Union[Sequence[float], np.ndarray]) -> None:
        assert isinstance(value, Sequence) or isinstance(value, np.ndarray)
        assert len(value) == 2

        self._position = value

    @property
    def g(self):
        return self._gravity_acceleration

    @g.setter
    def g(self, value) -> None:
        self._gravity_acceleration = value
