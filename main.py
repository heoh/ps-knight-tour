from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Button, Footer, Header
from solution import Board, Solution

APP_MAX_N = 20

board: Board = None
sequence_labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

class KnightTourApp(App):
    CSS_PATH = 'main.tcss'

    BINDINGS = [
        Binding('ctrl+c', 'quit', 'Quit', show=True, priority=True),
        Binding('ctrl+z', 'undo', 'Undo', show=True, priority=True),
        Binding('ctrl+y', 'redo', 'Redo', show=True, priority=True),
        Binding('ctrl+r', 'reset', 'Reset', show=True, priority=True),
    ]

    def on_mount(self) -> None:
        self.render_board()

    def compose(self) -> ComposeResult:
        # yield Header()
        yield Footer()
        yield VerticalGroup(
            *[HorizontalGroup(*[Button(' ', id=f'cell_{x}_{y}', classes='cell', flat=True)
                                for x in range(1, board.N+1)])
              for y in range(1, board.N+1)]
        )

    def on_button_pressed(self, event: Button.Pressed):
        _, x, y = event.button.id.split('_')
        x, y = int(x), int(y)

        try:
            board.move((x, y))
        except ValueError:
            pass
        self.render_board()

    def action_undo(self):
        board.undo()
        self.render_board()

    def action_redo(self):
        board.redo()
        self.render_board()

    def action_reset(self):
        board.reset()
        self.render_board()

    def render_board(self):
        for y in range(1, board.N+1):
            for x in range(1, board.N+1):
                p = (x, y)
                button: Button = self.query_one(f'#cell_{x}_{y}')
                if p == board.knight:
                    button.label = '♞'
                    button.disabled = True
                elif board.is_movable(p):
                    button.label = ' '
                    button.disabled = False
                elif board.is_visited(p):
                    button.label = sequence_labels[board[p] % len(sequence_labels)]
                    button.disabled = True
                else:
                    button.label = ' '
                    button.disabled = True


if __name__ == '__main__':
    N = int(input('N: '))
    S = tuple(map(int, input('X Y: ').split()))
    board = Board(N, S)

    moves = Solution(board).solve()

    if N <= APP_MAX_N:
        app = KnightTourApp()
        app.run()
    else:
        for move in (moves or [(-1, -1)]):
            print(*move)
