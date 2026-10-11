"""
rider.py
--------
The delivery rider. Starts at the shop, then repeatedly heads to the
nearest remaining customer (nearest = shortest route by the chosen finder).
"""

from dataclasses import dataclass, field
from route_finders import FINDERS


@dataclass
class TripReport:
    algorithm: str
    legs: list = field(default_factory=list)      # one RouteResult per drop
    order: list = field(default_factory=list)     # drop-offs in visit order
    undeliverable: list = field(default_factory=list)

    @property
    def total_blocks(self):
        return sum(leg.blocks for leg in self.legs)

    @property
    def total_effort(self):
        return sum(leg.effort for leg in self.legs)

    @property
    def total_visited(self):
        return sum(leg.visited for leg in self.legs)

    @property
    def full_route(self):
        tiles = []
        for leg in self.legs:
            tiles.extend(leg.path)
        return tiles


class Rider:
    def __init__(self, city, algorithm="bfs"):
        if algorithm not in FINDERS:
            raise ValueError(f"unknown algorithm: {algorithm}")
        self.city = city
        self.algorithm = algorithm
        self.find = FINDERS[algorithm]

    def run_trip(self, drops=None):
        todo = list(drops if drops is not None else self.city.drops)
        here = self.city.shop
        report = TripReport(self.algorithm)

        while todo:
            options = [(self.find(self.city, here, d), d) for d in todo]
            reachable = [(res, d) for res, d in options if res.path]

            # anything with no route at all gets reported, not silently lost
            for res, d in options:
                if not res.path:
                    report.undeliverable.append(d)
                    todo.remove(d)
            if not reachable:
                break

            # pick the closest by the finder's own measure
            key = (lambda x: x[0].blocks) if self.algorithm == "bfs" \
                else (lambda x: x[0].effort)
            best, target = min(reachable, key=key)

            report.legs.append(best)
            report.order.append(target)
            here = target
            todo.remove(target)

        return report
