import numpy as np
from .BaseConstruct import BaseConstruct


class Box(BaseConstruct):
    def __init__(self, position=(0., 0.), velocity=(0., 0.), half_lengths=(1., 1.), border_material='Inf',
                 fill='vacuum', parent=None, styles=None):
        """
        Class to allow the construction of a box
        :param position: sequence of floats describing center position of the box
        :param velocity: sequence of floats describing initial velocity vector
        :param half_lengths: sequence of half lengths (in meters)
        :param border_material: string representing the material name making the borders of this material
        :param fill: string representing what material fills the box
        :param parent: Parent object if any
        :param styles: Visual styles dictionary
        """
        super().__init__(position, velocity, parent, styles)

        self._half_lengths = np.array(half_lengths)

        self.fill = fill
        self.border_material = border_material

    @property
    def hlx(self) -> float:
        return self._half_lengths[0]

    @hlx.setter
    def hlx(self, value: float) -> None:
        assert value >= 0.
        self._half_lengths[0] = value

    @property
    def hly(self) -> float:
        return self._half_lengths[0]

    @hly.setter
    def hly(self, value: float) -> None:
        assert value >= 0.
        self._half_lengths[1] = value
