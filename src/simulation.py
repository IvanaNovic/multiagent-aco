from src.colony import Colony
import copy

class Simulation:
    def __init__(self, graph, colony_configs, num_iterations=100):

        self.graph = graph
        self.num_iterations = num_iterations
        self.colonies = []

        for i, config in enumerate(colony_configs):
            colony = Colony(colony_id=i, **config)
            colony.init_pheromones(graph)
            self.colonies.append(colony)

    def _run_ants_for_colony(self, colony, start_city):
        ants= [colony.construct_tour(start_city, self.graph)
                for _ in range(colony.num_ants)]
        colony.update_pheromones(ants, self.graph)

    def run_independent(self):
        start_city = self.graph.cities[0][0]

        for iteration in range(self.num_iterations):
            for colony in self.colonies:
                self._run_ants_for_colony(colony, start_city)

        return self.colonies

    def run_cooperative(self, exchange_interval=10):
        start_city = self.graph.cities[0][0]

        for iteration in range(self.num_iterations):
            for colony in self.colonies:
                self._run_ants_for_colony(colony, start_city)
            if (iteration + 1) % exchange_interval == 0:
                self._exchange_pheromones()

        return self.colonies

    def _exchange_pheromones(self, injection_weight=0.2):
        best_colony = min(self.colonies, key=lambda c: c.best_tour_length)

        for colony in self.colonies:
            if colony.colony_id == best_colony.colony_id:
                continue
            for edge in colony.pheromones:
                colony.pheromones[edge] += injection_weight * best_colony.pheromones[edge]

    def run_competitive(self):
        self.run_independent()

        best_colony = min(self.colonies, key=lambda c: c.best_tour_length)
        print(f"Pobjednicka kolonija: {best_colony.colony_id} "
              f"sa turom {best_colony.best_tour_length:.2f}")

        return self.colonies, best_colony

    def run_with_snapshots(self, colony_index=0, snapshot_interval=5):

        colony = self.colonies[colony_index]
        start_city = self.graph.cities[0][0]
        snapshots = []

        for iteration in range(self.num_iterations):
            self._run_ants_for_colony(colony, start_city)

            if iteration % snapshot_interval == 0:
                snapshots.append(copy.deepcopy(colony.pheromones))

        snapshots.append(copy.deepcopy(colony.pheromones))  # finalno stanje
        return colony, snapshots