import csv
import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from models import Package, Truck


def save_statistics(
    history: list[float], filename: str = "Data/Statistics.csv"
) -> None:
    """Sparar statistik till CSV."""
    file_path = Path(filename)
    file_exists = file_path.exists()

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                [
                    "Tidpunkt",
                    "Start_Fitness",
                    "Gen_50",
                    "Gen_100",
                    "Gen_150",
                    "Gen_200",
                    "Slut_Fitness",
                ]
            )

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        start_value = history[0] if len(history) > 0 else 0
        gen_50 = history[49] if len(history) >= 50 else ""
        gen_100 = history[99] if len(history) >= 100 else ""
        gen_150 = history[149] if len(history) >= 150 else ""
        gen_200 = history[199] if len(history) >= 200 else ""
        end_value = history[-1] if len(history) > 0 else 0

        writer.writerow(
            [timestamp, start_value, gen_50, gen_100, gen_150, gen_200, end_value]
        )

    print(f"\nStatistik sparad till {filename}")


def save_manifest(
    trucks: list[Truck], filename: str = "Data/Lastningsplan.csv"
) -> None:
    """Sparar en lista på vilka paket som ska till vilken bil."""
    file_path = Path(filename)

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Lastbil", "Paket_ID", "Vikt", "Volym", "Förtjänst"])

        for truck in trucks:
            for p in truck.packages:
                writer.writerow(
                    [
                        truck.truck_id,
                        p.package_id,
                        p.weight,
                        p.volume,
                        p.calculate_profit(),
                    ]
                )

    print(f"Lastningsplan sparad till {filename}")


def plot_improvement(history: list[float]) -> None:
    """Plottar förbättringen av bäst fitness över generationerna."""
    generations = range(1, len(history) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(generations, history, marker="o", linestyle="-", color="b")
    plt.title("Förbättring av bästa fitness över generationer")
    plt.xlabel("Generation")
    plt.ylabel("Bästa Fitness-poäng")
    plt.grid(True)
    plt.show()


def analyze_results(
    packages: list[Package], title: str = "Analys av levererade paket"
) -> None:
    """Analyserar och plottar statistik för en lista av paket."""
    weights = []
    for p in packages:
        weights.append(p.weight)
    weights = np.array(weights)
    profits = []
    for p in packages:
        profits.append(p.calculate_profit())
    profits = np.array(profits)

    print(f"\n {title}:")
    print(f"Totalt antal paket: {len(packages)}")
    print(
        f"Snittvikt: {np.mean(weights):.2f} kg, Std: {np.std(weights):.2f}, Var: {np.var(weights):.2f}"
    )
    print(
        f"Snittvinst: {np.mean(profits):.2f}, Std: {np.std(profits):.2f}, Var: {np.var(profits):.2f}"
    )

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.hist(weights, bins=20, color="green", alpha=0.7)
    plt.title(f"Viktfördelning - {title}")
    plt.xlabel("Vikt (kg)")
    plt.ylabel("Antal paket")

    plt.subplot(1, 2, 2)
    plt.hist(profits, bins=20, color="orange", alpha=0.7)
    plt.title(f"Vinstfördelning - {title}")
    plt.xlabel("Vinst (kr)")
    plt.ylabel("Antal paket")

    plt.tight_layout()
    plt.show()


def analyze_leftovers(
    all_packages: list[Package], delivered_packages: list[Package]
) -> float:
    """Analyserar de paket som inte levererades. Returnerar total straffavgift."""
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
        analyze_results(leftover_packages, title="Analys av kvarvarande paket")

    return total_penalty


def print_truck_details(trucks: list[Truck]) -> float:
    """Printar detaljerad information om varje lastbil. Returnerar total vinst."""
    print("\n" + "=" * 80)
    print("DETALJERAD LASTBILSSTATUS")
    print("=" * 80)
    print(
        f"{'ID':<10} {'Paket':<8} {'Vikt (kg)':<20} {'Volym (m3)':<20} {'Vinst (kr)':<15}"
    )
    print("-" * 80)

    total_truck_profit = 0.0

    for truck in trucks:
        weight_pct = (truck.current_weight / truck.weight_capacity) * 100
        volume_pct = (truck.current_volume / truck.volume_capacity) * 100

        truck_profits = []
        for p in truck.packages:
            truck_profits.append(p.calculate_profit())
        truck_profit = sum(truck_profits)
        total_truck_profit += truck_profit

        w_str = (
            f"{truck.current_weight:.1f}/{truck.weight_capacity} ({weight_pct:.0f}%)"
        )
        v_str = (
            f"{truck.current_volume:.1f}/{truck.volume_capacity} ({volume_pct:.0f}%)"
        )

        print(
            f"{truck.truck_id:<10} {len(truck.packages):<8} {w_str:<20} {v_str:<20} {truck_profit:<15.1f}"
        )
    print("=" * 80)
    print(f"TOTAL VINST PÅ LASTBILARNA: {total_truck_profit:.1f} kr")
    print("=" * 80)

    return total_truck_profit
