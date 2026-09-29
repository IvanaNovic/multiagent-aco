import statistics
from src.graph import Graph
from src.simulation import Simulation


def stability_analysis(graph, colony_configs, num_iterations, num_runs=10):
    """
    Pokrece kompletnu simulaciju vise puta i racuna prosjek/varijansu
    najbolje duzine ture po koloniji, radi provjere stabilnosti algoritma.
    """
    results_per_colony = {i: [] for i in range(len(colony_configs))}

    for run in range(num_runs):
        sim = Simulation(graph, colony_configs, num_iterations)
        colonies = sim.run_independent()
        for c in colonies:
            results_per_colony[c.colony_id].append(c.best_tour_length)

    summary = {}
    for colony_id, lengths in results_per_colony.items():
        summary[colony_id] = {
            "mean": statistics.mean(lengths),
            "stdev": statistics.stdev(lengths) if len(lengths) > 1 else 0.0,
            "min": min(lengths),
            "max": max(lengths),
        }

    return summary