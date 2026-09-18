import time, argparse, heapq
from collections import deque

class GridCity:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, pos):
        r, c = pos
        moves = [(1,0), (-1,0), (0,1), (0,-1)]
        for dr, dc in moves:
            nr, nc = r+dr, c+dc
            if self.in_bounds((nr,nc)) and self.grid[nr][nc] != 1:
                yield (nr,nc)

    def cost(self, pos):
        return self.grid[pos[0]][pos[1]]

def build_path(came, start, goal):
    if goal not in came: return []
    p, cur = [], goal
    while cur is not None:
        p.append(cur)
        cur = came[cur]
    return p[::-1]

def bfs(city):
    q = deque([city.start])
    came = {city.start: None}
    while q:
        cur = q.popleft()
        if cur == city.goal: break
        for n in city.neighbors(cur):
            if n not in came:
                came[n] = cur
                q.append(n)
    return build_path(came, city.start, city.goal), len(came)

def ucs(city):
    pq = [(0, city.start)]
    came, cost_map = {city.start: None}, {city.start: 0}
    while pq:
        cost, cur = heapq.heappop(pq)
        if cur == city.goal: break
        for n in city.neighbors(cur):
            new = cost_map[cur] + city.cost(n)
            if n not in cost_map or new < cost_map[n]:
                cost_map[n] = new
                heapq.heappush(pq,(new,n))
                came[n] = cur
    return build_path(came, city.start, city.goal), cost_map.get(city.goal), len(came)

def astar(city):
    h = lambda a,b: abs(a[0]-b[0]) + abs(a[1]-b[1])
    pq = [(0, city.start)]
    came, cost_map = {city.start: None}, {city.start: 0}
    while pq:
        _, cur = heapq.heappop(pq)
        if cur == city.goal: break
        for n in city.neighbors(cur):
            new = cost_map[cur] + city.cost(n)
            if n not in cost_map or new < cost_map[n]:
                cost_map[n] = new
                f = new + h(n, city.goal)
                heapq.heappush(pq, (f, n))
                came[n] = cur
    return build_path(came, city.start, city.goal), cost_map.get(city.goal), len(came)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", choices=["bfs","ucs","astar"], default="bfs")
    args = parser.parse_args()

    # quick demo grid: 0=free, 1=wall, 2=costlier road
    grid = [
        [0,0,0,0],
        [0,1,1,0],
        [0,0,2,0],
        [0,0,0,0]
    ]

    city = GridCity(grid, (0,0), (3,3))

    t0 = time.time()
    if args.algo == "bfs":
        path, explored = bfs(city)
        cost = len(path) - 1
    elif args.algo == "ucs":
        path, cost, explored = ucs(city)
    else:
        path, cost, explored = astar(city)
    t1 = time.time()

    print("Algorithm:", args.algo.upper())
    print("Path:", path)
    print("Cost:", cost)
    print("Nodes Seen:", explored)
    print("Time:", round(t1-t0, 4), "sec")
