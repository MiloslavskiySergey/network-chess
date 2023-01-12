"""Move file."""


class Move:

    def __init__(self, initial, final) -> None:
        self.initial = initial
        self.final = final

    def __str__(self) -> str:
        s = ''
        s += f'({self.initial.column}, {self.initial.row})'
        s += f' -> ({self.final.column}, {self.final.row})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
