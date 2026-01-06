import csv
from pathlib import Path

from analysis import (
    analyze_leftovers,
    analyze_results,
    plot_improvement,
    print_truck_details,
    save_manifest,
    save_statistics,
)
from ga import (
    genetic_algorithm,
)
from models import Package, Truck

TestData1 = Path("data/TestData1.csv")


def load_data(file_name: Path) -> list[Package]:
    packages: list[Package] = []
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            package_id = int(row["Paket_id"])
            weight = float(row["Vikt"])
            profit = float(row["Förtjänst"])
            deadline = int(row["Deadline"])
            volume = float(row["Volym"])
            new_package = Package(package_id, weight, profit, deadline, volume)
            packages.append(new_package)
    return packages


if __name__ == "__main__":
    print("Laddar data...")
    packages = load_data(TestData1)
    best_solution, best_fitness, history = genetic_algorithm(
        packages, population_size=200, generations=200, mutation_rate=0.2, patience=25
    )

    print(f"Högsta poäng: {best_fitness}")

    save_statistics(history)
    plot_improvement(history)

    trucks = []
    for i in range(10):
        trucks.append(Truck(f"Bil_{i + 1}"))

    delivered_packages = []

    for p in best_solution:
        for truck in trucks:
            if truck.add_package(p):
                delivered_packages.append(p)
                break

    save_manifest(trucks)
    truck_profit = print_truck_details(trucks)

    print("\n--- Analys av levererade paket ---")
    analyze_results(delivered_packages)
    print("\n--- Analys av olämnade paket ---")
    warehouse_penalty = analyze_leftovers(packages, delivered_packages)

    print("\n" + "#" * 50)
    print("SLUTRESULTAT FÖR DAGEN")
    print("#" * 50)
    print(f"Vinst från leveranser:   + {truck_profit:.1f} kr")
    print(f"Straffavgift lager:      - {warehouse_penalty:.1f} kr")
    print("-" * 50)
    print(f"TOTALT RESULTAT:         {truck_profit - warehouse_penalty:.1f} kr")
    print("#" * 50)
