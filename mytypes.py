from dataclasses       import dataclass

@dataclass
class Vec3d:
    x: float
    y: float
    z: float

    def clamp(self, min_x, max_x, min_y, max_y, min_z, max_z):
        self.x = min(max(self.x, min_x), max_x)
        self.y = min(max(self.y, min_y), max_y)
        self.z = min(max(self.z, min_z), max_z)