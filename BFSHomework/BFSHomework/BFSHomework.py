# tsp_solver.py

from collections import deque
import sys

def load_city_distances(city_names, distance_matrix):
    """
    Load the distances between cities into a dictionary.
    """
    distances = {}
    for i, origin in enumerate(city_names):
        for j, destination in enumerate(city_names):
            distances[(origin, destination)] = distance_matrix[i][j]
    return distances

def bfs_tsp(cities, distances):
    """
    Solves the TSP using BFS to minimize the longest single jump between consecutive cities.
    """
    queue = deque([(cities[0], [cities[0]], 0)])  # (current city, path taken, max jump in path)
    best_path = None
    min_max_jump = sys.maxsize

    while queue:
        current_city, path, max_jump = queue.popleft()

        # If all cities are visited and path is valid
        if len(path) == len(cities) + 1 and path[-1] == path[0]:
            if max_jump < min_max_jump:
                best_path = path
                min_max_jump = max_jump
            continue  # Prevent further expansion of a complete path

        # Explore next moves
        for next_city in cities:
            # Only add unvisited cities or return to start if all cities are visited
            if next_city not in path or (next_city == path[0] and len(set(path)) == len(cities)):
                new_path = path + [next_city]
                new_jump = distances[(current_city, next_city)]
                new_max_jump = max(max_jump, new_jump)
                if not (next_city == path[0] and len(set(path)) < len(cities)):  # Prevent looping back to start too early
                    queue.append((next_city, new_path, new_max_jump))

    return best_path, min_max_jump

if __name__ == "__main__":
    # Example usage
    city_names = ["A", "B", "C", "D"]
    distance_matrix = [
        [0, 1, 4, 5],
        [1, 0, 2, 6],
        [4, 2, 0, 3],
        [5, 6, 3, 0]
    ]

    distances = load_city_distances(city_names, distance_matrix)
    best_path, min_max_jump = bfs_tsp(city_names, distances)
    print("Best path:", best_path)
    print("Minimum longest jump:", min_max_jump)