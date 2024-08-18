from typing import Self
from math import sin, cos, pi

type PlotMode = int

pixel_characters = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
square_pixel_map = {
    " ": "  ",
    "▘": "▀ ",
    "▝": " ▀",
    "▀": "▀▀",
    "▖": "▄ ",
    "▌": "█ ",
    "▞": "▄▀",
    "▛": "█▀",
    "▗": " ▄",
    "▚": "▀▄",
    "▐": " █",
    "▜": "▀█",
    "▄": "▄▄",
    "▙": "█▄",
    "▟": "▄█",
    "█": "██",
}


class BlockelplotException(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return f"Blockelplot Exception: {self.msg}"


class _Mode:
    @property
    def write(self) -> PlotMode:
        """Draws pixels on screen."""
        return 1

    @property
    def toggle(self) -> PlotMode:
        """Toggles pixels on screen."""
        return 0

    @property
    def remove(self) -> PlotMode:
        """Removes pixels on screen."""
        return -1


Mode = _Mode()


class Screen:
    def __init__(
        self,
        height_in_pixels: int,
        width_in_pixels: int,
        adjust_aspect=False,
    ) -> None:
        self.height_in_pixels = height_in_pixels
        self.width_in_pixels = width_in_pixels

        self._adjust_aspect = adjust_aspect
        rows = height_in_pixels // 2 + height_in_pixels % 2
        columns = width_in_pixels // 2 + width_in_pixels % 2
        self.data = [[0 for _ in range(columns)] for _ in range(rows)]

    def __str__(self) -> str:
        rows = ["".join(pixel_characters[i] for i in cs) for cs in self.data]
        if self._adjust_aspect:
            rows = ["".join(square_pixel_map[pixel] for pixel in row) for row in rows]
        return "\n".join(rows)

    def __repr__(self) -> str:
        return str(self)

    def cell_characters(self) -> list[list[str]]:
        """
        The individual screen characters.
        """
        return [[pixel_characters[i] for i in cs] for cs in self.data]

    def clear(self) -> Self:
        """
        Clears the screen.
        """
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                self.data[r][c] = 0

        return self

    def _seek_pixel(
        self,
        row: int,
        column: int,
        wrap: bool,
    ) -> tuple[int, int, int]:
        if wrap:
            row %= self.height_in_pixels
            column %= self.width_in_pixels
        r, dr = row // 2, row % 2
        c, dc = column // 2, column % 2
        bit = dr * 2 + dc
        return r, c, bit

    def pixel(
        self,
        row: int,
        column: int,
        wrap=False,
        mode=Mode.write,
    ) -> Self:
        """
        Draws a pixel at (row, column).
        """
        r, c, bit = self._seek_pixel(row, column, wrap)
        if 0 <= r < len(self.data) and 0 <= c < len(self.data[0]):
            xor_data, or_data = False, False
            match mode:
                case Mode.write:
                    or_data = True
                case Mode.remove:
                    xor_data, or_data = True, True
                case Mode.toggle:
                    xor_data = True
            if or_data:
                self.data[r][c] |= 1 << bit
            if xor_data:
                self.data[r][c] ^= 1 << bit

        return self

    def is_set(self, row: int, column: int, wrap=False) -> bool:
        """
        Whether the pixel at (row, column) is set.
        """
        r, c, bit = self._seek_pixel(row, column, wrap)
        if 0 <= r < len(self.data) and 0 <= c < len(self.data[0]):
            return self.data[r][c] & (1 << bit) > 0
        raise BlockelplotException(
            f"Point row: {r} column {c} out of bounds with no wrap."
        )

    def line(
        self,
        r0: int,
        c0: int,
        r1: int,
        c1: int,
        wrap=False,
        mode=Mode.write,
    ) -> Self:
        """
        Draws a line from (r0, c0) to (r1, c1) (using Bresenham's algorithm).
        """
        dx = abs(r1 - r0)
        sx = 1 if r0 < r1 else -1
        dy = -abs(c1 - c0)
        sy = 1 if c0 < c1 else -1
        error = dx + dy

        while True:
            self.pixel(r0, c0, wrap, mode)
            if r0 == r1 and c0 == c1:
                break
            e = 2 * error
            if e >= dy:
                if r0 == r1:
                    break
                error += dy
                r0 += sx
            if e <= dx:
                if c0 == c1:
                    break
                error += dx
                c0 += sy

        return self

    def circle(
        self,
        row: int,
        column: int,
        radius: int,
        wrap=False,
        mode=Mode.write,
    ) -> Self:
        """
        Draws a circle with radius centered at row, column (using Bresenham's algorithm).
        """
        r, c, e = 0, -radius, 2 - 2 * radius
        while c < 0:
            self.pixel(row + r, column - c, wrap, mode)
            self.pixel(row - c, column - r, wrap, mode)
            self.pixel(row - r, column + c, wrap, mode)
            self.pixel(row + c, column + r, wrap, mode)
            radius = e
            if radius <= r:
                r += 1
                e += r * 2 + 1
            if radius > c or e > r:
                c += 1
                e += c * 2 + 1

        return self

    def rectangle(
        self,
        row: int,
        column: int,
        height: int,
        width: int,
        wrap=False,
        mode=Mode.write,
    ) -> Self:
        """
        Draws a rectangle with top left corner at (row, column).
        """
        r0, c0 = row, column
        r1, c1 = r0 + height, c0 + width
        self.line(r0, c0, r1, c0, wrap, mode)
        self.line(r1, c0, r1, c1, wrap, mode)
        self.line(r1, c1, r0, c1, wrap, mode)
        self.line(r0, c1, r0, c0, wrap, mode)

        return self

    def polygon(
        self,
        row: int,
        column: int,
        radius: float,
        sides: int,
        rotation=0.0,
        wrap=False,
        mode=Mode.write,
    ) -> Self:
        """
        Draws a regular polygon with center (row, column).
        """

        def theta(index: int) -> float:
            return rotation + index * 2 * pi / sides

        def to_row(index: int) -> int:
            return row + round(radius * sin(theta(index)))

        def to_column(index: int) -> int:
            return column + round(radius * cos(theta(index)))

        for index in range(sides):
            self.line(
                to_row(index),
                to_column(index),
                to_row(index + 1),
                to_column(index + 1),
                wrap,
                mode,
            )

        return self

    def peek(
        self,
        row: int,
        column: int,
        bits=8,
        wrap=False,
        inverse=False,
    ) -> int:
        """
        Interprets the pixels starting at row as bits comprising an integer.
        """
        result = 0
        for i in range(bits):
            result <<= 1
            if inverse:
                if not self.is_set(row, column + i, wrap):
                    result += 1
            else:
                if self.is_set(row, column + i, wrap):
                    result += 1

        return result

    def poke(
        self,
        row: int,
        column: int,
        datum: int,
        bits=8,
        wrap=False,
        inverse=False,
    ) -> Self:
        """
        Writes the bits comprising an integer to pixels starting at row, column.
        """
        for i in range(bits):
            if not inverse:
                mode = Mode.write if (1 << (bits - i - 1)) & datum > 0 else Mode.remove
            else:
                mode = Mode.remove if (1 << (bits - i - 1)) & datum > 0 else Mode.write
            self.pixel(row, column + i, wrap, mode)

        return self

    def sprite(
        self,
        row: int,
        column: int,
        sprite_data: list[int],
        bits=8,
        wrap=False,
        inverse=False,
    ) -> Self:
        """
        Draws a sprite with top left corner at row, column.
        """
        for i, datum in enumerate(sprite_data):
            self.poke(
                row + i,
                column,
                datum,
                bits,
                wrap,
                inverse,
            )

        return self
