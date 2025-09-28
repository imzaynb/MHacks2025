import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Graph:
    def __init__(self, physics_engine):
        self.physics = physics_engine
        self.fig, self.ax = plt.subplots(figsize=(10,6))

        self.line_accel_x, = self.ax.plot([], [], label="Accel X", color="blue")
        self.line_pos_raw, = self.ax.plot([], [], label="Raw Pos X", color="orange")

        self.ax.set_title("Acceleration and X Position")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value")
        self.ax.legend()
        self.ax.grid(True)

        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=10, blit=False)
        plt.ion()

    def update_plot(self, i):
        # Just plot existing physics data
        self.line_accel_x.set_data(self.physics.time_data, self.physics.accel_x_data)
        self.line_pos_raw.set_data(self.physics.time_data, self.physics.position_x_raw)

        if self.physics.time_data:
            self.ax.set_xlim(self.physics.time_data[0], self.physics.time_data[-1])
            all_data = self.physics.accel_x_data + self.physics.position_x_raw
            self.ax.set_ylim(min(all_data), max(all_data))

        return self.line_accel_x, self.line_pos_raw
