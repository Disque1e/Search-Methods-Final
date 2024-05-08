import heapq


class UniformCostWindow:
    def __init__(self, master, menu):
        self.master = master
        self.menu = menu


def uniform_cost_search(start_city, destination_city, connections):
    # Check if the cities inserted by the user is a valid city
    if start_city not in connections:
        raise ValueError(f"Starting city '{start_city}' is not in the connections dictionary.")

    if destination_city not in connections:
        raise ValueError(f"Destination city '{destination_city}' is not in the connections dictionary.")

    search_queue = [(0, start_city, [])]
    full_path = []
    visited = set()
    iteration = 0

    print(f"Idx   | Current Path")
    print('─' * 6 + '┼' + '─' * 150)

    while search_queue:
        current_cost, current_city, current_path = heapq.heappop(search_queue)
        full_path.append(current_city)

        if current_city == destination_city:
            return current_cost, current_path + [current_city], current_city, full_path

        for next_city, cost in connections[current_city].items():
            if next_city not in visited:
                next_city_cost = current_cost + cost
                next_path = current_path + [current_city]
                heapq.heappush(search_queue, (next_city_cost, next_city, next_path))

        iteration += 1

        print(f"{iteration:<4}  | {current_city} -> ", end='')
        for cost, city, path in search_queue:
            if city not in visited:
                print(f"{city}({cost}), ", end='')

        print()

        visited.add(current_city)

    return None
