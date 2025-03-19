import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from BubbleSort import BubbleSort
from LinearSearch import LinearSearch
from Knapsack import Knapsack  # Import the Knapsack class


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ma'am L's Learning App for DAA")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        self.algorithms = BubbleSort()

        # Custom Fonts
        self.title_font = ("Helvetica", 24, "bold")
        self.subtitle_font = ("Helvetica", 14)
        self.button_font = ("Helvetica", 12, "bold")
        self.text_font = ("Helvetica", 12)

        # Title Label
        self.create_title_label()

        # Subtitle Label
        self.create_subtitle_label()

        # Buttons for Algorithms
        self.create_algorithm_buttons()

        # Exit Button
        self.create_exit_button()

    def create_title_label(self):
        title_label = tk.Label(
            self.root,
            text="Ma'am L's Learning App for DAA",
            font=self.title_font,
            bg="#f5f5f5",
            fg="#333333"
        )
        title_label.pack(pady=20)

    def create_subtitle_label(self):
        subtitle_label = tk.Label(
            self.root,
            text="Learn and visualize 4 important algorithms with detailed steps!",
            font=self.subtitle_font,
            bg="#f5f5f5",
            fg="#555555"
        )
        subtitle_label.pack(pady=10)

    def create_algorithm_buttons(self):
        button_frame = tk.Frame(self.root, bg="#f5f5f5")
        button_frame.pack(pady=20)

        self.bubble_sort_button = tk.Button(
            button_frame,
            text="Bubble Sort",
            font=self.button_font,
            bg="#F44336",
            fg="white",
            padx=20,
            pady=10,
            command=self.teach_bubble_sort
        )
        self.bubble_sort_button.grid(row=0, column=0, padx=10, pady=10)

        self.linear_search_button = tk.Button(
            button_frame,
            text="Linear Search",
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=self.teach_linear_search
        )
        self.linear_search_button.grid(row=0, column=1, padx=10, pady=10)

        self.knapsack_button = tk.Button(
            button_frame,
            text="Knapsack Problem",
            font=self.button_font,
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            command=self.teach_knapsack
        )
        self.knapsack_button.grid(row=0, column=2, padx=10, pady=10)  # Changed column to 2

    def create_exit_button(self):
        exit_button = tk.Button(
            self.root,
            text="Exit",
            font=self.button_font,
            bg="#555555",
            fg="white",
            padx=20,
            pady=10,
            command=self.root.quit
        )
        exit_button.pack(pady=20)

    def teach_bubble_sort(self):
        teach_window = tk.Toplevel(self.root)
        teach_window.title("Learn Bubble Sort")
        teach_window.geometry("900x700")
        teach_window.configure(bg="#f5f5f5")

        # Lecture
        lecture = """
        Bubble Sort:
        ------------
        Bubble Sort is a simple sorting algorithm that repeatedly steps through the list,
        compares adjacent elements, and swaps them if they are in the wrong order.
        The algorithm gets its name because smaller elements "bubble" to the top of the list.

        Steps to Solve Bubble Sort:
        1. Start from the first element of the array.
        2. Compare each pair of adjacent elements.
        3. Swap them if they are in the wrong order.
        4. Repeat the process until no swaps are needed.
        """
        lecture_label = tk.Label(
            teach_window,
            text=lecture,
            justify=tk.LEFT,
            bg="#f5f5f5",
            font=self.text_font
        )
        lecture_label.pack(pady=10)

        # Try It Yourself
        try_it_frame = tk.Frame(teach_window, bg="#f5f5f5")
        try_it_frame.pack(pady=10)

        tk.Label(try_it_frame, text="Try It Yourself:", bg="#f5f5f5", font=("Helvetica", 14, "bold")).grid(row=0, column=0, pady=10)

        tk.Label(try_it_frame, text="Enter the array elements (space-separated):", bg="#f5f5f5", font=self.text_font).grid(row=1, column=0, pady=5)
        arr_entry = tk.Entry(try_it_frame, font=self.text_font)
        arr_entry.grid(row=1, column=1, pady=5)

        def visualize_bubble_sort():
            try:
                arr = list(map(int, arr_entry.get().split()))
                self.algorithms.bubble_sort_visual(teach_window, arr)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        visualize_button = tk.Button(
            try_it_frame,
            text="Visualize Bubble Sort",
            font=self.button_font,
            bg="#F44336",
            fg="white",
            padx=20,
            pady=10,
            command=visualize_bubble_sort
        )
        visualize_button.grid(row=2, column=0, columnspan=2, pady=10)

    def teach_linear_search(self):
        teach_window = tk.Toplevel(self.root)
        teach_window.title("Learn Linear Search")
        teach_window.geometry("900x700")
        teach_window.configure(bg="#f5f5f5")

        # Lecture
        lecture = """
        Linear Search:
        --------------
        Linear Search is a simple algorithm to find the index of a target element in a list.
        It works by checking each element of the list one by one until the target is found.

        Steps to Solve Linear Search:
        1. Start from the first element of the array.
        2. Compare each element with the target.
        3. If the element matches the target, return its index.
        4. If no match is found after traversing the array, return -1.
        """
        lecture_label = tk.Label(
            teach_window,
            text=lecture,
            justify=tk.LEFT,
            bg="#f5f5f5",
            font=self.text_font
        )
        lecture_label.pack(pady=10)

        # Try It Yourself
        try_it_frame = tk.Frame(teach_window, bg="#f5f5f5")
        try_it_frame.pack(pady=10)

        tk.Label(try_it_frame, text="Try It Yourself:", bg="#f5f5f5", font=("Helvetica", 14, "bold")).grid(row=0,
                                                                                                           column=0,
                                                                                                           pady=10)

        tk.Label(try_it_frame, text="Enter the array elements (space-separated):", bg="#f5f5f5",
                 font=self.text_font).grid(row=1, column=0, pady=5)
        arr_entry = tk.Entry(try_it_frame, font=self.text_font)
        arr_entry.grid(row=1, column=1, pady=5)

        tk.Label(try_it_frame, text="Enter the target value:", bg="#f5f5f5", font=self.text_font).grid(row=2, column=0,
                                                                                                       pady=5)
        target_entry = tk.Entry(try_it_frame, font=self.text_font)
        target_entry.grid(row=2, column=1, pady=5)

        def visualize_linear_search():
            try:
                arr = list(map(int, arr_entry.get().split()))
                target = int(target_entry.get())
                LinearSearch(teach_window, arr, target)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        visualize_button = tk.Button(
            try_it_frame,
            text="Visualize Linear Search",
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=visualize_linear_search
        )
        visualize_button.grid(row=3, column=0, columnspan=2, pady=10)




    def teach_knapsack(self):
        """Calls the Knapsack class when the button is clicked."""
        Knapsack()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()