import numpy as np
from scipy import constants
from typing import Sequence, Union


class BaseConstruct:
    """
        Class representing the base of any construct/object
    """

    def __init__(self, position, velocity, parent, styles=None):
        """
        Init for base construct
        :param position: Sequence of floats definining position in meters
        :param velocity: Sequence of floats definining velocity in meters/seconds
        :param parent: Parent object
        :param styles: styles dictionary
        """
        # Set basic position, velocity
        self._position = np.array(position)
        self._velocity = np.array(velocity)

        self._gravity_acceleration = np.array((0, -0.1 * constants.g))  # m/s^2

        self.parent = parent
        self.children = []
        self.particles = []

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
    def vx(self) -> float:
        return self._velocity[0]

    @vx.setter
    def vx(self, value: float) -> None:
        self._velocity[0] = value

    @property
    def vy(self) -> float:
        return self._velocity[1]

    @vy.setter
    def vy(self, value: float) -> None:
        self._velocity[1] = value

    @property
    def velocity(self) -> np.ndarray:
        return self._velocity

    @velocity.setter
    def velocity(self, value: Union[Sequence[float], np.ndarray]) -> None:
        assert isinstance(value, Sequence) or isinstance(value, np.ndarray)
        assert len(value) == 2

        self._velocity = value

    @property
    def velocity_magnitude(self) -> float:
        # Note that np.linalg is a bit slower than say
        # np.sqrt((v * v).sum(axis=1)) but safer
        # Consider changing to this if needed
        return np.sqrt((self.velocity * self.velocity).sum(axis=0))

    @property
    def g(self):
        return self._gravity_acceleration

    @g.setter
    def g(self, value) -> None:
        self._gravity_acceleration = value
