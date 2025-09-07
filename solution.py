import sys; sys.setrecursionlimit(1000000)
from abc import ABC, abstractmethod

Position = tuple[int, int]
X, Y = range(2)


class BaseSolution(ABC):
    def __init__(self, board: 'Board'):
        self.board = board

    @abstractmethod
    def solve(self) -> list[Position]:
        ...


class BacktrackingSolution(BaseSolution):
    def __init__(self, board: 'Board', candidates_func, cost_limit: int=None):
        super().__init__(board)
        self.candidates_func = candidates_func
        self.cost_limit = cost_limit or 1e12
        self.cost = 0

    def solve(self):
        stack = [None]
        while stack:
            target = stack.pop()

            if self.cost >= self.cost_limit:
                break

            if self.board.is_completed():
                break

            if target == -1:
                self.board.undo()
                continue
            elif target:
                self.board.move(target)
                self.cost += 1

            for p in reversed(self.candidates_func()):
                stack.append(-1)
                stack.append(p)

        return self.board.moves if self.board.is_completed() else []


class GreedySolution(BaseSolution):
    def __init__(self, board: 'Board', score_func, k: int=None, cost_limit: int=None):
        super().__init__(board)
        self.score_func = score_func
        self.k = k
        self.cost_limit = cost_limit

    def get_candidates(self):
        candidates = self.board.get_candidates()
        candidates.sort(key=self.score_func, reverse=True)
        return candidates[:self.k] if self.k else candidates

    def solve(self):
        return BacktrackingSolution(self.board, self.get_candidates, self.cost_limit).solve()


class Solution(BaseSolution):
    def solve(self):
        def get_score(p: Position):
            N = self.board.N
            px, py = p
            return abs((px - 0.5 - N/2) / N) + abs((py - 0.5 - N/2) / N)

        return GreedySolution(self.board, get_score, k=3, cost_limit=1000000).solve()


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
