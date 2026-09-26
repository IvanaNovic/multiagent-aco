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

    def __repr__(self):
        return (f"Colony({self.colony_id}, ants={self.num_ants}, "
                f"alpha={self.alpha}, beta={self.beta}, rho={self.rho})")