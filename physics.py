# python libs
from datetime import datetime as dt

# our fiels
from helpers import clamp, Vec3d

class Physics:
    def __init__(self, get_acceleration):
        self.time_start = dt.now().timestamp()
        self.time_prev  = None
        self.get_acceleration = get_acceleration

        self.acceleration      = Vec3d(0.0, 0.0, 0.0)
        self.velocity          = Vec3d(0.0, 0.0, 0.0)
        self.position          = Vec3d(1920/2, 1080/2, 0.0)
        
        self.paused = False

    def step(self):
        if self.paused:
            return

        raw_acceleration = self.get_acceleration()
        self.time_now = dt.now().timestamp()

        delta_t       = (self.time_now - self.time_start) if self.time_prev == None else (self.time_now - self.time_prev)
        delta_t       = clamp(delta_t, 0, 0.005)

        self.acceleration.x = clamp(raw_acceleration.x, -4000.0, 4000.0)
        adjusted_velocity_x = self.velocity.x + self.acceleration.x * delta_t if self.acceleration.x != 0 else 0
        self.velocity.x = clamp(adjusted_velocity_x, -1000.0, 1000)
        self.position.x = clamp(self.position.x + self.velocity.x * delta_t, 0, 1080)
        
        self.acceleration.y = clamp(raw_acceleration.y, -4000.0, 4000.0)
        adjusted_velocity_y = self.velocity.y + self.acceleration.y * delta_t if self.acceleration.y != 0 else 0
        self.velocity.y = clamp(adjusted_velocity_y, -1000.0, 1000)
        self.position.y = clamp(self.position.y + self.velocity.y * delta_t, 0, 1920)
        
        self.acceleration.z = clamp(raw_acceleration.z, -4000.0, 4000.0)
        adjusted_velocity_z = self.velocity.z + self.acceleration.z * delta_t if self.acceleration.z != 0 else 0
        self.velocity.z = clamp(adjusted_velocity_z, -1000.0, 1000)
        self.position.z = clamp(self.position.z + self.velocity.z * delta_t, 0, 1080)

        self.time_prev = self.time_now



    def setPaused(self, value: bool):
        self.paused = bool
