import random
class Colony:
    def __init__(self, colony_id, num_ants, alpha=1.0, beta=3.0, rho=0.5):
        self.colony_id = colony_id
        self.num_ants = num_ants
        self.alpha = alpha      # uticaj feromona
        self.beta = beta        # uticaj heuristike (1/distanca)
        self.rho = rho          # stopa isparavanja feromona
        self.ants = []
        self.best_tour_length = float("inf")
        self.best_tour = None
        self.pheromones = {}

    def init_pheromones(self, graph, initial_value=1.0):
        """Inicijalizacija feromona na svim ivicama grafa na pocetnu vrijednost."""
        for city_a, _, _ in graph.cities:
            for city_b, _, _ in graph.cities:
                if city_a != city_b:
                    self.pheromones[(city_a, city_b)] = initial_value

    def select_next_city(self, current_city, unvisited, graph):
        """Bira sljedeci grad na osnovu feromona (tau) i heuristike (eta = 1/distanca)"""
        weights = []
        for city in unvisited:
            tau = self.pheromones[(current_city, city)]
            eta = 1.0 / graph.distance(current_city, city)
            weight = (tau ** self.alpha) * (eta ** self.beta)
            weights.append(weight)

        total = sum(weights)
        probabilities = [w / total for w in weights]

        return random.choices(unvisited, weights=probabilities, k=1)[0]

    def __repr__(self):
        return (f"Colony({self.colony_id}, ants={self.num_ants}, "
                f"alpha={self.alpha}, beta={self.beta}, rho={self.rho})")