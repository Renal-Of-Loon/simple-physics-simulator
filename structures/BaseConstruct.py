import numpy as np
from typing import Sequence, Union


def cart2pol(coords):
    x, y = coords
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(coords):
    rho, phi = coords
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


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
        self._radial_velocity = cart2pol(self._velocity)

        self.previous_position = None

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
        self._radial_velocity = cart2pol(value)

    @property
    def radial_velocity(self):
        return self._velocity

    @radial_velocity.setter
    def radial_velocity(self, value: Union[Sequence[float], np.ndarray]) -> None:
        assert isinstance(value, Sequence) or isinstance(value, np.ndarray)
        assert len(value) == 2

        self._radial_velocity = value
        self._velocity = pol2cart(value)

    @property
    def velocity_magnitude(self) -> float:
        # Note that np.linalg is a bit slower than say
        # np.sqrt((v * v).sum(axis=1)) but safer
        # Consider changing to this if needed
        return np.sqrt((self.velocity * self.velocity).sum(axis=0))
