from leven import levenshtein as leven


def score(a: str, b: str, *, case_sensitive: bool=True) -> float:
    if not case_sensitive:
        a = a.upper()
        b = b.upper()

    diff = leven(a, b)
    if diff == 0:
        return 1
    if diff == min(len(a), len(b)):
        return 0

    length = max(len(a), len(b))
    return (length - diff) / length
