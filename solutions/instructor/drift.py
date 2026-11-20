import random


def build_population(N, p):
    """Create N diploid individuals with initial A frequency p."""
    population = []
    for i in range(N):
        allele1 = "A" if random.random() < p else "a"
        allele2 = "A" if random.random() < p else "a"
        population.append((allele1, allele2))
    return population


def count_genotypes(population):
    return {
        "AA": population.count(("A", "A")),
        "Aa": population.count(("A", "a")) + population.count(("a", "A")),
        "aa": population.count(("a", "a")),
    }


def reproduce_population(population):
    """Produce one non-overlapping generation by random mating."""
    N = len(population)
    new_generation = []
    for i in range(N):
        parent1 = random.randrange(N)
        parent2 = random.randrange(N)
        copy1 = random.randrange(2)
        copy2 = random.randrange(2)
        allele1 = population[parent1][copy1]
        allele2 = population[parent2][copy2]
        offspring = (allele1, allele2)
        new_generation.append(offspring)
    return new_generation
