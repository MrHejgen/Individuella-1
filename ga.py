import random

from models import Package, Truck


def calculate_fitness(packages: list[Package]) -> float:
    """Kalkylerar fitness-värdet av paket."""
    trucks = []
    for i in range(10):
        trucks.append(Truck(f"Lastbil_{i + 1}"))

    for p in packages:
        if p.calculate_profit() <= 0:
            continue
        for truck in trucks:
            if truck.add_package(p):
                break

    total_profit = float(0)

    for truck in trucks:
        for p in truck.packages:
            total_profit += p.calculate_profit()

    return total_profit


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
    if random.random() < mutation_rate:
        num_swaps = int(len(individual) * 0.1)
        for i in range(num_swaps):
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

    # Initiera med första individen istället för None
    best_solution = population[0]
    best_fitness = calculate_fitness(best_solution)
    no_improvement_counter = 0

    history = []

    print(
        f"Starting Genetic Algorithm with population size {population_size}, generations {generations}, mutation rate {mutation_rate}"
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
            print(f"Generation {gen + 1}: New best fitness found: {best_fitness}")
            no_improvement_counter = 0
        else:
            no_improvement_counter += 1

        if no_improvement_counter >= patience:
            print(
                f"No improvement for {patience} generations. Stopping early at generation {gen + 1}."
            )
            break

        # Elitism: Behåll den bästa lösningen direkt till nästa generation
        new_population = [best_solution]

        # Fyll på resten med Tournament Selection och Crossover
        while len(new_population) < population_size:
            parents = selection(population, fitness_scores)
            child = crossover(parents[0], parents[1])
            mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
    print(f"Best solution found with fitness: {best_fitness}")
    return best_solution, best_fitness, history
