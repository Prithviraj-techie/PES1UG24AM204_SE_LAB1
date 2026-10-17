from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    has_pieces,
    has_legal_move,
    has_capture,
    has_piece_capture
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def run(self):
        print("Checkers — move: sr sc er ec")

        while True:
            self.print_board()

            raw = input(f"{self.player}> ").strip().lower().split()

            # Quit
            if raw == ["q"]:
                return

            # Four coordinates required
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            # Convert coordinates to integers
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            # Check board boundaries
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue

            # Check that the starting square contains the current
            # player's piece
            if self.board[sr][sc] not in (
                self.player,
                self.player + "K"
            ):
                print("That is not your piece.")
                continue

            start = (sr, sc)
            end = (er, ec)

            # --------------------------------------------------
            # MOVE VALIDATION
            # --------------------------------------------------

            # If any capture is available, capturing is compulsory.
            if has_capture(self.board, self.player):

                if capture_move(
                    self.board,
                    self.player,
                    start,
                    end
                ):
                    move_piece(self.board, start, end)
                    print(f"Capture: {start} -> {end}")

                else:
                    print(
                        "You must capture when a capture is available."
                    )
                    continue

            # If no capture exists, allow a normal move.
            elif simple_move(
                self.board,
                self.player,
                start,
                end
            ):
                move_piece(self.board, start, end)
                print(f"Move accepted: {start} -> {end}")

            else:
                print("Invalid move.")
                continue

            # --------------------------------------------------
            # PROMOTION
            # --------------------------------------------------

            promote(self.board)

            # --------------------------------------------------
            # MULTIPLE CAPTURE
            # --------------------------------------------------

            # If the move was a capture and the same piece can
            # capture again, the same player continues.
            if (
                abs(end[0] - start[0]) == 2
                and abs(end[1] - start[1]) == 2
                and has_piece_capture(
                    self.board,
                    self.player,
                    end
                )
            ):
               print(
                        f"Another capture is available for {end}. "
                        f"Continue with the same piece."
                    )
            continue

            # --------------------------------------------------
            # SWITCH PLAYER
            # --------------------------------------------------

            self.player = "B" if self.player == "R" else "R"
            print(f"Next turn: {self.player}")
            # --------------------------------------------------
            # WIN CONDITION: NO PIECES
            # --------------------------------------------------

            if not has_pieces(
                self.board,
                self.player
            ):
                winner = "B" if self.player == "R" else "R"

                self.print_board()

                print(
                    f"{winner} wins! "
                    f"{self.player} has no pieces."
                )

                return

            # --------------------------------------------------
            # WIN CONDITION: NO LEGAL MOVES
            # --------------------------------------------------

            if not has_legal_move(
                self.board,
                self.player
            ):
                winner = "B" if self.player == "R" else "R"

                self.print_board()

                print(
                    f"{winner} wins! "
                    f"{self.player} has no legal moves."
                )

                return