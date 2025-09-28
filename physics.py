import datetime as dt
from mytypes import Vec3d

class PhysicsEngine:
    def __init__(self, get_acceleration):
        self.get_acceleration = get_acceleration

        self.time_start = dt.datetime.now().timestamp()
        self.time_data = []

        # X and Y data
        self.accel_x_data = []
        self.accel_y_data = []
        self.position_x_raw = []
        self.position_y_raw = []

        self.velocity = Vec3d(0.0, 0.0, 0.0)
        self.position = Vec3d(0.0, 0.0, 0.0)

    def update(self):
        # Get acceleration
        acceleration = self.get_acceleration()
        current_time = dt.datetime.now().timestamp()
        self.time_data.append(current_time - self.time_start)

        # Compute dt
        dt_sec = 0.01
        if len(self.time_data) > 1:
            dt_sec = self.time_data[-1] - self.time_data[-2]

        # --- X axis ---
        ax = max(min(acceleration.x, 4000.0), -4000.0)
        self.accel_x_data.append(ax)

        if ax == 0:
            self.velocity.x = 0.0
        else:
            self.velocity.x += ax * dt_sec

        self.velocity.x = max(min(self.velocity.x, 1000.0), -1000.0)
        self.position.x += self.velocity.x * dt_sec
        self.position.x = max(0, min(1080, self.position.x))
        self.position_x_raw.append(self.position.x)

        # --- Y axis ---
        ay = max(min(acceleration.y, 4000.0), -4000.0)
        self.accel_y_data.append(ay)

        if ay == 0:
            self.velocity.y = 0.0
        else:
            self.velocity.y += ay * dt_sec

        self.velocity.y = max(min(self.velocity.y, 1000.0), -1000.0)
        self.position.y += self.velocity.y * dt_sec
        self.position.y = max(0, min(1920, self.position.y))  # assuming 1080p vertical clamp
        self.position_y_raw.append(self.position.y)

        # Debug prints
        print(f"Time: {self.time_data[-1]:.2f}s, "
              f"Accel X: {ax:.2f}, Vel X: {self.velocity.x:.2f}, Pos X: {self.position.x:.2f}, "
              f"Accel Y: {ay:.2f}, Vel Y: {self.velocity.y:.2f}, Pos Y: {self.position.y:.2f}")

        # Keep data arrays reasonable
        limit = 50
        self.time_data[:] = self.time_data[-limit:]
        self.accel_x_data[:] = self.accel_x_data[-limit:]
        self.accel_y_data[:] = self.accel_y_data[-limit:]
        self.position_x_raw[:] = self.position_x_raw[-limit:]
        self.position_y_raw[:] = self.position_y_raw[-limit:]

        return ax, self.velocity.x, self.position.x, ay, self.velocity.y, self.position.y
