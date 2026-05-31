"""Plasma / water ripple effect using sine wave composition."""

import math
from ..engine import rgb


def plasma_effect(dt: float, width: int, height: int) -> list[str]:
    time_val = dt * 2.0

    scale_x = 8.0 / width
    scale_y = 5.0 / height

    buffer = []

    for y in range(height):
        row = []
        py = y * scale_y

        for x in range(width):
            px = x * scale_x
            v = math.sin(px * 4 + time_val)
            v += math.sin(py * 3 + time_val * 0.7)
            v += math.sin((px + py) * 2 + time_val * 1.3)
            v += math.sin(math.sqrt((px - 2) ** 2 + (py - 2) ** 2) * 3 + time_val * 0.5)
            v /= 4.0

            r = int(((math.sin(v * math.pi) + 1) / 2) * 255)
            g = int(((math.sin(v * math.pi + 2.094) + 1) / 2) * 255)
            b = int(((math.sin(v * math.pi + 4.189) + 1) / 2) * 255)

            row.append(f"{rgb(r, g, b)}\u2588")

        buffer.append("".join(row))

    return buffer
