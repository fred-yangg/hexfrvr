def indices():
    for row in range(9):
        start = max(0, row - 4)
        end = min(9, row + 5)
        for col in range(start, end):
            yield row, col

def piece_hexes(piece, position):
    pos_row, pos_col = position
    for row, col in piece:
        yield pos_row + row, pos_col + col

def build_piece_checks(piece_types):
    piece_checks = {}
    for piece in piece_types:
        for position in indices():
            checks = []
            hexes = piece_hexes(piece, position)
            rows = set(map(lambda x: x[0], hexes))
            cols = set(map(lambda x: x[1], hexes))
            diags = set(map(lambda x: x[0] - x[1], hexes))

            for row in rows:
                start = max(0, row - 4)
                end = min(9, row + 5)
                checks.append([(row, col) for col in range(start, end)])

            for col in cols:
                start = max(0, col - 4)
                end = min(9, col + 5)
                checks.append([(row, col) for row in range(start, end)])

            for diag in diags:
                diag_mag = abs(diag)
                if diag < 0:
                    start = (0, diag_mag)
                else:
                    start = (diag_mag, 0)
                size = 9 - diag_mag
                checks.append([(start[0] + i, start[1] + i) for i in range(size)])

            piece_checks[(piece, position)] = checks