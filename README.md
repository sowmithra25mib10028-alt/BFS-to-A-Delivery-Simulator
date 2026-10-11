# Delivery Route Simulator

A small Python project that sends a delivery rider across a grid-shaped city
and finds the shortest way to each customer using **breadth-first search
(BFS)**. I also added Dijkstra and A* so I could see what happens when some
streets are slower than others.

## Why I built it

I wanted to understand BFS by watching it solve something real instead of
tracing nodes on paper. A delivery rider going from a shop to a door is easy
to picture, and the "fewest blocks" answer is exactly what BFS gives you on a
grid.

## What it does

- Reads the city from a plain text map (or uses the built-in sample).
- Starts the rider at the shop (`S`) and visits every customer (`D`).
- Always heads to the nearest remaining customer next.
- Draws the final route on the map with `*`.
- Prints blocks ridden, street cost, tiles searched and run time.
- Reports any customer that can't be reached instead of crashing.

## Map symbols

| Symbol | Meaning | Cost |
|--------|---------|------|
| `.` | normal street | 1 |
| `~` | congested street | 3 |
| `#` | building, can't enter | - |
| `S` | shop (start) | 1 |
| `D` | customer drop-off | 1 |

## Files

| File | What's in it |
|------|--------------|
| `city_map.py` | the map class, symbols, drawing |
| `route_finders.py` | BFS, Dijkstra and A* |
| `rider.py` | the rider and the multi-stop trip logic |
| `main.py` | command line interface |
| `test_routes.py` | a few quick checks |
| `maps/rush_hour.txt` | tiny map where BFS and Dijkstra disagree |

## How to run

Needs Python 3.8 or newer. No extra packages.

```bash
python main.py                       # BFS on the sample city
python main.py --algo dijkstra       # cheapest route instead of shortest
python main.py --algo astar
python main.py --compare             # all three side by side
python main.py --map maps/rush_hour.txt --compare
python main.py --no-map              # skip the drawing
python test_routes.py                # run the checks
```

You can make your own city by writing a text file where every row is the same
length, with exactly one `S` and as many `D`s as you like.

## Sample result (built-in city)

```
algorithm   blocks    cost  searched
------------------------------------
bfs             23      25        93
dijkstra        23      25        89
astar           23      25        47
```

All three agree here because the congested tiles aren't on the best path, but
A* only has to look at about half as many tiles.

On `maps/rush_hour.txt` they split: BFS rides 4 blocks but pays a cost of 10
through traffic, while Dijkstra and A* ride 8 blocks for a cost of only 8.

## What I learned

- BFS is great when every step costs the same, and wrong the moment it doesn't.
- A* gives the same answer as Dijkstra but searches less, thanks to the
  distance guess.
- Greedy "nearest customer next" is simple but not always the best overall
  order. That would be a good next step (see the report).
