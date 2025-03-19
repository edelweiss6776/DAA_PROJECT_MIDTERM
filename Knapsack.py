import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time


class Knapsack(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Knapsack Visualizer")
        self.geometry("900x600")
        self.configure(bg="white")

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Knapsack Visualizer", font=("Arial", 24, "bold"), fg="gold", bg="white")
        title_label.pack(pady=10)

        # Input Fields
        input_frame = tk.Frame(self, bg="white")
        input_frame.pack()

        tk.Label(input_frame, text="Weights:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5)
        self.weights_entry = tk.Entry(input_frame, width=15)
        self.weights_entry.grid(row=0, column=1, padx=5)
        self.weights_entry.insert(0, "1,2,3")

        tk.Label(input_frame, text="Values:", font=("Arial", 12), bg="white").grid(row=0, column=2, padx=5)
        self.values_entry = tk.Entry(input_frame, width=15)
        self.values_entry.grid(row=0, column=3, padx=5)
        self.values_entry.insert(0, "10,15,40")

        tk.Label(input_frame, text="Max Weight:", font=("Arial", 12), bg="white").grid(row=0, column=4, padx=5)
        self.max_weight_entry = tk.Entry(input_frame, width=5)
        self.max_weight_entry.grid(row=0, column=5, padx=5)
        self.max_weight_entry.insert(0, "6")

        tk.Label(input_frame, text="Milliseconds per Tick:", font=("Arial", 12), bg="white").grid(row=0, column=6,
                                                                                                  padx=5)
        self.tick_speed_entry = tk.Entry(input_frame, width=5)
        self.tick_speed_entry.grid(row=0, column=7, padx=5)
        self.tick_speed_entry.insert(0, "100")

        update_button = tk.Button(self, text="UPDATE", command=self.start_knapsack, font=("Arial", 12, "bold"),
                                  bg="blue", fg="white")
        update_button.pack(pady=10)

        # Table Display
        self.table_frame = tk.Frame(self, bg="white")
        self.table_frame.pack()

    def start_knapsack(self):
        # Get user input
        try:
            weights = list(map(int, self.weights_entry.get().split(',')))
            values = list(map(int, self.values_entry.get().split(',')))
            max_weight = int(self.max_weight_entry.get())
            tick_speed = int(self.tick_speed_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers separated by commas.")
            return

        if len(weights) != len(values):
            messagebox.showerror("Input Error", "Weights and Values must have the same number of elements.")
            return

        # Clear the previous table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Knapsack DP Table
        n = len(weights)
        dp = np.zeros((n + 1, max_weight + 1), dtype=int)

        # Table Headers
        tk.Label(self.table_frame, text="Weights", font=("Arial", 12, "bold"), bg="lightgray").grid(row=0, column=0)
        tk.Label(self.table_frame, text="Values", font=("Arial", 12, "bold"), bg="lightgray").grid(row=1, column=0)

        for j in range(max_weight + 1):
            tk.Label(self.table_frame, text=str(j), font=("Arial", 12, "bold"), bg="lightgray").grid(row=2,
                                                                                                     column=j + 1)

        # Display Weights and Values
        for i in range(n):
            tk.Label(self.table_frame, text=str(weights[i]), font=("Arial", 12), bg="white").grid(row=0, column=i + 1)
            tk.Label(self.table_frame, text=str(values[i]), font=("Arial", 12), bg="white").grid(row=1, column=i + 1)

        # Table Cells (DP Grid)
        dp_labels = [[None for _ in range(max_weight + 1)] for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(max_weight + 1):
                label = tk.Label(self.table_frame, text="0", font=("Arial", 12), width=6, height=2, relief="ridge",
                                 bg="white")
                label.grid(row=i + 2, column=j + 1)
                dp_labels[i][j] = label

        self.update_idletasks()

        # Solve the Knapsack Problem with Visualization
        for i in range(1, n + 1):
            for j in range(max_weight + 1):
                if weights[i - 1] <= j:
                    dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weights[i - 1]] + values[i - 1])
                    dp_labels[i][j].config(bg="lightgreen")  # Latest Maximum Value
                else:
                    dp[i][j] = dp[i - 1][j]
                    dp_labels[i][j].config(bg="lightblue")  # Previous Best Answer

                dp_labels[i][j].config(text=str(dp[i][j]))

                self.update()
                time.sleep(tick_speed / 1000)

        # Highlight the Final Answer
        dp_labels[n][max_weight].config(bg="green")

        messagebox.showinfo("Knapsack Solved!", f"Maximum value: {dp[n][max_weight]}")


if __name__ == "__main__":
    app = Knapsack()
    app.mainloop()
