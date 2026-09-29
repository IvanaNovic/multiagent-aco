import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot_convergence(colonies, save_path=None):
    plt.figure(figsize=(10, 6))

    for colony in colonies:
        label = f"Kolonija {colony.colony_id} (a={colony.alpha}, b={colony.beta}, r={colony.rho})"
        plt.plot(colony.history, label=label)

    plt.xlabel("Iteracija")
    plt.ylabel("Najbolja duzina ture")
    plt.title("Konvergencija ACO kolonija")
    plt.legend()
    plt.grid(True)

    if save_path:
        plt.savefig(save_path)
        print(f"Grafik sacuvan: {save_path}")
    else:
        plt.show()

def plot_pheromones(graph, colony, save_path=None, min_linewidth=0.3, max_linewidth=6.0):

    plt.figure(figsize=(10, 10))

    coords = {city_id: (x, y) for city_id, x, y in graph.cities}

    pheromone_values = list(colony.pheromones.values())
    max_pheromone = max(pheromone_values) if pheromone_values else 1.0

    for (city_a, city_b), tau in colony.pheromones.items():
        if city_a < city_b:
            x1, y1 = coords[city_a]
            x2, y2 = coords[city_b]

            intensity = tau / max_pheromone
            linewidth = min_linewidth + intensity * (max_linewidth - min_linewidth)

            plt.plot([x1, x2], [y1, y2],
                     color="darkorange", alpha=min(intensity + 0.1, 1.0),
                     linewidth=linewidth, zorder=1)

    for city_id, (x, y) in coords.items():
        plt.scatter(x, y, color="steelblue", s=100, zorder=2)
        plt.annotate(str(city_id), (x, y), textcoords="offset points",
                     xytext=(5, 5), fontsize=9)

    plt.title(f"Feromoni - Kolonija {colony.colony_id} "
              f"(a={colony.alpha}, b={colony.beta}, r={colony.rho})")
    plt.xlabel("X")
    plt.ylabel("Y")

    if save_path:
        plt.savefig(save_path)
        print(f"Grafik sacuvan: {save_path}")
    else:
        plt.show()

    plt.close()

def animate_pheromones(graph, snapshots, colony, save_path="results/pheromone_animation.gif"):
    fig, ax = plt.subplots(figsize=(10, 10))
    coords = {city_id: (x, y) for city_id, x, y in graph.cities}

    max_pheromone = max(max(s.values()) for s in snapshots)

    def update(frame_index):
        ax.clear()
        pheromones = snapshots[frame_index]

        for (city_a, city_b), tau in pheromones.items():
            if city_a < city_b:
                x1, y1 = coords[city_a]
                x2, y2 = coords[city_b]
                intensity = tau / max_pheromone
                linewidth = 0.3 + intensity * 5.7
                ax.plot([x1, x2], [y1, y2], color="darkorange",
                         alpha=min(intensity + 0.1, 1.0), linewidth=linewidth, zorder=1)

        for city_id, (x, y) in coords.items():
            ax.scatter(x, y, color="steelblue", s=100, zorder=2)

        ax.set_title(f"Feromoni - Kolonija {colony.colony_id} - Frejm {frame_index + 1}/{len(snapshots)}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

    anim = FuncAnimation(fig, update, frames=len(snapshots), interval=400)
    anim.save(save_path, writer="pillow")
    print(f"Animacija sacuvana: {save_path}")
    plt.close()