def predict(r_1, r_2):
    Rank_1 = pow(10, r_1 / 400)
    Rank_2 = pow(10, r_2 / 400)

    E_1 = Rank_1 / (Rank_1 + Rank_2)
    E_2 = Rank_2 / (Rank_1 + Rank_2)

    return E_1, E_2
