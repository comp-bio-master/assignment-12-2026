def GCcontent(dna):
    """Return fraction of A/C/G/T bases that are G or C; None if none."""
    dna = dna.upper()
    numG = dna.count("G")
    numC = dna.count("C")
    numA = dna.count("A")
    numT = dna.count("T")
    total = numA + numC + numG + numT
    if total == 0:
        return None
    return (numG + numC) / total


def squared(start=1, end=10):
    results = []
    for i in range(start, end):
        results.append(i ** 2)
    return results
