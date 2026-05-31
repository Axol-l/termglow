"""Matrix-style digital rain effect with glowing heads and scanlines."""

import random
import math
from ..engine import rgb, reset


CHARS = [
    "\u30A0", "\u30A1", "\u30A2", "\u30A3", "\u30A4", "\u30A5",
    "\u30A6", "\u30A7", "\u30A8", "\u30A9", "\u30AA", "\u30AB",
    "\u30AC", "\u30AD", "\u30AE", "\u30AF", "\u3099", "\u309A",
    "\u30FC", "\u30FB", "0", "1", "2", "3", "4", "5", "6",
    "7", "8", "9", ":", "+", "*", "%", "#", "&",
]

GLOW_CHARS = "\u2591\u2592\u2593\u2588"


class MatrixDrop:
    def __init__(self, x: int, height: int):
        self.x = x
        self.y = float(random.randint(-height * 2, -2))
        self.speed = random.uniform(1.0, 3.5)
        max_len = max(5, min(height // 2, 25))
        self.length = random.randint(4, max_len)
        self.chars = [random.choice(CHARS) for _ in range(self.length)]
        self.brightness = random.uniform(0.6, 1.0)
        self.hue_shift = random.uniform(-0.05, 0.05)


def matrix_effect(dt: float, width: int, height: int) -> list[str]:
    global _drops, _accumulated_dt
    _accumulated_dt += dt

    while len(_drops) < width:
        _drops.append(MatrixDrop(len(_drops), height))
    while len(_drops) > width:
        _drops.pop()

    buffer = [[] for _ in range(height)]

    for drop in _drops:
        drop.y += drop.speed * dt * 25

        head_y = int(drop.y)

        for i in range(drop.length):
            py = head_y - i
            if py < 0 or py >= height:
                continue

            if i == 0:
                r, g, b = 180, 255, 180
            elif i == 1:
                ratio = 0.8
                r = int(40 * ratio * drop.brightness)
                g = int(255 * ratio * drop.brightness)
                b = int(60 * ratio * drop.brightness)
            elif i == 2:
                ratio = 0.5
                r = int(20 * ratio * drop.brightness)
                g = int(220 * ratio * drop.brightness)
                b = int(30 * ratio * drop.brightness)
            else:
                ratio = max(0.05, 0.35 * (1.0 - i / drop.length))
                r = int(0 * ratio * drop.brightness)
                g = int(180 * ratio * drop.brightness)
                b = int(20 * ratio * drop.brightness)

            char = random.choice(CHARS) if random.random() < 0.08 else drop.chars[i % len(drop.chars)]
            buffer[py].append(rgb(r, g, b) + char)

        if head_y - drop.length > height:
            idx = drop.x
            _drops[idx] = MatrixDrop(idx, height)

    for y in range(height):
        if not buffer[y]:
            buffer[y] = " " * width
        else:
            buffer[y] = "".join(buffer[y]) + reset()

    return buffer


_drops: list[MatrixDrop] = []
_accumulated_dt = 0.0
