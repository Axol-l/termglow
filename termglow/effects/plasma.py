"""Enhanced plasma effect with animated center and richer color mapping."""

import math
from ..engine import rgb


def plasma_effect(dt: float, width: int, height: int) -> list[str]:
    time_val = dt * 1.8
    cx = 2 + math.sin(time_val * 0.4) * 0.8
    cy = 2 + math.cos(time_val * 0.35) * 0.8

    scale_x = 7.5 / width
    scale_y = 5.5 / height

    buffer = []

    for y in range(height):
        row = []
        py = y * scale_y

        for x in range(width):
            px = x * scale_x
            dx = px - cx
            dy = py - cy

            v = math.sin(px * 4.0 + time_val)
            v += math.sin(py * 3.5 + time_val * 0.75)
            v += math.sin((px + py) * 2.3 + time_val * 1.2)
            v += math.sin(math.sqrt(dx * dx + dy * dy) * 3.5 + time_val * 0.55)
            v += math.cos(px * 6.0 - py * 2.0 + time_val * 1.1) * 0.5
            v += math.sin(py * 5.0 - px * 1.5 - time_val * 0.65) * 0.5
            v /= 5.0

            r = int(((math.sin(v * math.pi) + 1) / 2) * 255)
            g = int(((math.sin(v * math.pi + 2.094) + 1) / 2) * 255)
            b = int(((math.sin(v * math.pi + 4.189) + 1) / 2) * 255)

            row.append(f"{rgb(r, g, b)}\u2588")

        buffer.append("".join(row))

    return buffer
