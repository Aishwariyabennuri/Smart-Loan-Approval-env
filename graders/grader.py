def compute_score(rewards):
    if not rewards:
        return 0.0

    total = sum(rewards)
    max_possible = len(rewards) * 1.0

    score = total / max_possible
    return round(score, 2)
