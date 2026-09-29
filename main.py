import argparse
from src.graph import Graph
from src.simulation import Simulation
from src.visualize import plot_convergence, plot_pheromones, animate_pheromones
from src.analysis import stability_analysis


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent ACO sistem")
    parser.add_argument("--cities", type=str, default="data/cities.txt")
    parser.add_argument("--iterations", type=int, default=40)
    parser.add_argument("--mode", choices=["independent", "cooperative", "competitive"],
                         default="competitive")
    parser.add_argument("--stability-runs", type=int, default=0,
                         help="Ako je > 0, pokrece analizu stabilnosti sa N ponavljanja")
    parser.add_argument("--animate", action="store_true",
                         help="Generise animaciju sirenja feromona (GIF)")
    args = parser.parse_args()

    graph = Graph.from_file(args.cities)

    configs = [
        {"num_ants": 12, "alpha": 1.0, "beta": 3.0, "rho": 0.5},
        {"num_ants": 12, "alpha": 0.8, "beta": 4.0, "rho": 0.4},
        {"num_ants": 12, "alpha": 1.2, "beta": 2.5, "rho": 0.6},
    ]

    sim = Simulation(graph, configs, num_iterations=args.iterations)

    if args.mode == "independent":
        colonies = sim.run_independent()
    elif args.mode == "cooperative":
        colonies = sim.run_cooperative()
    else:
        colonies, _ = sim.run_competitive()

    for c in colonies:
        print(f"Kolonija {c.colony_id}: najbolja tura = {c.best_tour_length:.2f}")

    plot_convergence(colonies, save_path="results/convergence.png")
    plot_pheromones(graph, colonies[0], save_path="results/pheromones.png")

    if args.stability_runs > 0:
        summary = stability_analysis(graph, configs, args.iterations, args.stability_runs)
        for colony_id, stats in summary.items():
            print(f"Kolonija {colony_id}: prosjek={stats['mean']:.2f}, stdev={stats['stdev']:.2f}")

    if args.animate:
        anim_sim = Simulation(graph, configs, num_iterations=args.iterations)
        anim_colony, snapshots = anim_sim.run_with_snapshots(
            colony_index=0, snapshot_interval=max(1, args.iterations // 8)
        )
        animate_pheromones(graph, snapshots, anim_colony)


if __name__ == "__main__":
    main()