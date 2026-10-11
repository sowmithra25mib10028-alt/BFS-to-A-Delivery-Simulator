"""
route_finders.py
----------------
Three ways of getting the rider from one tile to another.

  * bfs_route      - fewest blocks (ignores how slow a street is)
  * cheapest_route - Dijkstra / uniform cost, minimises total street cost
  * astar_route    - same answer as cheapest_route but explores fewer tiles

Each finder returns a RouteResult so the simulator can compare them easily.
"""

import heapq
from collections import deque
from dataclasses import dataclass


@dataclass
class RouteResult:
    path: list        # tiles from start to goal, empty if unreachable
    blocks: int       # number of moves
    effort: int       # total street cost along the path
    visited: int      # how many tiles the search looked at


def _rebuild(parents, goal):
    if goal not in parents:
        return []
    trail = []
    spot = goal
    while spot is not None:
        trail.append(spot)
        spot = parents[spot]
    trail.reverse()
    return trail


def _wrap(city, parents, goal):
    path = _rebuild(parents, goal)
    if not path:
        return RouteResult([], 0, 0, len(parents))
    effort = sum(city.cost_of(p) for p in path[1:])
    return RouteResult(path, len(path) - 1, effort, len(parents))


def bfs_route(city, start, goal):
    parents = {start: None}
    waiting = deque([start])

    while waiting:
        here = waiting.popleft()
        if here == goal:
            break
        for nxt in city.adjacent(here):
            if nxt not in parents:
                parents[nxt] = here
                waiting.append(nxt)

    return _wrap(city, parents, goal)


def cheapest_route(city, start, goal):
    parents = {start: None}
    best = {start: 0}
    heap = [(0, start)]

    while heap:
        spent, here = heapq.heappop(heap)
        if spent > best[here]:
            continue                      # stale entry, skip it
        if here == goal:
            break
        for nxt in city.adjacent(here):
            total = spent + city.cost_of(nxt)
            if total < best.get(nxt, float("inf")):
                best[nxt] = total
                parents[nxt] = here
                heapq.heappush(heap, (total, nxt))

    return _wrap(city, parents, goal)


def _manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_route(city, start, goal):
    parents = {start: None}
    best = {start: 0}
    heap = [(_manhattan(start, goal), 0, start)]

    while heap:
        _, spent, here = heapq.heappop(heap)
        if spent > best[here]:
            continue
        if here == goal:
            break
        for nxt in city.adjacent(here):
            total = spent + city.cost_of(nxt)
            if total < best.get(nxt, float("inf")):
                best[nxt] = total
                parents[nxt] = here
                guess = total + _manhattan(nxt, goal)
                heapq.heappush(heap, (guess, total, nxt))

    return _wrap(city, parents, goal)


FINDERS = {
    "bfs": bfs_route,
    "dijkstra": cheapest_route,
    "astar": astar_route,
}
