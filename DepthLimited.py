import Database
import heapq


class DepthLimitedWindow:
    def __init__(self, master, menu):
        self.master = master
        self.menu = menu


def depth_limited_search(start_city, destination_city, connections, depth_limit):
    # Check if the cities inserted by the user is a valid city
    if start_city not in connections:
        raise ValueError(f"Starting city '{start_city}' is not in the connections dictionary.")

    if destination_city not in connections:
        raise ValueError(f"Destination city '{destination_city}' is not in the connections dictionary.")

    search_stack = [(0, start_city, [])]
    full_path = []
    visited = set()
    iteration = 0

    print(f"Iter  | Current Path")
    print('─' * 6 + '┼' + '─' * 150)

    while search_stack:
        current_cost, current_city, current_path = search_stack.pop()
        full_path.append(current_city)

        if current_city == destination_city:
            return current_cost, current_path + [current_city], current_city, full_path

        # Limits the expansion just if the actual depth is smaller than the limit
        if len(current_path) < depth_limit:
            # Expand the current node (city) in DLS order (LIFO)
            for next_city, cost in connections[current_city].items():
                if next_city not in visited:
                    next_city_cost = current_cost + cost
                    next_path = current_path + [current_city]
                    search_stack.append((next_city_cost, next_city, next_path))

        iteration += 1

        # Print current state of the search
        print(f"{iteration:<5} | {' -> '.join(current_path + [current_city])}")

        visited.add(current_city)

    return None
