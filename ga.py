import random

from models import Package, Truck


def calculate_fitness(packages: list[Package]) -> float:
    """Kalkylerar fitness-värdet med 'Triage'-strategi."""
    trucks = []
    for i in range(10):
        trucks.append(Truck(f"Lastbil_{i + 1}"))

    loaded_package_ids = set()

    for p in packages:
        for truck in trucks:
            if truck.add_package(p):
                loaded_package_ids.add(p.package_id)
                break

    total_score = float(0)

    for p in packages:
        if p.package_id in loaded_package_ids:
            total_score += p.calculate_profit()

            if p.deadline >= 0:
                days_after_one_day = p.deadline - 1
                if days_after_one_day < 0:
                    penalty_if_skipped = abs(days_after_one_day) ** 2
                    total_score += penalty_if_skipped
            else:
                current_penalty = abs(p.deadline) ** 2
                next_penalty = (abs(p.deadline) + 1) ** 2
                penalty_growth = next_penalty - current_penalty
                total_score += penalty_growth

        else:
            if p.deadline < 0:
                days_late = abs(p.deadline)
                penalty = days_late**2
                total_score -= penalty

    return total_score


def create_population(
    packages: list[Package], population_size: int
) -> list[list[Package]]:
    """Skapar en initial population av individer slumpmässigt."""
    population = []
    for i in range(population_size):
        individual = packages[:]
        random.shuffle(individual)
        population.append(individual)

    return population


def selection(
    population: list[list[Package]],
    fitness_scores: list[float],
    tournament_size: int = 5,
) -> list[list[Package]]:
    """Tournament Selection: Väljer ut föräldrar genom att låta slumpmässiga individer tävla."""
    parents = []
    for i in range(2):
        competitors = random.sample(range(len(population)), tournament_size)

        best_index = competitors[0]
        best_competitor_score = fitness_scores[best_index]
        best_competitors = population[best_index]

        for index in competitors[1:]:
            score = fitness_scores[index]
            if score > best_competitor_score:
                best_competitor_score = score
                best_competitors = population[index]

        parents.append(best_competitors)

    return parents


def crossover(parent1: list[Package], parent2: list[Package]):
    """Gör crossover mellan två "parents" för att skapa ett "barn"."""
    child: list = [None] * len(parent1)
    start = random.randint(0, len(parent1) - 1)
    end = random.randint(0, len(parent1) - 1)

    if start > end:
        start, end = end, start

    taken_packages = set()

    for i in range(start, end + 1):
        package = parent1[i]
        child[i] = package
        taken_packages.add(package.package_id)

    current_pos = 0
    for package in parent2:
        if package.package_id in taken_packages:
            continue
        while child[current_pos] is not None:
            current_pos += 1
            if current_pos >= len(child):
                break

        if current_pos < len(child):
            child[current_pos] = package

    return child


def mutate(individual: list[Package], mutation_rate: float):
    """Funktion för mutering av en individ"""
    num_swaps = max(1, int(len(individual) * 0.01))

    for i in range(num_swaps):
        if random.random() > mutation_rate:
            continue
        idx1 = random.randint(0, len(individual) - 1)
        idx2 = random.randint(0, len(individual) - 1)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]


def genetic_algorithm(
    packages: list[Package],
    population_size: int,
    generations: int,
    mutation_rate: float,
    patience: int = 10,
):
    """Huvudfunktionen för den genetiska algoritmen."""
    population = create_population(packages, population_size)

    best_solution = population[0]
    best_fitness = calculate_fitness(best_solution)
    no_improvement_counter = 0

    history = []

    print(
        f"Startar genetisk algoritm med populationsstorlek {population_size}, generationer {generations}, mutationsfrekvens {mutation_rate}"
    )

    for gen in range(generations):
        fitness_scores = []

        for individual in population:
            score = calculate_fitness(individual)
            fitness_scores.append(score)

        current_best_fitness = max(fitness_scores)

        history.append(current_best_fitness)

        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_index = fitness_scores.index(current_best_fitness)
            best_solution = population[best_index]
            print(
                f"Generation {gen + 1}: Nytt bästa fitness-värde hittat: {best_fitness}"
            )
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1

        if no_improvement_counter >= patience:
            print(
                f"Ingen förbättring på {patience} generationer. Avslutar tidigt vid generation {gen + 1}."
            )
            break

        new_population = [best_solution]

        while len(new_population) < population_size:
            parents = selection(population, fitness_scores)
            child = crossover(parents[0], parents[1])
            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
    print(f"Bästa lösning hittad med fitness: {best_fitness}")
    return best_solution, best_fitness, history
