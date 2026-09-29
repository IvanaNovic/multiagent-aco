import matplotlib.pyplot as plt


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