import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt

from mytypes import Vec3d

class Graph:
    def __init__(self, get_acceleration):
        self.get_acceleration = get_acceleration
        
        self.time_start = dt.datetime.now().timestamp()
        self.time_data = []
        self.x_data = []
        self.y_data = []
        self.z_data = []

        self.data_limit = 50

        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        self.line_x, = self.ax.plot(self.time_data, self.x_data, label="Acceleration X", color="blue")
        self.line_y, = self.ax.plot(self.time_data, self.y_data, label="Acceleration Y", color="green")
        self.line_z, = self.ax.plot(self.time_data, self.z_data, label="Acceleration Z", color="yellow")

        self.ax.set_title("Acceleration data")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Acceleration")
        self.ax.legend()
        self.ax.grid(True)

        self.ani = animation.FuncAnimation(self.fig, self.add_data, interval=1000, blit=False)


    def add_data(self, i):
        # Get acceleration
        acceleration = self.get_acceleration()

        # Get the current time and set it on the time_data
        current_time = dt.datetime.now().timestamp()
        self.time_data.append(current_time-self.time_start)
        
        # Append acceleration datas
        self.x_data.append(acceleration.x)
        self.y_data.append(acceleration.y)
        self.z_data.append(acceleration.z)

        # Chop off everything older than the data limit
        self.time_data[:] = self.time_data[-self.data_limit:] 
        self.x_data[:] = self.x_data[-self.data_limit:] 
        self.y_data[:] = self.y_data[-self.data_limit:] 
        self.z_data[:] = self.z_data[-self.data_limit:] 

        # Update the line
        self.line_x.set_data(self.time_data, self.x_data)
        self.line_y.set_data(self.time_data, self.y_data)
        self.line_z.set_data(self.time_data, self.z_data)
        
        # Re-scale the axes
        self.ax.set_xlim(self.time_data[0], self.time_data[-1])

        # The y-axis needs to be re-scaled to fit the min/max of visible data
        all_visible_data = self.x_data + self.y_data + self.z_data
        if all_visible_data:
            # min_val = min(all_visible_data)
            # max_val = max(all_visible_data)

            self.ax.set_ylim(-50000, 50000)

        self.ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        # print(f"{self.x_data}")
        # print(f"{self.y_data}")

        return self.line_x, self.line_y, self.line_z
    
    def show(self):
        plt.show()
    
