import tkinter as tk
from tkinter import messagebox
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TSPVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP Solver & Visualizer")

        # Initialize variables
        self.num_cities = tk.IntVar()
        self.graph = []
        self.path = []
        self.min_cost = float("inf")
        self.best_path = []

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        """Create the GUI layout for the app."""
        tk.Label(self.root, text="Enter number of cities:").pack()

        self.city_entry = tk.Entry(self.root, textvariable=self.num_cities)
        self.city_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.get_matrix_input)
        self.submit_button.pack()

    def get_matrix_input(self):
        """Get user input for the distance matrix."""
        try:
            num_cities = int(self.city_entry.get())
            if num_cities <= 1:
                raise ValueError("Number of cities must be greater than 1.")

            self.num_cities = num_cities
            self.matrix_window = tk.Toplevel(self.root)
            self.matrix_window.title("Enter Distance Matrix")

            self.entries = []
            for i in range(num_cities):
                row_entries = []
                for j in range(num_cities):
                    entry = tk.Entry(self.matrix_window, width=5)
                    entry.grid(row=i, column=j)
                    row_entries.append(entry)
                self.entries.append(row_entries)

            submit_matrix_btn = tk.Button(self.matrix_window, text="Solve TSP", command=self.solve_tsp)
            submit_matrix_btn.grid(row=num_cities, columnspan=num_cities)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def solve_tsp(self):
        """Solve the TSP using brute force and visualize the process."""
        try:
            self.graph = []
            for i in range(self.num_cities):
                row = [int(self.entries[i][j].get()) for j in range(self.num_cities)]
                self.graph.append(row)

            self.graph = np.array(self.graph)
            self.tsp_bruteforce()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    def tsp_bruteforce(self):
        """Solve TSP using brute force (all permutations) and visualize step by step."""
        cities = list(range(1, self.num_cities))  # Exclude starting node 0
        min_cost = float("inf")
        best_path = []

        # Create a new window for visualization
        self.visualization_window = tk.Toplevel(self.root)
        self.visualization_window.title("TSP Visualization")

        # Create a canvas for the plot
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_window)
        self.canvas.get_tk_widget().pack()

        for perm in itertools.permutations(cities):
            cost = 0
            current_path = [0] + list(perm) + [0]  # Start & end at 0

            for i in range(len(current_path) - 1):
                cost += self.graph[current_path[i]][current_path[i + 1]]

            self.update_visualization(current_path, cost)

            if cost < min_cost:
                min_cost = cost
                best_path = current_path

            self.visualization_window.update()
            plt.pause(0.5)

        self.min_cost = min_cost
        self.best_path = best_path
        self.path = [(best_path[i], best_path[i + 1]) for i in range(len(best_path) - 1)]

        self.visualize_solution()

    def update_visualization(self, path, cost):
        """Update the visualization dynamically for each path being evaluated."""
        G = nx.Graph()
        for i in range(self.num_cities):
            G.add_node(i)

        for i in range(len(path) - 1):
            G.add_edge(path[i], path[i + 1], weight=self.graph[path[i]][path[i + 1]])

        pos = nx.spring_layout(G, seed=42)
        self.ax.clear()
        self.ax.set_title(f"Checking Path: {path} (Cost: {cost})")

        nx.draw(G, pos, ax=self.ax, with_labels=True, node_color="orange", edge_color="gray", node_size=700, font_size=12)
        labels = {(path[i], path[i + 1]): f"{self.graph[path[i]][path[i + 1]]}" for i in range(len(path) - 1)}
        nx.draw_networkx_edge_labels(G, pos, ax=self.ax, edge_labels=labels)

        self.canvas.draw()

    def visualize_solution(self):
        """Final visualization of the best path found."""
        G = nx.Graph()

        for i in range(self.num_cities):
            G.add_node(i)

        for i, j in self.path:
            G.add_edge(i, j, weight=self.graph[i][j])

        pos = nx.spring_layout(G, seed=42)

        self.ax.clear()
        self.ax.set_title(f"Optimal TSP Path: {self.best_path} (Cost: {self.min_cost})")

        nx.draw(G, pos, ax=self.ax, with_labels=True, node_color="orange", edge_color="red", node_size=700, font_size=12)
        labels = {(i, j): f"{self.graph[i][j]}" for i, j in self.path}
        nx.draw_networkx_edge_labels(G, pos, ax=self.ax, edge_labels=labels)

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPVisualizer(root)
    root.mainloop()