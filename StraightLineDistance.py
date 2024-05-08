from geopy.distance import distance


# Function that calculates the distance between two cities in a straight line
def calculate_distance_between_cities(first_city, second_city, coordinates):
    if first_city in coordinates and second_city in coordinates:
        first_city_coordinates = coordinates[first_city]
        second_city_coordinates = coordinates[second_city]
        dist = distance(first_city_coordinates, second_city_coordinates).km
        return dist
    else:
        return None
