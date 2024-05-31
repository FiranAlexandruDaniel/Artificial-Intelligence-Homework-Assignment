# file: tsp_a_star_search.py

import heapq
from sys import maxsize

class TSPSolver:
    """
    Class to solve the Traveling Salesman Problem using A* Search.
    This implementation focuses on minimizing the longest jump between consecutive cities.
    """

    def __init__(self, cities, distance_matrix):
        """
        Initialize the TSP Solver with city names and a distance matrix.

        Args:
        cities (list of str): Names of the cities.
        distance_matrix (list of list of int): Matrix of distances between cities.
        """
        self.cities = cities
        self.distances = self.load_city_distances(cities, distance_matrix)

    def load_city_distances(self, cities, distance_matrix):
        """
        Load the distances between cities into a dictionary for quick access.

        Args:
        cities (list of str): List of city names.
        distance_matrix (list of list of int): 2D list representing distances.

        Returns:
        dict: Dictionary with city pair tuples as keys and distances as values.
        """
        distances = {}
        for i, origin in enumerate(cities):
            for j, destination in enumerate(cities):
                distances[(origin, destination)] = distance_matrix[i][j]
        return distances

    def heuristic(self, remaining_cities, current_city):
        """
        Calculate a heuristic for the A* search. Here we use the minimum distance to any remaining city.

        Args:
        remaining_cities (list of str): Cities that have not been visited yet.
        current_city (str): The current city in the path.

        Returns:
        int: Estimated minimum cost to complete the tour.
        """
        min_dist = min([self.distances[(current_city, city)] for city in remaining_cities if city != current_city], default=0)
        return min_dist

    def solve(self):
        """
        Solve the TSP using the A* search algorithm.

        Returns:
        tuple: The optimal path and its maximum jump distance.
        """
        # Priority queue for the A* search: stores tuples of (cost, path, max_jump)
        open_set = []
        heapq.heappush(open_set, (0, [self.cities[0]], 0))
        best_path = None
        min_max_jump = maxsize

        while open_set:
            cost, path, max_jump = heapq.heappop(open_set)
            current_city = path[-1]

            if len(path) == len(self.cities) + 1 and path[-1] == path[0]:
                if max_jump < min_max_jump:
                    best_path = path
                    min_max_jump = max_jump
                continue

            remaining_cities = [city for city in self.cities if city not in path or (city == path[0] and len(set(path)) == len(self.cities))]
            for next_city in remaining_cities:
                new_path = path + [next_city]
                new_jump = self.distances[(current_city, next_city)]
                new_max_jump = max(max_jump, new_jump)
                estimated_cost = cost + new_jump + self.heuristic(remaining_cities, next_city)
                heapq.heappush(open_set, (estimated_cost, new_path, new_max_jump))

        return best_path, min_max_jump

# Example usage
if __name__ == "__main__":
    cities = ["A", "B", "C", "D"]
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 40],
        [15, 35, 0, 30],
        [20, 40, 30, 0]
    ]
    solver = TSPSolver(cities, distance_matrix)
    best_path, min_max_jump = solver.solve()
    print("Best path:", best_path)
    print("Minimum longest jump:", min_max_jump)
