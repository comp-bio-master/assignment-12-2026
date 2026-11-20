#!/usr/bin/env python3
import random
import sys
import drift


def simulate_drift(N, p):
    population = drift.build_population(N, p)
    generations = 0
    while True:
        counts = drift.count_genotypes(population)
        if counts["AA"] == N:
            return generations, "A", counts
        if counts["aa"] == N:
            return generations, "a", counts
        population = drift.reproduce_population(population)
        generations += 1


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        raise SystemExit("Usage: python3 simulate_drift.py N p [seed]")

    try:
        N = int(sys.argv[1])
        p = float(sys.argv[2])
        if N < 1 or not (0 <= p <= 1):
            raise ValueError("N must be >= 1 and p must be between 0 and 1")
        if len(sys.argv) == 4:
            random.seed(int(sys.argv[3]))
    except ValueError as error:
        raise SystemExit(f"Invalid arguments: {error}")

    generations, fixed_allele, counts = simulate_drift(N, p)
    print(f"Fixation at generation: {generations}")
    print(f"Fixed allele: {fixed_allele}")
    print(f"Final genotype counts: {counts}")
