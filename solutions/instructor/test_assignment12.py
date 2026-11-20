import random
import drift
from function_practice import GCcontent, squared
from simulate_drift import simulate_drift

assert GCcontent("GGCC") == 1.0
assert GCcontent("AAAA") == 0.0
assert GCcontent("atgc") == 0.5
assert GCcontent("NNNN") is None
assert squared(3, 6) == [9, 16, 25]
assert drift.build_population(4, 1.0) == [("A", "A")] * 4
assert drift.build_population(4, 0.0) == [("a", "a")] * 4
example = [("A", "A"), ("A", "a"), ("a", "A"), ("a", "a")]
assert drift.count_genotypes(example) == {"AA": 1, "Aa": 2, "aa": 1}
random.seed(2026)
for n in (1, 10, 100):
    population = drift.build_population(n, 0.5)
    offspring = drift.reproduce_population(population)
    assert len(offspring) == n
    assert all(len(genotype) == 2 for genotype in offspring)
    assert all(allele in ("A", "a") for genotype in offspring for allele in genotype)
assert simulate_drift(10, 1.0)[0:2] == (0, "A")
assert simulate_drift(10, 0.0)[0:2] == (0, "a")
print("All checks passed!")
