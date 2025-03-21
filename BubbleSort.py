import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BubbleSort:
    # Helper function for Bubble Sort
    def compare_and_swap(self, arr, j):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return True, arr
        return False, arr

    def perform_bubble_sort(self, arr):
        steps = []
        n = len(arr)
        steps.append(("Step 1: Start from the first element of the array.", "blue"))
        steps.append(("", "black"))  # Blank line for spacing

        for i in range(n - 1):
            steps.append((f"Iteration {i + 1}:", "green"))
            steps.append(("", "black"))  # Blank line for spacing
            for j in range(n - i - 1):
                steps.append((f"  Comparing elements at indices {j} and {j + 1}: {arr[j]} and {arr[j + 1]}", "black"))
                swapped, arr = self.compare_and_swap(arr, j)
                if swapped:
                    steps.append((f"    Swapped {arr[j + 1]} and {arr[j]}. New array: {arr}", "black"))
                else:
                    steps.append(("    No swap needed.", "black"))
                steps.append(("", "black"))  # Blank line for spacing
        steps.append((f"Final sorted array: {arr}", "green"))
        return arr, steps

    # Visualization for Bubble Sort
    def bubble_sort_visual(self, root, arr):
        visualization_window = tk.Toplevel(root)
        visualization_window.title("Bubble Sort Visualization")
        visualization_window.geometry("800x600")

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()
        bar_rects = ax.bar(range(len(arr)), arr, color='skyblue')
        ax.set_xlim(0, len(arr))
        ax.set_ylim(0, int(1.1 * max(arr)))

        # Add values on top of the bars
        for rect, val in zip(bar_rects, arr):
            height = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                height,
                f"{val}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        # Create a canvas to embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=visualization_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Control variables
        paused = False
        speed = 1000  # Default speed in milliseconds
        step = 0
        i = 0
        j = 0
        swapped = True

        # Create control buttons
        control_frame = tk.Frame(visualization_window)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        # Play/Pause Button
        play_pause_button = tk.Button(
            control_frame, text="Pause", command=lambda: toggle_pause()
        )
        play_pause_button.pack(side=tk.LEFT, padx=5)

        # Speed Control
        speed_label = tk.Label(control_frame, text="Speed (ms):")
        speed_label.pack(side=tk.LEFT, padx=5)
        speed_scale = tk.Scale(
            control_frame, from_=10, to=500, orient=tk.HORIZONTAL, command=lambda s: set_speed(int(s))
        )
        speed_scale.set(speed)
        speed_scale.pack(side=tk.LEFT, padx=5)

        # Step Forward/Backward
        step_back_button = tk.Button(
            control_frame, text="Step Back", command=lambda: step_back()
        )
        step_back_button.pack(side=tk.LEFT, padx=5)
        step_forward_button = tk.Button(
            control_frame, text="Step Forward", command=lambda: step_forward()
        )
        step_forward_button.pack(side=tk.LEFT, padx=5)

        # Bubble Sort Generator
        def bubble_sort():
            nonlocal i, j, swapped
            while swapped:
                swapped = False
                for j in range(len(arr) - i - 1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        swapped = True
                        yield arr
                i += 1
                yield arr

        # Animation update function
        def update_fig(arr):
            ax.clear()
            bar_rects = ax.bar(range(len(arr)), arr, color='skyblue')
            ax.set_xlim(0, len(arr))
            ax.set_ylim(0, int(1.1 * max(arr)))

            # Add values on top of the bars
            for rect, val in zip(bar_rects, arr):
                height = rect.get_height()
                ax.text(
                    rect.get_x() + rect.get_width() / 2,
                    height,
                    f"{val}",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                )

            # Highlight the compared elements
            for rect in bar_rects:
                rect.set_color("skyblue")
            if j < len(arr) - i - 1:
                bar_rects[j].set_color("red")
                bar_rects[j + 1].set_color("red")

            # Highlight sorted elements
            for k in range(len(arr) - i, len(arr)):
                bar_rects[k].set_color("green")

            canvas.draw()

        # Control functions
        def toggle_pause():
            nonlocal paused
            paused = not paused
            play_pause_button.config(text="Resume" if paused else "Pause")

        def set_speed(new_speed):
            nonlocal speed
            speed = new_speed
            ani.event_source.interval = speed

        def step_forward():
            nonlocal step
            if paused:
                step += 1
                update_fig(next(bubble_sort_gen))

        def step_back():
            nonlocal step
            if paused and step > 0:
                step -= 1
                update_fig(next(bubble_sort_gen))

        # Start the animation
        bubble_sort_gen = bubble_sort()
        ani = animation.FuncAnimation(
            fig,
            update_fig,
            frames=bubble_sort_gen,
            interval=speed,
            repeat=False,
            cache_frame_data=False,
        )


# Main application
class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.geometry("400x200")

        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)

        # Label and Entry for array input
        tk.Label(input_frame, text="Enter array (comma-separated):").pack(side=tk.LEFT)
        self.array_entry = tk.Entry(input_frame, width=30)
        self.array_entry.pack(side=tk.LEFT, padx=10)

        # Button to start visualization
        tk.Button(self.root, text="Start Bubble Sort", command=self.start_bubble_sort).pack(pady=10)

    def start_bubble_sort(self):
        try:
            # Get the array from the entry widget
            arr = list(map(int, self.array_entry.get().split(',')))
            # Instantiate BubbleSort and start visualization
            bubble_sort = BubbleSort()
            bubble_sort.bubble_sort_visual(self.root, arr)
        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter a valid comma-separated list of integers.")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()