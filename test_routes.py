"""Small sanity checks. Run with:  python test_routes.py"""

from city_map import CityMap
from route_finders import bfs_route, cheapest_route, astar_route
from rider import Rider


def test_open_street():
    city = CityMap.from_text("S..D")
    assert bfs_route(city, (0, 0), (0, 3)).blocks == 3


def test_blocked_goal():
    city = CityMap.from_text("S#D")
    assert bfs_route(city, (0, 0), (0, 2)).path == []


def test_bfs_vs_dijkstra_on_congestion():
    city = CityMap.from_text("S~~~D\n.###.\n.....")
    short = bfs_route(city, (0, 0), (0, 4))
    cheap = cheapest_route(city, (0, 0), (0, 4))
    assert short.blocks == 4 and short.effort == 10
    assert cheap.blocks == 8 and cheap.effort == 8


def test_astar_matches_dijkstra():
    city = CityMap.from_text("S~~~D\n.###.\n.....")
    a = astar_route(city, (0, 0), (0, 4))
    d = cheapest_route(city, (0, 0), (0, 4))
    assert a.effort == d.effort


def test_unreachable_drop_is_reported():
    city = CityMap.from_text("S.#D")
    report = Rider(city, "bfs").run_trip()
    assert report.undeliverable == [(0, 3)]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok  ", name)
