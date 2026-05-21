def calculate_robustness_score(
    walk_forward_efficiency,
    consistency_score,
    drawdown_score,
    parameter_stability
):
    score = (
        (walk_forward_efficiency * 0.35) +
        (consistency_score * 0.25) +
        (drawdown_score * 0.20) +
        (parameter_stability * 0.20)
    )

    return round(score, 2)