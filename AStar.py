import heapq
import Database


class AStarWindow:
    def __init__(self, master, menu):
        self.master = master
        self.menu = menu


def AStar_search(start_city, destination_city, connections):
    # Check if the cities inserted by the user are valid cities
    if start_city not in connections:
        raise ValueError(f"Starting city '{start_city}' is not in the connections dictionary.")

    if destination_city not in connections:
        raise ValueError(f"Destination city '{destination_city}' is not in the connections dictionary.")

    # Check if direct paths are available for start_city and destination_city
    if start_city not in Database.direct_path or destination_city not in Database.direct_path[start_city]:
        raise ValueError(f"Direct path from '{start_city}' to '{destination_city}' is not defined.")

    visited = set()
    start_h = Database.direct_path[start_city][destination_city]
    search_queue = [(start_h, start_city, 0, [])]
    full_path = []

    while search_queue:
        f, curr_city, g, curr_path = heapq.heappop(search_queue)
        full_path.append(curr_city)

        print(f'In {curr_city} with cost of {g}')
        print(f'Current Path: {curr_path + [curr_city]}')
        print('-' * 150)

        if curr_city == destination_city:
            return g, curr_path + [curr_city], curr_city, full_path

        visited.add(curr_city)

        for next_city, cost in connections[curr_city].items():
            if next_city not in visited:
                if next_city in Database.direct_path and destination_city in Database.direct_path[next_city]:
                    h = Database.direct_path[next_city][destination_city]
                else:
                    h = 0

                next_g = g + cost
                f = h + next_g
                next_path = curr_path + [curr_city]
                heapq.heappush(search_queue, (f, next_city, next_g, next_path))

    return None
