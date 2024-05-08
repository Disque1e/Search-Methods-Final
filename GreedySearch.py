import heapq


class GreedSearchyWindow:
    def __init__(self, master, menu):
        self.master = master
        self.menu = menu


def greedy_search(start_city, destination_city, connections):
    if start_city not in connections:
        raise ValueError(f"Starting city '{start_city}' is not in the connections dictionary.")

    if destination_city not in connections:
        raise ValueError(f"Destination city '{destination_city}' is not in the connections dictionary.")

    search_queue = [(0, start_city, [])]
    visited = set()
    full_path = []

    while search_queue:
        current_cost, current_city, current_path = heapq.heappop(search_queue)
        full_path.append(current_city)

        if current_city in visited:
            continue

        visited.add(current_city)

        print(f'Current city: {current_city}, Current distance: {current_cost}, Current path: {current_path + [current_city]}')

        if current_city == destination_city:
            if len(current_path) > 0:
                total_cost = sum(connections[current_path[i]][current_path[i+1]] for i in range(len(current_path) - 1))
                total_cost += connections[current_path[-1]][current_city]
            else:
                total_cost = 0

            return total_cost, current_path + [current_city], current_city, full_path

        for next_city, cost in connections[current_city].items():
            if next_city not in visited:
                heapq.heappush(search_queue, (cost, next_city, current_path + [current_city]))

    return None
