Position = tuple[int, int]
X, Y = range(2)

class Solution:
    def __init__(self, board: 'Board'):
        self.board = board

    def solve(self):
        self.dfs()
        return self.board.moves[1:] if self.board.is_completed() else []

    def dfs(self):
        if self.board.is_completed():
            return True
        candidates = self.board.get_candidates()
        for p in candidates:
            self.board.move(p)
            if self.dfs():
                return True
            self.board.undo()
        return False


########################################
# Board
########################################
class Board:
    KNIGHT_MOVES = [          (-1, -2),         ( 1, -2),
                    (-2, -1),                             ( 2, -1),
    #                                     ♞
                    (-2,  1),                             ( 2,  1),
                              (-1,  2),         ( 1,  2)           ]

    def __init__(self, N: int, start: Position):
        self.N = N
        self.moves: list[Position] = [start]
        self.cells: dict[Position, int] = {start: 1}
        self.redo_moves: list[Position] = []

    def reset(self):
        start = self.moves[0]
        self.moves = [start]
        self.cells = {start: 1}
        self.redo_moves = []

    def copy(self):
        board = Board(self.N, self.moves[0])
        board.N = self.N
        board.moves = self.moves.copy()
        board.cells = self.cells.copy()
        board.redo_moves = self.redo_moves.copy()
        return board

    def __getitem__(self, position: Position):
        return self.cells.get(position)

    @property
    def knight(self):
        return self.moves[-1]

    def move(self, target: Position):
        if not self.is_movable(target):
            raise ValueError()
        self.cells[target] = self.cells[self.knight] + 1
        self.moves.append(target)
        self.redo_moves.clear()

    def undo(self):
        if len(self.moves) > 1:
            move = self.moves.pop()
            self.cells.pop(move)
            self.redo_moves.append(move)

    def redo(self):
        if self.redo_moves:
            move = self.redo_moves.pop()
            self.cells[move] = self.cells[self.knight] + 1
            self.moves.append(move)

    def contains(self, p: Position):
        return 1 <= p[X] <= self.N and 1 <= p[Y] <= self.N

    def is_movable(self, p: Position):
        s = self.knight
        return (self.contains(p) and
                not self.is_visited(p) and
                abs((p[X]-s[X]) * (p[Y]-s[Y])) == 2)

    def is_visited(self, p: Position):
        return p in self.cells

    def get_candidates(self) -> list[Position]:
        movables = []
        sx, sy = self.knight
        for dx, dy in self.KNIGHT_MOVES:
            p = (sx+dx, sy+dy)
            if self.contains(p) and not self.is_visited(p):
                movables.append(p)
        return movables

    def is_completed(self):
        return self.cells[self.knight] == self.N**2


if __name__ == '__main__':
    N = int(input())
    S = tuple(map(int, input().split()))
    board = Board(N, S)

    moves = Solution(board).solve()
    for move in (moves or [(-1, -1)]):
        print(*move)
