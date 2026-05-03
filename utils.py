def indices():
    for row in range(9):
        start = max(0, row - 4)
        end = min(9, row + 5)
        for col in range(start, end):
            yield row, col
