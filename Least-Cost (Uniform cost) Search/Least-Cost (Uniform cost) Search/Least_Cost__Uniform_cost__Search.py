# file: tsp_uniform_cost_search.py

from heapq import heappush, heappop
import sys

class TSPSolver:
    """
    A class to solve the Traveling Salesman Problem using Uniform Cost Search.
    This solver minimizes the longest single jump between consecutive cities.
    """

    def __init__(self, cities, distance_matrix):
        """
        Initializes the TSP Solver.

        Args:
        cities (list of str): List of city names.
        distance_matrix (list of list of int): Square matrix of distances.
        """
        self.cities = cities
        self.distances = self._load_city_distances(cities, distance_matrix)

    def _load_city_distances(self, cities, distance_matrix):
        """
        Loads the distances between cities into a dictionary.

        Args:
        cities (list of str): List of city names.
        distance_matrix (list of list of int): Square matrix representing the distances.

        Returns:
        dict: A dictionary with city pair tuples as keys and distances as values.
        """
        distances = {}
        for i, origin in enumerate(cities):
            for j, destination in enumerate(cities):
                distances[(origin, destination)] = distance_matrix[i][j]
        return distances

    def solve(self):
        """
        Solves the TSP using Uniform Cost Search.

        Returns:
        tuple: Best path found and its maximum jump distance.
        """
        # Priority queue: stores tuples of (max jump in path, current path)
        frontier = []
        heappush(frontier, (0, [self.cities[0]]))

        best_path = None
        min_max_jump = sys.maxsize

        while frontier:
            max_jump, path = heappop(frontier)
            current_city = path[-1]

            # Check if all cities have been visited and path returns to start
            if len(path) > 1 and path[-1] == self.cities[0]:
                if len(set(path[:-1])) == len(self.cities):  # Ensure all cities are visited
                    if max_jump < min_max_jump:
                        best_path = path
                        min_max_jump = max_jump
                    continue

            # Explore next moves
            for next_city in self.cities:
                if next_city not in path or (next_city == self.cities[0] and len(set(path)) == len(self.cities)):
                    new_path = path + [next_city]
                    new_jump = self.distances[(current_city, next_city)]
                    new_max_jump = max(max_jump, new_jump)
                    if not (next_city == self.cities[0] and len(set(path)) < len(self.cities)):  # Check path validity
                        heappush(frontier, (new_max_jump, new_path))

        return best_path, min_max_jump

# Example usage
if __name__ == "__main__":
    cities = ["A", "B", "C", "D"]
    distance_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    solver = TSPSolver(cities, distance_matrix)
    best_path, min_max_jump = solver.solve()
    print("Best path:", best_path)
    print("Minimum longest jump:", min_max_jump)
