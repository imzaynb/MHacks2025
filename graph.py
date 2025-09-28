import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
from helpers import Vec3d  # Your Vec3d dataclass

class Graph:
    def __init__(self, get_acceleration, get_velocity, get_position):
        self.get_acceleration = get_acceleration
        self.get_velocity = get_velocity
        self.get_position = get_position

        self.time_start = dt.datetime.now().timestamp()
        self.time_data = []

        # X's
        self.acceleration_xs = []     
        self.velocity_xs = []     
        self.position_xs_raw = []    

        # Y's 
        self.acceleration_ys = []     
        self.velocity_ys = []     
        self.position_ys_raw = []   

        # Z's
        self.acceleration_zs = []     
        self.velocity_zs = []     
        self.position_zs_raw = []   
        
        self.data_limit = 50

        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Plot lines
        self.line_acceleration_x,    = self.ax.plot(self.time_data, self.acceleration_xs, label="Accel X", color="blue")
        self.line_velocity_x,        = self.ax.plot(self.time_data, self.velocity_xs, label="Accel X", color="green")
        self.line_position_x_raw,    = self.ax.plot(self.time_data, self.position_xs_raw, label="Raw Pos X", color="orange")
        
        self.line_acceleration_y,    = self.ax.plot(self.time_data, self.acceleration_ys, label="Accel y", color="blue")
        self.line_velocity_y,        = self.ax.plot(self.time_data, self.velocity_ys, label="Accel y", color="green")
        self.line_position_y_raw,    = self.ax.plot(self.time_data, self.position_ys_raw, label="Raw Pos y", color="orange")
        
        self.line_acceleration_z,    = self.ax.plot(self.time_data, self.acceleration_zs, label="Accel z", color="blue")
        self.line_velocity_z,        = self.ax.plot(self.time_data, self.velocity_zs, label="Accel z", color="green")
        self.line_position_z_raw,    = self.ax.plot(self.time_data, self.position_zs_raw, label="Raw Pos z", color="orange")
        
        self.ax.set_title("Acceleration, Velocity, Position, and Smoothed Position")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value")
        self.ax.legend()
        self.ax.grid(True)

        self.ani = animation.FuncAnimation(self.fig, self.add_data, interval=10, blit=False)
        plt.ion()

    def add_data(self, i):
        # Get acceleration
        acceleration = self.get_acceleration()
        velocity = self.get_velocity()
        position = self.get_position()

        # Current time
        current_time = dt.datetime.now().timestamp()
        self.time_data.append(current_time - self.time_start)

        # Only X acceleration
        a_x = acceleration.x
        a_y = acceleration.y
        a_z = acceleration.z

        v_x = velocity.x
        v_y = velocity.y
        v_z = velocity.z
        
        p_x = position.x
        p_y = position.y
        p_z = position.z
       
        self.acceleration_xs.append(a_x)
        self.acceleration_ys.append(a_y)
        self.acceleration_zs.append(a_z)
        
        self.velocity_xs.append(v_x)
        self.velocity_ys.append(v_y)
        self.velocity_zs.append(v_z)
        
        self.position_xs_raw.append(p_x)
        self.position_ys_raw.append(p_y)
        self.position_zs_raw.append(p_z)
        
        self.acceleration_xs[:] = self.acceleration_xs[-self.data_limit:]
        self.acceleration_ys[:] = self.acceleration_ys[-self.data_limit:]
        self.acceleration_zs[:] = self.acceleration_zs[-self.data_limit:]
        self.time_data[:] = self.time_data[-self.data_limit:]
        
        self.velocity_xs[:] = self.velocity_xs[-self.data_limit:]
        self.velocity_ys[:] = self.velocity_ys[-self.data_limit:]
        self.velocity_zs[:] = self.velocity_zs[-self.data_limit:]
        
        self.position_xs_raw[:] = self.position_xs_raw[-self.data_limit:]
        self.position_ys_raw[:] = self.position_ys_raw[-self.data_limit:]
        self.position_zs_raw[:] = self.position_zs_raw[-self.data_limit:]
        

        self.line_acceleration_x.set_data(self.time_data, self.acceleration_xs)
        self.line_velocity_x.set_data(self.time_data, self.velocity_xs)
        self.line_position_x_raw.set_data(self.time_data, self.position_xs_raw)
        
        self.line_acceleration_y.set_data(self.time_data, self.acceleration_ys)
        self.line_velocity_y.set_data(self.time_data, self.velocity_ys)
        self.line_position_y_raw.set_data(self.time_data, self.position_ys_raw)
        
        self.line_acceleration_z.set_data(self.time_data, self.acceleration_zs)
        self.line_velocity_z.set_data(self.time_data, self.velocity_zs)
        self.line_position_z_raw.set_data(self.time_data, self.position_zs_raw)

        self.ax.set_ylim(-5000, 5000)

        self.ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        return self.line_acceleration_x, \
            self.line_velocity_x, \
            self.line_position_x_raw, \
            self.line_acceleration_y, \
            self.line_velocity_y, \
            self.line_position_y_raw, \
            self.line_acceleration_z, \
            self.line_velocity_z, \
            self.line_position_z_raw
