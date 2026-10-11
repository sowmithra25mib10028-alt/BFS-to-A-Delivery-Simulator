"""
main.py
-------
Command line entry point for the delivery route simulator.

Examples
    python main.py
    python main.py --algo dijkstra
    python main.py --compare
    python main.py --map my_city.txt --algo bfs
"""

import argparse
import time

from city_map import CityMap, SAMPLE_CITY
from rider import Rider


def load_city(path):
    if path is None:
        return CityMap.from_text(SAMPLE_CITY)
    with open(path) as fh:
        return CityMap.from_text(fh.read())


def run_one(city, algo, show_map=True):
    started = time.perf_counter()
    report = Rider(city, algo).run_trip()
    elapsed = (time.perf_counter() - started) * 1000

    print(f"=== {algo.upper()} ===")
    print("Delivery order :", report.order)
    print("Blocks ridden  :", report.total_blocks)
    print("Street cost    :", report.total_effort)
    print("Tiles searched :", report.total_visited)
    print(f"Run time       : {elapsed:.2f} ms")
    if report.undeliverable:
        print("Could not reach:", report.undeliverable)
    if show_map:
        print()
        print(city.draw(report.full_route))
    print()
    return report


def compare_all(city):
    rows = []
    for algo in ("bfs", "dijkstra", "astar"):
        rep = Rider(city, algo).run_trip()
        rows.append((algo, rep.total_blocks, rep.total_effort, rep.total_visited))

    print(f"{'algorithm':<10}{'blocks':>8}{'cost':>8}{'searched':>10}")
    print("-" * 36)
    for name, blocks, cost, seen in rows:
        print(f"{name:<10}{blocks:>8}{cost:>8}{seen:>10}")


def main():
    ap = argparse.ArgumentParser(description="Delivery route simulator")
    ap.add_argument("--algo", choices=["bfs", "dijkstra", "astar"], default="bfs")
    ap.add_argument("--map", help="path to a text map file")
    ap.add_argument("--compare", action="store_true",
                    help="run all three algorithms side by side")
    ap.add_argument("--no-map", action="store_true", help="hide the drawn map")
    args = ap.parse_args()

    city = load_city(args.map)
    if args.compare:
        compare_all(city)
    else:
        run_one(city, args.algo, show_map=not args.no_map)


if __name__ == "__main__":
    main()
