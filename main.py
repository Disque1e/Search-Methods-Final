import tkinter as tk
from tkinter import messagebox, simpledialog

import StraightLineDistance
import Database
import UniformCost
import DepthLimited
import GreedySearch
import AStar
import Map


class CityPathSearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("City Path Search")
        self.geometry("300x200")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create "Start" label and input
        self.start_label = tk.Label(self, text="Start:")
        self.start_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.start_input = tk.Entry(self)
        self.start_input.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Create "Destination" label and input
        self.destination_label = tk.Label(self, text="Destination:")
        self.destination_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.destination_input = tk.Entry(self)
        self.destination_input.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Create Algorithm selection
        self.algorithm_label = tk.Label(self, text="Select Algorithm:")
        self.algorithm_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.algorithm_var = tk.StringVar(self)
        self.algorithm_var.set("Uniform Cost Search")  # Default option

        self.algorithm_options = ["Uniform Cost Search", "Depth Limited Search", "Greedy Search", "A*", "Straight Line Distance"]
        self.algorithm_menu = tk.OptionMenu(self, self.algorithm_var, *self.algorithm_options)
        self.algorithm_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Create "Select" button
        select_btn = tk.Button(self, text="Select", command=self.select_path)
        select_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Monitor changes to the algorithm selection
        self.algorithm_var.trace("w", self.on_algorithm_change)

        # Initialize visibility based on default algorithm
        self.on_algorithm_change()

    def hide_destination_widgets(self):
        self.destination_label.grid_remove()
        self.destination_input.grid_remove()

    def show_destination_widgets(self):
        self.destination_label.grid()
        self.destination_input.grid()

    def on_algorithm_change(self, *args):
        algorithm = self.algorithm_var.get()
        if algorithm in ["Greedy Search", "A*"]:
            self.hide_destination_widgets()
        else:
            self.show_destination_widgets()

    def select_path(self):
        start = self.start_input.get()
        if start not in Database.connections:
            messagebox.showerror("Invalid Starting City", f"Starting city '{start}' is invalid. Please select another "
                                                          f"city.")
            return

        algorithm = self.algorithm_var.get()
        if algorithm == "Greedy Search" or algorithm == "A*":
            if start == "Faro":
                messagebox.showerror("Invalid Starting City", f"Starting city shouldn't be 'Faro' for {algorithm}.")
                return

        # Handle Depth Limited Search with Depth Limit
        if algorithm == "Depth Limited Search":
            depth_limit = self.ask_depth_limit()
            if depth_limit is None:
                return  # User cancelled or entered invalid depth limit
            destination = self.destination_input.get()
            if destination not in Database.connections:
                messagebox.showerror("Invalid Destination City", f"Destination city '{destination}' is invalid. Please "
                                                                 f"select another city.")
                return
            result = DepthLimited.depth_limited_search(start, destination, Database.connections, depth_limit)
        elif algorithm == "Straight Line Distance":
            self.calculate_straight_line_distance(start)
        else:
            destination = self.destination_input.get() if algorithm != "Greedy Search" and algorithm != "A*" else "Faro"
            if destination not in Database.connections:
                messagebox.showerror("Invalid Destination City", f"Destination city '{destination}' is invalid. Please "
                                                                 f"select another city.")
                return

            if algorithm == "Uniform Cost Search":
                result = UniformCost.uniform_cost_search(start, destination, Database.connections)
            elif algorithm == "Greedy Search":
                result = GreedySearch.greedy_search(start, destination, Database.connections)
            elif algorithm == "A*":
                result = AStar.AStar_search(start, destination, Database.connections)
            else:
                messagebox.showerror("Invalid Algorithm", "Please select a valid algorithm.")
                return

        if result:
            path_cost, path_steps, final_city, full_path = result
            chosen_path = ' -> '.join(path_steps)
            print(f"Chosen Path: {chosen_path}, Distance: {path_cost}km")
            self.open_map_window(result, start, destination)

    def ask_depth_limit(self):
        try:
            depth_limit = simpledialog.askinteger("Depth Limit", "Please enter the depth limit:")
            if depth_limit is None or depth_limit <= 0:
                messagebox.showerror("Invalid Depth Limit", "Depth limit must be a positive integer.")
                return None
            return depth_limit
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the depth limit.")
            return None

    def calculate_straight_line_distance(self, start):
        destination = self.destination_input.get()
        if destination not in Database.coordinates:
            messagebox.showerror("Invalid Destination City", f"Destination city '{destination}' is invalid. Please "
                                                             f"select another city.")
            return None
        distance_km = StraightLineDistance.calculate_distance_between_cities(start, destination, Database.coordinates)
        if distance_km is not None:
            formatted_distance = "{:.2f}".format(distance_km)
            messagebox.showinfo("Straight Line Distance",
                                f"Straight line distance between {start} and {destination}: {formatted_distance} km")
            return None
        else:
            messagebox.showerror("Error", "Failed to calculate straight line distance.")
            return None

    def open_map_window(self, result, start, destination):
        path_cost, path_steps, final_city, full_path = result
        map_window = tk.Toplevel(self)
        Map.MapWindow(map_window, path_steps, path_steps, full_path, start, destination)


if __name__ == '__main__':
    app = CityPathSearchApp()
    app.mainloop()
