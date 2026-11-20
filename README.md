# Assignment 12: Writing Good Code — Simulating Genetic Drift

  
**Submit:** Push the required files to your individual Assignment 12 GitHub repository.

> [!IMPORTANT]
> This is an **independent, guided assignment**, not an additional class meeting. Read each section in order, run the examples, and check your output before proceeding. You are expected to understand and explain the code you submit.

## What you will learn

By the end of this assignment, you will be able to:

1. Write and call Python functions using parameters and `return`.
2. Divide a larger biological problem into smaller, testable functions.
3. Save functions in a Python *module* and import them into a separate script.
4. Run a Python program from the Bash command line with arguments.
5. Check that code works using simple tests and use a simulation to investigate genetic drift.
6. Document and submit a reproducible programming project using Git and GitHub.

**Background:** We have already used Python variables, lists, tuples, dictionaries, loops, conditionals, and files in Lectures 10–11. This assignment brings those skills together. You **do not need** to install NumPy or SciPy: we will use Python's built-in `random` module. [Original Lecture 12](https://github.com/tamucc-comp-bio/classroom_repo_2026/blob/main/lectures/lecture12.md) is available for additional examples; the instructions here supersede its older code.

## 0. Prepare your computer and repository

Use the Python installation you configured earlier in the course. In Bash, check:

```bash
python3 --version
git --version
```

Accept the instructor's Assignment 12 repository invitation and clone **your own** repository, as you did for earlier assignments:

```bash
cd ~
git clone YOUR_ASSIGNMENT_12_REPO_SSH_URL assignment-12
cd assignment-12
pwd
```

Replace `YOUR_ASSIGNMENT_12_REPO_SSH_URL` with the SSH clone URL of your personal assignment repository. If you already cloned it, enter that directory instead; do not clone it a second time.

You will produce these files in the **root of that repository**:

```text
assignment-12/
├── README.md                 # Your explanations, results, and instructions
├── function_practice.py      # The introductory function exercises
├── drift.py                  # Three functions for the genetic drift model
└── simulate_drift.py         # The program you run from Bash
```

> [!TIP]
> You may develop code in any plain-text editor. Test your files by running them from Bash. Save frequently and commit your progress to GitHub.

---

## 1. Think before you code

Good scientific code is easier to test and modify when a complex task is broken into smaller steps. Before beginning, answer the following in the **Planning** section of your `README.md` (2–4 sentences or a short numbered outline):

- What biological question will our simulation address?
- What information must go into the simulation, and what should come out?
- Why might it be helpful to write several functions instead of one very long script?

Use plain English first. This is a form of **pseudocode**: describing the steps before worrying about Python syntax.

## 2. Practice writing functions

A *function* is a named block of code that can accept inputs, perform an operation, and return a result. We have used built-in functions such as `len()` and `sum()`. Now we will write our own.

### 2.1 Calculate GC content

Use a text editor (nano, notepad++, bbedit) to create a file named`function_practice.py` and enter this function:

```python
def GCcontent(dna):
    """Return the fraction of A/C/G/T bases that are G or C.

    Ignore other characters (such as N). Return None if no A/C/G/T
    bases are present.
    """
    dna = dna.upper()
    numG = dna.count("G")
    numC = dna.count("C")
    numA = dna.count("A")
    numT = dna.count("T")
    total = numA + numC + numG + numT
    if total == 0:
        return None
    return (numG + numC) / total
```

Notice the `def` keyword, the function name `GCcontent`, the parameter `dna`, and the `return` statement. Unlike `print()`, `return` makes a value available to other parts of a program. The `if` statement also prevents division by zero if a sequence contains no A, C, G, or T.

Run your code in an interactive Python session from the repository directory:

```bash
python3
```

```python
>>> from function_practice import GCcontent
>>> GCcontent("AATTTCCCGGGAAA")
0.42857142857142855
>>> GCcontent("atgcatgc")
0.5
>>> GCcontent("GGNNCC")
1.0
>>> GCcontent("NNNN") is None
True
```

The results should match. Exit Python using `Ctrl-D` (on macOS/Linux) or `exit()`.

### 2.2 Write a second function yourself

In the file you made above, `function_practice.py`, create a function called `squared(start=1, end=10)` that:

1. Creates an empty list.
2. Uses a `for` loop with `range(start, end)`.
3. Appends the square of each number to the list.
4. **Returns** the list.

The default values should allow these commands to work:

```python
>>> from function_practice import squared
>>> squared()
[1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> squared(3, 6)
[9, 16, 25]
>>> squared(end=3)
[1, 4]
```

**Checkpoint 1:** Both functions run from an interactive Python session, produce the expected results, and are saved in `function_practice.py`. Add a short note to the **Function practice** section of `answers.md` explaining the difference between `print` and `return`.

---

## 3. The biological problem: [genetic drift](https://en.wikipedia.org/wiki/Genetic_drift)

We will use a simplified **[Wright–Fisher simulation](https://en.wikipedia.org/wiki/Genetic_drift#Wright.E2.80.93Fisher_model)** to investigate how chance alone can change allele frequencies through time.

Assume that:

- The population contains `N` diploid individuals of one reproducing type.
- One gene has two alleles: `A` and `a`.
- In the starting population, the probability of drawing `A` is `p`; the probability of `a` is `1 - p`.
- Each new individual receives one allele chosen at random from each of two parents. Parents are chosen at random **with replacement** from the previous generation.
- The population size is constant. Generations do not overlap. There is no mutation, migration, or selection.

We will follow the population until an allele becomes **fixed**: all individuals have [genotype](https://en.wikipedia.org/wiki/Genotype) `AA`, or all have genotype `aa`.

### 3.1 Choose a data structure

A population will be a **list of tuples**. Each tuple contains the two alleles belonging to one diploid individual:

```python
population = [("A", "a"), ("A", "A"), ("a", "a")]
```

This represents three diploid individuals and six total copies of the gene. The order of alleles within a tuple has no biological significance in this model, so `("A", "a")` and `("a", "A")` are both heterozygotes.

We will create three functions in `drift.py`, then a fourth function in `simulate_drift.py` to coordinate them.

| Function | Input | Output |
| --- | --- | --- |
| `build_population(N, p)` | Population size and starting allele frequency | A list of N diploid individuals |
| `count_genotypes(population)` | A population | A dictionary of genotype **counts** |
| `reproduce_population(population)` | A population | A new population of the same size |
| `simulate_drift(N, p)` | Population size and starting frequency | Generations to fixation, fixed allele, final genotype counts |

> [!NOTE]
> The original Lecture 12 called its counting function `compute_frequencies()`, but it actually returned **counts**, not frequencies. We use the more accurate name `count_genotypes()` in this assignment.

## 4. Build the population (`drift.py`)

Create `drift.py`. At the top, import Python's standard-library `random` module:

```python
import random
```

The following function creates `N` individuals. For each of the two gene copies, `random.random()` gives a number between 0 and 1; it is used to decide whether the allele is `A` or `a`:

```python
def build_population(N, p):
    """Create N diploid individuals with initial A frequency p."""
    population = []
    for i in range(N):
        allele1 = "A" if random.random() < p else "a"
        allele2 = "A" if random.random() < p else "a"
        population.append((allele1, allele2))
    return population
```

You have seen `if/else` statements already; the conditional expressions above are a shorter way to write the same logic. Add the function to `drift.py`. Follow Python's usual style of **four spaces per indentation level** (see [PEP 8](https://peps.python.org/pep-0008/)).

Test it:

```python
>>> import drift
>>> pop = drift.build_population(10, 0.5)
>>> len(pop)
10
>>> pop
```

The genotypes will vary from run to run because the model uses random numbers. Your list should contain **10 tuples, each with two alleles**.

Try `drift.build_population(5, 1.0)` and `drift.build_population(5, 0.0)`. What genotypes should each produce? Do you get the expected result?

**Checkpoint 2:** Explain in `answers.md` why two calls with `N=10, p=0.5` usually produce different populations, and why the results with `p=0` or `p=1` do not vary.

## 5. Count genotypes (`drift.py`)

Now write a second function in the same file, called `count_genotypes(population)`.

The function must return a dictionary with **exactly these keys**: `"AA"`, `"Aa"`, and `"aa"`. The values are integer **[genotypic](https://en.wikipedia.org/wiki/Genotype) counts**, not frequencies. Both forms of the heterozygote (`("A", "a")` and `("a", "A")`) count as `"Aa"`.

You can use the list method `.count()` to count a particular tuple. For example:

```python
population = [("A", "A"), ("A", "a"), ("a", "A"), ("a", "a")]
population.count(("A", "A"))          # 1
population.count(("A", "a"))          # 1
```

Use these ideas to complete the function. Your result for this fixed example **must** be:

```python
>>> import drift
>>> example = [("A", "A"), ("A", "a"), ("a", "A"), ("a", "a")]
>>> drift.count_genotypes(example)
{'AA': 1, 'Aa': 2, 'aa': 1}
```

Also test:

```python
>>> counts = drift.count_genotypes(drift.build_population(100, 0.5))
>>> sum(counts.values())
100
```

**Checkpoint 3:** The three counts always add up to `N`, and the function treats both heterozygote orders as the same genotype. Explain why the sum must equal `N`.

## 6. Reproduce the population (`drift.py`)

Our next function will construct a new generation of exactly `N` individuals from the current one.

For each offspring, the function needs to:

1. Select two parents independently at random from the current generation.
2. Select one of the two alleles randomly from each parent.
3. Combine those alleles into one offspring tuple.
4. Add that offspring to the next-generation list.

Python's `random.randrange(N)` chooses a random index between `0` and `N-1`; `random.randrange(2)` chooses either allele index `0` or `1`.

Here is a skeleton to complete. Replace the `TODO` lines with Python statements:

```python
def reproduce_population(population):
    """Produce one non-overlapping generation by random mating."""
    N = len(population)
    new_generation = []
    for i in range(N):
        parent1 = random.randrange(N)
        parent2 = random.randrange(N)
        copy1 = random.randrange(2)
        copy2 = random.randrange(2)

        # TODO: Get one allele from population[parent1][copy1].
        # TODO: Get one allele from population[parent2][copy2].
        # TODO: Combine the two alleles as a tuple named offspring.
        # TODO: Append offspring to new_generation.

    return new_generation
```

Note that the two allele-copy indices are chosen **independently**. This is important even when the same individual happens to be sampled as both parents.

Test your function:

```python
>>> pop = drift.build_population(20, 0.5)
>>> next_pop = drift.reproduce_population(pop)
>>> len(next_pop) == len(pop)
True
>>> all(len(individual) == 2 for individual in next_pop)
True
```

**Checkpoint 4:** The next generation must have the same number of individuals. Each genotype must contain exactly two alleles, and each allele must be `A` or `a`.

---

## 7. Combine the functions into a program (`simulate_drift.py`)

We now have the building blocks of a population simulation. Create `simulate_drift.py` in the **same directory** as `drift.py`.

At the top of the file put:

```python
#!/usr/bin/env python3

import random
import sys
import drift
```

### 7.1 Write the simulation function

Create a function named `simulate_drift(N, p)` with the following plan:

```text
1. Build the initial population.
2. Set the generation counter to 0.
3. Repeat:
   a. Count AA, Aa, and aa individuals.
   b. If every individual is AA, stop: A is fixed.
   c. If every individual is aa, stop: a is fixed.
   d. Otherwise, reproduce to create the next generation.
   e. Increase the generation counter by one.
4. Return the generation count, the fixed allele, and the final counts.
```

In this simulation, generation **0** is the initial population. If `p=0` or `p=1`, fixation has already occurred at generation 0.

Use `while True`, `if` statements, and `return` to implement the plan. You may find this starter helpful:

```python
def simulate_drift(N, p):
    population = drift.build_population(N, p)
    generations = 0

    while True:
        counts = drift.count_genotypes(population)

        # TODO: If counts["AA"] == N, return (generations, "A", counts).
        # TODO: If counts["aa"] == N, return (generations, "a", counts).
        # TODO: Otherwise, replace population with the next generation.
        # TODO: Increment generations by 1.
```

Be careful: `=` assigns a value; `==` compares two values. Use `return` to exit the function when fixation is detected.

### 7.2 Accept command-line arguments

A program is more useful when we can supply its inputs from Bash instead of editing the code every time. Add this block **at the bottom** of `simulate_drift.py`:

```python
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
```

`sys.argv` is a list of the words supplied on the command line: `sys.argv[1]` is `N`, and `sys.argv[2]` is `p`. The optional `seed` controls the random number generator. **The same seed and inputs should reproduce the same simulation result**; different seeds usually produce different results.

The provided argument-checking code gives a meaningful error for invalid input. You do not have to invent this code, but you should be able to explain what it checks.

### 7.3 Run the program from Bash

Exit the Python interpreter before entering these commands. From the assignment directory run:

```bash
python3 simulate_drift.py 10 0.5
python3 simulate_drift.py 100 0.5
python3 simulate_drift.py 20 1.0
python3 simulate_drift.py 20 0.0
```

You should see the generation when fixation occurred, the allele that fixed, and final counts such as `{'AA': 10, 'Aa': 0, 'aa': 0}`. The exact generation and allele for `p=0.5` depend on random chance.

To make a run repeatable, provide a third number:

```bash
python3 simulate_drift.py 20 0.5 2026
python3 simulate_drift.py 20 0.5 2026
```

The two lines should give **identical** output. You can also make the file executable (optional):

```bash
chmod +x simulate_drift.py
./simulate_drift.py 20 0.5 2026
```

**Checkpoint 5:** Your program runs from Bash; `p=0` and `p=1` report fixation at generation 0; repeating a seeded command gives identical output.

---

## 8. Test your code: do not just hope it works

Scientific results are only useful when the software producing them is trustworthy. Testing means checking behavior against expected results, including edge cases.

### 8.1 Run these checks

Start Python in your assignment directory and run:

```python
import random
import drift
from function_practice import GCcontent, squared
from simulate_drift import simulate_drift

# Function practice
assert GCcontent("GGCC") == 1.0
assert GCcontent("AAAA") == 0.0
assert GCcontent("atgc") == 0.5
assert GCcontent("NNNN") is None
assert squared(3, 6) == [9, 16, 25]

# Deterministic population boundaries
assert drift.build_population(4, 1.0) == [("A", "A")] * 4
assert drift.build_population(4, 0.0) == [("a", "a")] * 4

# Count both orders of heterozygote together
example = [("A", "A"), ("A", "a"), ("a", "A"), ("a", "a")]
assert drift.count_genotypes(example) == {"AA": 1, "Aa": 2, "aa": 1}

# Reproduction preserves population size and genotype structure
random.seed(2026)
for n in (1, 10, 100):
    population = drift.build_population(n, 0.5)
    offspring = drift.reproduce_population(population)
    assert len(offspring) == n
    assert all(len(genotype) == 2 for genotype in offspring)
    assert all(allele in ("A", "a") for genotype in offspring for allele in genotype)

# Already-fixed populations must stop immediately
assert simulate_drift(10, 1.0)[0:2] == (0, "A")
assert simulate_drift(10, 0.0)[0:2] == (0, "a")

print("All checks passed!")
```

If an `assert` fails, Python stops with `AssertionError`. Read the failing statement, inspect the function, fix the problem, then run the checks again. Exit with `exit()`.

### 8.2 Test invalid command-line input

From Bash, also try:

```bash
python3 simulate_drift.py 0 0.5
python3 simulate_drift.py 10 1.5
python3 simulate_drift.py banana 0.5
```

Each should stop with an informative error instead of producing a simulation result. You may copy the error message into `answers.md` if it helps explain the test.

**Checkpoint 6:** In the **Testing** section of your `answers.md`, state whether the checks passed, report one error you encountered (or an edge case you deliberately tested), and explain what you did or learned. Do not submit code with failing tests without explaining the issue.

---

## 9. Biological investigation: does population size affect fixation time?

You now have a program that can test a biological prediction. Because drift is a random process, **one simulation is not enough** to compare population sizes.

**Hypothesis:** Smaller populations typically reach fixation faster than larger populations, when the starting allele frequency is the same.

Conduct **10 independent replicate simulations** for each of these scenarios:

| Scenario | N | Starting p | Replicates |
| --- | ---: | ---: | ---: |
| Small population | 10 | 0.5 | 10 |
| Large population | 100 | 0.5 | 10 |

Run the program 10 times for each population size; do **not** reuse the same seed for all replicates. You can omit the seed argument or use a different integer seed for each run. Record the generation at fixation for every run.

In `answers.md`, include a small table listing the 10 fixation times for each scenario, summarize the typical fixation time (mean or median), and answer these questions:

1. Which population size tended to reach fixation sooner in your simulations?
2. Did every simulation have the same fixation time? Why or why not?
3. How is this result relevant to small or declining natural populations?

You are **not** required to make a plot or write another analysis program. Your results are observations from a stochastic model, not guaranteed outcomes of a single run. It is fine if some individual runs do not match the overall trend.

---

## 10. Complete `answers.md` and submit your work

**Leave `README.md` unchanged**: it contains the assignment instructions. Put all written responses in `answers.md`, the separate file provided in your assignment repository. Complete these sections:

- **Planning:** The simulation problem and your outline from Section 1.
- **Running the program:** Commands to run it, with an example of the output.
- **Function practice:** The distinction between `return` and `print`.
- **Checkpoints:** Your brief answers about randomness and genotype counting.
- **Testing:** Confirmation of the checks and a brief description of an error or edge case.
- **Biological investigation:** Your replicate results, typical fixation times, and answers to the three questions.

Do not paste all your Python code into `answers.md`: it belongs in the `.py` files. Explain enough that another student could clone your repository, run your program, and understand your interpretation. **Do not delete, overwrite, or edit `README.md`.**

From Bash, verify which files you changed and push everything to GitHub:

```bash
git status
git add answers.md function_practice.py drift.py simulate_drift.py
git commit -m "Complete Assignment 12 genetic drift simulation"
git push
```

Check your personal GitHub repository in a browser to confirm that the updated files are visible. **Pushing your work is the submission.**

### Submission checklist

- [ ] `function_practice.py` contains the two working introductory functions.
- [ ] `drift.py` contains `build_population`, `count_genotypes`, and `reproduce_population`.
- [ ] `simulate_drift.py` runs with `N`, `p`, and an optional seed from Bash.
- [ ] Tests pass, including starting frequencies of 0 and 1.
- [ ] `answers.md` contains the planning, testing, explanation, and biological investigation.
- [ ] `README.md` still contains the original assignment instructions and has not been modified.
- [ ] All files are committed and pushed to your individual GitHub repository by the due date.

### How the assignment will be evaluated (100 points)

| Component | Points |
| --- | ---: |
| Function practice and explanation | 15 |
| Three working functions in `drift.py` | 30 |
| Working command-line simulation | 20 |
| Tests and edge-case discussion | 15 |
| Biological investigation and interpretation | 15 |
| `answers.md` clarity and GitHub submission | 5 |

### Optional extension (not required)

Modify your program to save the frequency of allele `A` **at each generation** to a CSV or TSV file. Plot allele frequency against generation number using R (which you already learned), or explain how you would make such a plot. Consider how the trajectories vary among replicates.

---

## Help and references

Before asking for help, note the command you ran, the exact error message, and the smallest input that reproduces the problem. Consult your Lecture 10–11 notes, the [original Lecture 12](https://github.com/tamucc-comp-bio/classroom_repo_2026/blob/main/lectures/lecture12.md), the [Python tutorial on functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions), and the [Python `random` documentation](https://docs.python.org/3/library/random.html). If you use an AI assistant, run and test the code yourself and make sure you can explain what it does.
