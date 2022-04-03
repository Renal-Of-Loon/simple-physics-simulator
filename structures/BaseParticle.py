import numpy as np
from typing import Sequence, Union


class BaseParticle:
    """
    Class representing the base of any particle
    """

    def __init__(self, x, y, vx, vy, radius=0.01, mass=1):
        """
        Init for BaseParticle
        :param x: relative position in x (meters)
        :param y: relative position in y (meters)
        :param vx: velocity vector in x (m/s)
        :param vy: velocity vector in y (m/s)
        :param radius: radius of particle (m)
        :parma mass :mass of particle (kg)
        """

        # Set basic position, velocity, and radius values
        self._position = np.array((x, y))
        self._velocity = np.array((vx, vy))
        self._radius = radius

        self.mass = mass

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
        return self._velocity[0]

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
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        assert value > 0.
        self._radius = value

    def move(self, dt: float) -> None:
        """
        Method governing particle displacement
        :param dt: variation in time (seconds)
        """

        # New position = velocity * time interval
        self._position = self._velocity * dt

        # For now let's deal with wall physics here
        # Walls are assumed to be at 0m and 1m in both x and y
        if self.x - self.radius < 0:
            # If we passed the x = 0 wall, bounce back
            self.x = self.radius
            self.vx = -self.vx
        if self.x + self.radius > 1:
            # If we passed the x = 1 wall...
            self.x = 1 - self.radius
            self.vx = -self.vx

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy
        if self.y + self.radius > 1:
            self.y = 1 - self.radius
            self.vy = -self.vy
