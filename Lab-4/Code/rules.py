SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 1 or abs(ec - sc) != 1:
        return False

    # King moves both directions
    if piece == player + "K":
        return True

    # Normal pieces move forward
    direction = -1 if player == "R" else 1

    return er - sr == direction


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]

    # Destination must be empty
    if board[er][ec] != ".":
        return False

    # Capture must be exactly two diagonal squares
    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False

    # Middle square
    mr = (sr + er) // 2
    mc = (sc + ec) // 2

    middle = board[mr][mc]

    # Must jump over opponent
    if middle == ".":
        return False

    if middle == player or middle == player + "K":
        return False

    # King can capture in either direction
    if piece == player + "K":
        return True

    # Normal piece captures forward
    direction = -1 if player == "R" else 1

    return er - sr == 2 * direction


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"


def has_pieces(board, player):
    for row in board:
        for cell in row:
            if cell == player or cell == player + "K":
                return True

    return False


def has_legal_move(board, player):
    for r in range(SIZE):
        for c in range(SIZE):

            if board[r][c] not in (player, player + "K"):
                continue

            for er in range(SIZE):
                for ec in range(SIZE):

                    if simple_move(
                        board,
                        player,
                        (r, c),
                        (er, ec)
                    ):
                        return True

                    if capture_move(
                        board,
                        player,
                        (r, c),
                        (er, ec)
                    ):
                        return True

    return False


def has_capture(board, player):
    for r in range(SIZE):
        for c in range(SIZE):

            if board[r][c] not in (player, player + "K"):
                continue

            for er in range(SIZE):
                for ec in range(SIZE):

                    if capture_move(
                        board,
                        player,
                        (r, c),
                        (er, ec)
                    ):
                        return True

    return False


def has_piece_capture(board, player, position):
    r, c = position

    for er in range(SIZE):
        for ec in range(SIZE):

            if capture_move(
                board,
                player,
                position,
                (er, ec)
            ):
                return True

    return False