import numpy as np
from typing import Sequence, Union
import matplotlib as mpl

from .BaseConstruct import BaseConstruct


class BaseParticle(BaseConstruct):
    """
    Class representing the base of any particle
    """

    def __init__(self, x, y, vx, vy, radius=0.01, mass=1, styles=None):
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
        super().__init__(x, y, None, styles)

        # Set basic position, velocity, and radius values
        self._velocity = np.array((vx, vy))
        self._radius = radius

        self.mass = mass
        self.energy = self.compute_energy()

    # Define useful getter and setters
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
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        assert value > 0.
        self._radius = value

    def compute_energy(self) -> float:
        # E_k = 1/2 * m * v^2
        # E_p = m * g * h

        kinetic = 0.5 * self.mass * (self.velocity_magnitude ** 2)
        potential = self.mass * self.g * self.y

        return kinetic + potential

    def move(self, dt: float) -> None:
        """
        Method governing particle displacement
        :param dt: variation in time (seconds)
        """

        # New position = velocity * time interval
        self._position += self._velocity * dt + 0.5 * self.g * dt**2

        #print(self.velocity, dt)
        #print(f"After velocity move: {self.position}")

        # For now let's deal with wall physics here
        # Walls are assumed to be at 0m and 1m in both x and y
        if self.x - self.radius < 0:
            # If we passed the x = 0 wall, bounce back
            self.x = self.radius
            self.vx = -1. * self.vx
        if self.x + self.radius > 1:
            # If we passed the x = 1 wall...
            self.x = 1. - self.radius
            self.vx = -1. * self.vx

        if self.y - self.radius <= 0:
            #print(f"Reached floor, adjusting\nFrom: Position: {self.position}; Velocity: {self.velocity}")
            #print(self.vy)
            #print(-1. * self.vy)
            self.y = self.radius
            self.vy = -1. * self.vy
            #print(f"To: Position: {self.position}; Velocity: {self.velocity}")
        if self.y + self.radius >= 1:
            #print(f"Reached ceil, adjusting\nFrom: Position: {self.position}; Velocity: {self.velocity}")
            self.y = 1. - self.radius
            self.vy = -1. * self.vy
            #print(self.velocity, self.vy)
            #print(-1. * self.vy)
            #print(f"To: Position: {self.position}; Velocity: {self.velocity}")

        # We adjust velocity after boundary displacement to avoid increasing energy in the system magically
        # If not we are making the "first" increment after impact bigger than before impact
        # Velocity is update when gravity is involved
        self._velocity += self.g * dt

        self.compute_energy()

    def draw(self, ax):
        circle = mpl.patches.Circle(xy=self.position, radius=self.radius, **self.styles)
        ax.add_patch(circle)

        #ax.text(self.x, self.y, str(self.vy))

        return circle
