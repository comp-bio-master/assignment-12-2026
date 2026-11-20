# Instructor notes — Assignment 12 (not for student distribution)

## Who completes this assignment

- **BIOL 4360 undergraduate students only.** MARB 6360 graduate students are exempt and continue their independent course projects.
- There are no separate graduate-level requirements or graduate extensions for Assignment 12. The optional extension in the student instructions is simply optional undergraduate enrichment.

## Classroom conversion

- Student-facing assignment: `assignment_12_2026.md` (or identical `README.md` for your assignment template repository). **Students should not modify `README.md`.**
- Include `answers.md` as a separate, preformatted student response file. Students edit this alongside their Python scripts and commit/push it. Do not ask them to include their answers in the instructional README.
- Main change: convert Lecture 12 into an independently navigable guide. Retain Lecture 13 for the November 20 in-class meeting.
- Course README currently lists November 20 as Lecture 12 and links an older GitHub Classroom Assignment 12 invitation. Update the lecture schedule and the assignment acceptance link when the Classroom 50 assignment is ready; the old invitation could not be reviewed from here.
- Course due date is shown as December 2, 2026; confirm any specific time on Canvas or Classroom 50.
- The original `lectures/lecture12.md` can remain as a reference archive, but its SciPy, deprecated random calls, shebang advice, and `fixation == True` line should not be used for the new assignment.

## Pedagogical changes

- Students write a small `GCcontent` function and independent `squared` function first.
- Program design is explicitly explained before implementation.
- `build_population` is fully worked; `count_genotypes`, `reproduce_population`, and `simulate_drift` are scaffolded rather than fully supplied.
- The code uses standard-library `random`, so it requires no packages from Lecture 13.
- `count_genotypes` returns genotype counts (AA, Aa, aa), not proportions, and correctly groups both heterozygote orientations.
- The two transmitted copies are selected independently, correcting the dependence in the original lecture's reproduction example.
- The optional seed is useful for reproducible testing; students use independent stochastic runs for the biological comparison.
- Students validate their code with self-checking `assert` statements and summarize at least 10 trials at each of two population sizes.

## Suggested grade breakdown

- Function practice + explanation: 15
- Three `drift.py` functions: 30
- Command-line simulation: 20
- Tests + edge-case discussion: 15
- Biological investigation + interpretation: 15
- `answers.md` + GitHub: 5

## Verified behavior of included reference code

Run `python3 test_assignment12.py` to validate function and simulation edge cases. Example seeded run: `python3 simulate_drift.py 10 0.5 2026` gives fixation of `a` at generation 11. The fixed generation value is implementation-dependent if students draw random numbers in a different order; only repeated runs of *their own* same implementation and seed must match.

Run invalid arguments (`0 0.5`, `10 1.5`, `banana 0.5`) and verify readable errors.

## Example course README change

Replace the two current Week12 lines with, for example:

```markdown
* [11/20 Week12 Scientific Computing](lectures/lecture13.md)
  * [Assignment 12 (undergraduates only): Writing Good Code — Due 12/02/2026](assignments/assignment_12_2026.md)
  * [Assignment 12 personal repository](REPLACE_WITH_CLASSROOM_50_ACCEPT_LINK)
```

Do not use the placeholder invitation link until a Classroom 50 assignment exists. Lecture 13 itself can remain unchanged, except that it currently calls Assignment 12 due on the last day of classes; the course schedule gives December 2.

## Avoid accidentally posting the solutions

The `drift.py`, `simulate_drift.py`, `function_practice.py`, and `test_assignment12.py` in this **instructor** folder provide a working reference. Do **not** upload those reference `.py` files to the student template repository; students are expected to implement the TODOs themselves.
