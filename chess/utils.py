
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8]


def chess_notation(move):
    from_, to = move
    int_to_letter = dict(zip(range(8), LETTERS))
    cn_from = f"{int_to_letter[from_[1]]}{8 - from_[0]}"
    cn_to = f"{int_to_letter[to[1]]}{8 - to[0]}"
    return cn_from, cn_to
