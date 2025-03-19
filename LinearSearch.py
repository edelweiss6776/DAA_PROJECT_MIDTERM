import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LinearSearch:
    def __init__(self, root, arr, target):
        self.root = root
        self.arr = arr
        self.target = target
        self.n = len(arr)
        self.index = 0
        self.paused = False
        self.step = 0
        self.speed = 500  # Default speed in milliseconds

        # Create a figure and axis for the plot
        self.fig, self.ax = plt.subplots()
        self.bar_rects = self.ax.bar(range(self.n), self.arr, color='skyblue')
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, int(1.1 * max(self.arr)))

        # Add values on top of the bars
        for rect, val in zip(self.bar_rects, self.arr):
            height = rect.get_height()
            self.ax.text(
                rect.get_x() + rect.get_width() / 2,
                height,
                f"{val}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        # Create a canvas to embed the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create control buttons
        self.create_controls()

        # Start the animation
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update_fig,
            frames=self.linear_search(),
            interval=self.speed,
            repeat=False,
            cache_frame_data=False,
        )

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        # Play/Pause Button
        self.play_pause_button = tk.Button(
            control_frame, text="Pause", command=self.toggle_pause
        )
        self.play_pause_button.pack(side=tk.LEFT, padx=5)

        # Speed Control
        speed_label = tk.Label(control_frame, text="Speed (ms):")
        speed_label.pack(side=tk.LEFT, padx=5)
        self.speed_scale = tk.Scale(
            control_frame, from_=10, to=1000, orient=tk.HORIZONTAL, command=self.set_speed
        )
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side=tk.LEFT, padx=5)

        # Step Forward/Backward
        step_back_button = tk.Button(
            control_frame, text="Step Back", command=self.step_back
        )
        step_back_button.pack(side=tk.LEFT, padx=5)
        step_forward_button = tk.Button(
            control_frame, text="Step Forward", command=self.step_forward
        )
        step_forward_button.pack(side=tk.LEFT, padx=5)

    def toggle_pause(self):
        self.paused = not self.paused
        self.play_pause_button.config(text="Resume" if self.paused else "Pause")

    def set_speed(self, speed):
        self.speed = int(speed)
        self.ani.event_source.interval = self.speed

    def step_forward(self):
        if self.paused and self.step < self.n:
            self.step += 1
            self.update_fig(next(self.linear_search()))

    def step_back(self):
        if self.paused and self.step > 0:
            self.step -= 1
            self.update_fig(next(self.linear_search()))

    def linear_search(self):
        for self.index in range(self.n):
            yield self.index, self.arr[self.index] == self.target

    def update_fig(self, data):
        index, found = data
        self.ax.clear()
        self.bar_rects = self.ax.bar(range(self.n), self.arr, color='skyblue')
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, int(1.1 * max(self.arr)))

        # Add values on top of the bars
        for rect, val in zip(self.bar_rects, self.arr):
            height = rect.get_height()
            self.ax.text(
                rect.get_x() + rect.get_width() / 2,
                height,
                f"{val}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        # Highlight the current element being checked
        for rect in self.bar_rects:
            rect.set_color("skyblue")
        self.bar_rects[index].set_color("red")

        # Highlight the target if found
        if found:
            self.bar_rects[index].set_color("green")

        self.canvas.draw()


# Example usage:
if __name__ == "__main__":
    arr = [5, 3, 8, 6, 7, 2]
    target = 7
    root = tk.Tk()
    app = LinearSearch(root, arr, target)
    root.mainloop()