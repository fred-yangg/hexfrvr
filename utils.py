def indices():
    for row in range(9):
        start = max(0, row - 4)
        end = min(9, row + 5)
        for col in range(start, end):
            yield row, col

def tadd(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]

def piece_hexes(piece, position):
    for hexagon in piece:
        yield tadd(hexagon, position)

def build_line_checks_by_move(piece_types):
    line_checks_by_move = {}

    for piece in piece_types:
        for position in indices():
            checks = []
            hexes = list(piece_hexes(piece, position))
            rows = set(map(lambda x: x[0], hexes))
            cols = set(map(lambda x: x[1], hexes))
            diags = set(map(lambda x: x[1] - x[0], hexes))

            for row in rows:
                start = max(0, row - 4)
                end = min(9, row + 5)
                checks.append({(row, col) for col in range(start, end)})

            for col in cols:
                start = max(0, col - 4)
                end = min(9, col + 5)
                checks.append({(row, col) for row in range(start, end)})

            for diag in diags:
                diag_mag = abs(diag)
                if diag < 0:
                    start = (diag_mag, 0)
                else:
                    start = (0, diag_mag)
                size = 9 - diag_mag
                checks.append({(start[0] + i, start[1] + i) for i in range(size)})

            line_checks_by_move[(piece, position)] = checks

    return line_checks_by_move

def build_in_bounds_moves_by_piece(piece_types):
    positions = set(indices())
    in_bounds_moves_by_piece = {piece: set() for piece in piece_types}

    for piece in piece_types:
        for position in positions:
            valid = True

            for hexagon in piece_hexes(piece, position):
                if hexagon not in positions:
                    valid = False
                    break

            if valid:
                in_bounds_moves_by_piece[piece].add(position)

    return in_bounds_moves_by_piece