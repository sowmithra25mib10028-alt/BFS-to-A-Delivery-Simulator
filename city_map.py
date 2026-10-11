"""
city_map.py
-----------
Everything about the city lives here: the street layout, which tiles can be
driven on, and how much each tile costs to ride through.

Map legend (used in the text maps and in the printed output):
    .  normal street       cost 1
    #  building / blocked  cannot enter
    ~  congested street    cost 3
    S  shop (rider start)
    D  customer drop-off
"""

from dataclasses import dataclass, field

STREET_COST = {".": 1, "~": 3, "S": 1, "D": 1}
BLOCKED = "#"

# four directions the rider can move (no diagonals, streets only)
STEPS = ((-1, 0), (1, 0), (0, -1), (0, 1))


@dataclass
class CityMap:
    tiles: list                       # list of strings, one per row
    shop: tuple = None
    drops: list = field(default_factory=list)

    @classmethod
    def from_text(cls, text):
        rows = [line for line in text.strip("\n").splitlines()]
        width = len(rows[0])
        if any(len(r) != width for r in rows):
            raise ValueError("every row of the map must be the same length")

        shops, drops = [], []
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch == "S":
                    shops.append((r, c))
                elif ch == "D":
                    drops.append((r, c))
        if len(shops) != 1:
            raise ValueError("map needs exactly one S (shop) tile")
        return cls(tiles=rows, shop=shops[0], drops=drops)

    @property
    def height(self):
        return len(self.tiles)

    @property
    def width(self):
        return len(self.tiles[0])

    def is_open(self, spot):
        r, c = spot
        inside = 0 <= r < self.height and 0 <= c < self.width
        return inside and self.tiles[r][c] != BLOCKED

    def cost_of(self, spot):
        return STREET_COST[self.tiles[spot[0]][spot[1]]]

    def adjacent(self, spot):
        """All open tiles one step away from `spot`."""
        r, c = spot
        for dr, dc in STEPS:
            nxt = (r + dr, c + dc)
            if self.is_open(nxt):
                yield nxt

    def draw(self, route=()):
        """Return the map as text, marking the route with * ."""
        on_route = set(route)
        out = []
        for r, row in enumerate(self.tiles):
            line = ""
            for c, ch in enumerate(row):
                if (r, c) in on_route and ch not in "SD":
                    line += "*"
                else:
                    line += ch
            out.append(line)
        return "\n".join(out)


SAMPLE_CITY = """
S...#......
.##.#.####.
.#..~.#..#.
.#.####.D#.
.#....#...~
.####.#.##.
...D..~..#.
.#######.#.
...~....D..
"""
