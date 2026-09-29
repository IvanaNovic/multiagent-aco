import math
class Graph:
    def __init__(self, cities):
        """ cities: tuple lista (id, x, y) """
        self.cities = cities
        self.num_cities = len(cities)
        self.distances = self._compute_distances()

    def _compute_distances(self):
        distances = {}
        for i, (id_i, x_i, y_i) in enumerate(self.cities):
            for j, (id_j, x_j, y_j) in enumerate(self.cities):
                if i != j:
                    dx = x_i - x_j
                    dy = y_i - y_j
                    distances[(id_i, id_j)] = math.sqrt(dx ** 2 + dy ** 2)
        return distances

    def distance(self, city_a, city_b):
        return self.distances[(city_a, city_b)]

    @classmethod
    def from_file(cls, filepath):
        cities = []
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                city_id, x, y = int(parts[0]), float(parts[1]), float(parts[2])
                cities.append((city_id, x, y))
        return cls(cities)