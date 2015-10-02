from math import fabs, log, pow

K = 20


def calculate_points(score_1, score_2):
    if score_1 > score_2:
        return (1, 0)

    elif score_1 < score_2:
        return (0, 1)

    return (0.5, 0.5)


def calc_k(score_1, score_2):
    # Source: http://fivethirtyeight.com/datalab/introducing-nfl-elo-ratings/
    pd = fabs(score_1 - score_2)

    return log(pd + 1) * K


def rerank(r_1, r_2, score_1, score_2):
    k = calc_k(score_1, score_2)
    Rank_1 = pow(10, r_1 / 400)
    Rank_2 = pow(10, r_2 / 400)

    S_1, S_2 = calculate_points(score_1, score_2)

    E_1 = Rank_1 / (Rank_1 + Rank_2)
    E_2 = Rank_2 / (Rank_1 + Rank_2)

    r_1_p = r_1 + k * (S_1 - E_1)
    r_2_p = r_2 + k * (S_2 - E_2)

    return r_1_p, r_2_p
