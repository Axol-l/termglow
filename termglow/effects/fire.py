"""Doom-style fire effect using cellular automata."""

import random
import math
from ..engine import rgb


class Fire:
    """Procedural fire effect."""

    def __init__(self):
        self._buffer: list[list[float]] = []
        self._palette: list[tuple[int, int, int]] = []

    def _gen_palette(self, size: int = 256):
        palette = []
        for i in range(size):
            t = i / (size - 1)
            r = int(min(255, t * 3 * 255))
            g = int(min(255, max(0, (t - 0.33) * 3 * 255)))
            b = int(min(255, max(0, (t - 0.66) * 3 * 255)))
            palette.append((r, g, b))
        self._palette = palette

    def render(self, dt: float, width: int, height: int) -> list[str]:
        fire_h = height + 6
        if not self._palette:
            self._gen_palette()

        if len(self._buffer) != fire_h or (self._buffer and len(self._buffer[0]) != width):
            self._buffer = [[0.0] * width for _ in range(fire_h)]

        buf = self._buffer

        for x in range(width):
            if random.random() < 0.4:
                buf[fire_h - 1][x] = 1.0
            else:
                buf[fire_h - 1][x] = buf[fire_h - 1][x] * 0.85

        for y in range(fire_h - 1):
            for x in range(1, width - 1):
                s = buf[(y + 1) % fire_h][x]
                s += buf[(y + 1) % fire_h][(x - 1) % width]
                s += buf[(y + 1) % fire_h][(x + 1) % width]
                s += buf[(y + 2) % fire_h][x]
                r = random.uniform(0.9, 1.0)
                buf[y][x] = (s / 4.1) * r * 1.02

        result = []
        pal_size = len(self._palette) - 1
        for y in range(min(height, fire_h - 1)):
            row = []
            for x in range(width):
                idx = min(pal_size, int(buf[y][x] * pal_size))
                r, g, b = self._palette[idx]
                row.append(f"{rgb(r, g, b)}\u2588")
            result.append("".join(row))

        return result


_fire = Fire()


def fire_effect(dt: float, width: int, height: int) -> list[str]:
    return _fire.render(dt, width, height)
