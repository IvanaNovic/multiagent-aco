import random
from src.ant import Ant
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
        self.history= []

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

    def construct_tour(self, start_city, graph):
        """Konstruisanje kompletne ture jednog mrava, pocevsi od start_city"""
        ant = Ant(start_city)
        unvisited = [c for c, _, _ in graph.cities if c != start_city]

        while unvisited:
            next_city = self.select_next_city(ant.current_node, unvisited, graph)
            distance = graph.distance(ant.current_node, next_city)
            ant.visit(next_city, distance)
            unvisited.remove(next_city)

        # zatvaranje ture - povratak na pocetni grad
        closing_distance = graph.distance(ant.current_node, start_city)
        ant.tour_length += closing_distance

        return ant

    def update_pheromones(self, ants, graph):
        """Isparavanje feromona na svim ivicama, zatim depozit na osnovu tura mrava"""
        # isparavanje
        for edge in self.pheromones:
            self.pheromones[edge] *= (1 - self.rho)

        # depozit - svaki mrav ostavlja feromon proporcionalan kvalitetu ture
        for ant in ants:
            deposit = 1.0 / ant.tour_length
            for i in range(len(ant.visited) - 1):
                city_a = ant.visited[i]
                city_b = ant.visited[i + 1]
                self.pheromones[(city_a, city_b)] += deposit
                self.pheromones[(city_b, city_a)] += deposit

            # zatvaranje ture 
            first_city = ant.visited[0]
            last_city = ant.visited[-1]
            self.pheromones[(last_city, first_city)] += deposit
            self.pheromones[(first_city, last_city)] += deposit

            # azuriranje najbolje ture kolonije
            if ant.tour_length < self.best_tour_length:
                self.best_tour_length = ant.tour_length
                self.best_tour = ant.visited

        self.history.append(self.best_tour_length)


    def __repr__(self):
        return (f"Colony({self.colony_id}, ants={self.num_ants}, "
                f"alpha={self.alpha}, beta={self.beta}, rho={self.rho})")