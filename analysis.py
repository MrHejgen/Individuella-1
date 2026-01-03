import matplotlib.pyplot as plt
import numpy as np

from models import Package, Truck


def plot_improvement(history: list[float]) -> None:
    """Plottar förbättringen av den bäst fitness över generationerna."""
    generations = range(1, len(history) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(generations, history, marker="o", linestyle="-", color="b")
    plt.title("Improvement of Best Fitness Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness Score")
    plt.grid(True)
    plt.show()


def analyze_results(
    packages: list[Package], title: str = "Analysis of Delivered Packages"
) -> None:
    """Analyserar och plottar statistik för en lista av paket."""
    weights = np.array([p.weight for p in packages])
    profits = np.array([p.calculate_profit() for p in packages])

    print(f"\n {title}:")
    print(f"Total Packages: {len(packages)}")
    print(
        f"Average Weight: {np.mean(weights):.2f} kg, Std: {np.std(weights):.2f}, Var: {np.var(weights):.2f}"
    )
    print(
        f"Average Profit: {np.mean(profits):.2f}, Std: {np.std(profits):.2f}, Var: {np.var(profits):.2f}"
    )

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.hist(weights, bins=20, color="green", alpha=0.7)
    plt.title(f"Weight Distribution - {title}")
    plt.xlabel("Weight (kg)")
    plt.ylabel("Number of Packages")

    plt.subplot(1, 2, 2)
    plt.hist(profits, bins=20, color="orange", alpha=0.7)
    plt.title(f"Profit Distribution - {title}")
    plt.xlabel("Profit (kr)")
    plt.ylabel("Number of Packages")

    plt.tight_layout()
    plt.show()


def analyze_leftovers(
    all_packages: list[Package], delivered_packages: list[Package]
) -> None:
    """Analyserar de paket som inte levererades."""
    delivered_ids = {p.package_id for p in delivered_packages}

    leftover_packages = []
    total_penalty = 0
    potential_profit_left = 0.0

    for p in all_packages:
        if p.package_id not in delivered_ids:
            leftover_packages.append(p)
            if p.deadline < 0:
                days_late = abs(p.deadline)
                penalty = days_late**2
                total_penalty += penalty
            potential_profit_left += p.profit

    print("\n" + "=" * 40)
    print("LAGERSTATUS (DET SOM BLEV KVAR)")
    print("=" * 40)
    print(f"Antal paket kvar:      {len(leftover_packages)}")
    print(f"Missad vinst (brutto): {potential_profit_left:.1f} kr")
    print(f"TOTAL STRAFFAVGIFT:    -{total_penalty:.1f} kr")
    print("-" * 40)

    if len(leftover_packages) > 0:
        print("Statistik för kvarvarande paket:")
        analyze_results(leftover_packages, title="Analysis of Leftover Packages")


def print_truck_details(trucks: list[Truck]) -> None:
    """Printar detaljerad information om varje lastbil."""
    print("\n" + "=" * 65)
    print("DETALJERAD LASTBILSSTATUS")
    print("=" * 65)
    print(f"{'ID':<10} {'Paket':<8} {'Vikt (kg)':<20} {'Volym (m3)':<20}")
    print("-" * 65)

    for truck in trucks:
        w_pct = (truck.current_weight / truck.weight_capacity) * 100
        v_pct = (truck.current_volume / truck.volume_capacity) * 100

        w_str = f"{truck.current_weight:.1f}/{truck.weight_capacity} ({w_pct:.0f}%)"
        v_str = f"{truck.current_volume:.1f}/{truck.volume_capacity} ({v_pct:.0f}%)"

        print(f"{truck.truck_id:<10} {len(truck.packages):<8} {w_str:<20} {v_str:<20}")
    print("=" * 65)
