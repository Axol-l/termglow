"""Matrix-style digital rain effect with color cycling."""

import random
import math
from ..engine import rgb, reset


CHARS = [
    "\u30A0", "\u30A1", "\u30A2", "\u30A3", "\u30A4", "\u30A5", "\u30A6",
    "\u30A7", "\u30A8", "\u30A9", "\u30AA", "\u30AB", "\u30AC", "\u30AD",
    "\u30AE", "\u30AF", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ":", ";", "+", "*", "%", "#", "$", "@", "&",
]


class Matrix:
    """Matrix digital rain effect."""

    def __init__(self):
        self.columns: list[dict] = []

    def render(self, dt: float, width: int, height: int) -> list[str]:
        while len(self.columns) < width:
            self.columns.append(self._new_drop(height))
        while len(self.columns) > width:
            self.columns.pop()

        buffer = ["" for _ in range(height)]

        for x, col in enumerate(self.columns):
            y = int(col["y"])
            speed = col["speed"]
            col["y"] += speed * dt * 30

            for i in range(col["length"]):
                py = y - i
                if 0 <= py < height:
                    char = col["chars"][i % len(col["chars"])]
                    alpha = 1.0 - (i / col["length"])
                    g = int(180 + 75 * alpha)
                    r = int(40 * alpha)
                    b = int(80 * alpha)
                    color = rgb(r, g, b)
                    buffer[py] += color + char + reset()

            if y - col["length"] > height:
                self.columns[x] = self._new_drop(height)

        return buffer

    def _new_drop(self, height: int) -> dict:
        max_len = min(height // 3, 20)
        length = random.randint(6, max(max_len, 8))
        return {
            "y": float(random.randint(-height, -5)),
            "speed": random.uniform(1.5, 4.5),
            "length": length,
            "chars": [random.choice(CHARS) for _ in range(length)],
        }


def matrix_effect(dt: float, width: int, height: int) -> list[str]:
    """Render function for matrix effect."""
    return _matrix.render(dt, width, height)


_matrix = Matrix()
