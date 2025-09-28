import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
from mytypes import Vec3d  # Your Vec3d dataclass

class Graph:
    def __init__(self, get_acceleration, ema_alpha=0.2):
        self.get_acceleration = get_acceleration
        self.ema_alpha = ema_alpha  # smoothing factor for EMA

        self.time_start = dt.datetime.now().timestamp()
        self.time_data = [0.0]
        self.accel_x_data = [0.0]        # X acceleration
        self.position_x_raw = [0.0]      # Raw X position
        self.position_x_smooth = [0.0]   # EMA-smoothed X position

        # Use Vec3d for velocity and position
        self.velocity = Vec3d(0.0, 0.0, 0.0)
        self.position = Vec3d(0.0, 0.0, 0.0)
        self.ema_position_x = 0.0

        self.data_limit = 50

        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Plot lines
        self.line_accel_x, = self.ax.plot(self.time_data, self.accel_x_data, label="Accel X", color="blue")
        self.line_pos_raw, = self.ax.plot(self.time_data, self.position_x_raw, label="Raw Pos X", color="orange")
        self.line_pos_smooth, = self.ax.plot(self.time_data, self.position_x_smooth, label="Smoothed Pos X", color="red")

        self.ax.set_title("Acceleration and X Position (Raw vs Smoothed)")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value")
        self.ax.legend()
        self.ax.grid(True)

        self.ani = animation.FuncAnimation(self.fig, self.add_data, interval=10, blit=False)
        plt.ion()

    def add_data(self, i):
        # Get acceleration
        acceleration = self.get_acceleration()

        # Current time
        current_time = dt.datetime.now().timestamp()
        self.time_data.append(current_time - self.time_start)

        # Compute dt
        dt_sec = 0.01
        if len(self.time_data) > 1:
            dt_sec = self.time_data[-1] - self.time_data[-2]

        # Only X acceleration
        ax = acceleration.x
        self.accel_x_data.append(ax)

            # Zero velocity if acceleration is near zero
        if abs(ax) == 0:
            self.velocity.x = 0.0

        # Integrate velocity and position
        self.velocity.x += ax * dt_sec
        self.position.x += self.velocity.x * dt_sec
        self.position.x = max(0, min(1920, self.position.x))

        self.position_x_raw.append(self.position.x)

        # EMA smoothing for position
        self.ema_position_x = self.ema_alpha * self.position.x + (1 - self.ema_alpha) * self.ema_position_x
        self.position_x_smooth.append(self.ema_position_x)

        # Print for debugging
        #print(f"Raw X Acceleration: {ax}, Raw X Vel: {self.velocity.x}, Raw X Pos: {self.position.x:.2f}, Smoothed X Pos: {self.ema_position_x:.2f}")
    

        # Trim data arrays to data_limit
        self.time_data[:] = self.time_data[-self.data_limit:]
        self.accel_x_data[:] = self.accel_x_data[-self.data_limit:]
        self.position_x_raw[:] = self.position_x_raw[-self.data_limit:]
        self.position_x_smooth[:] = self.position_x_smooth[-self.data_limit:]

        # Update plot
        self.line_accel_x.set_data(self.time_data, self.accel_x_data)
        self.line_pos_raw.set_data(self.time_data, self.position_x_raw)
        self.line_pos_smooth.set_data(self.time_data, self.position_x_smooth)

        # Rescale axes
        self.ax.set_xlim(self.time_data[0], self.time_data[-1])
        all_visible = self.accel_x_data + self.position_x_raw + self.position_x_smooth
        if all_visible:
            self.ax.set_ylim(min(all_visible), max(all_visible))

        self.ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        return self.line_accel_x, self.line_pos_raw, self.line_pos_smooth
