from functools import cache
import importlib.util
from importlib.machinery import ModuleSpec
import sys
from pathlib import Path
from types import ModuleType

parser_path: Path = Path(__file__).resolve().parents[2] / "parser.py"
spec: ModuleSpec | None = importlib.util.spec_from_file_location("parser", parser_path)
if spec is None: raise ImportError(f"Could not load spec for parser module at {parser_path}")
parser: ModuleType = importlib.util.module_from_spec(spec)
sys.modules["parser"] = parser  
spec.loader.exec_module(parser)  # type: ignore

from parser import Part, parse_part # type: ignore 
from parser import sample # type: ignore
from collections import defaultdict

type Point = tuple[int, int, int]

def dist(a: Point, b: Point) -> int:
  return (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2

def p1(points: list[Point], sample: bool = True) -> int:
  dists: dict[tuple[Point, Point], int] = dict()
  for i in range(len(points) - 1):
    for j in range(i + 1, len(points)):
      dists[(points[i], points[j])] = dist(points[i], points[j])

  dists = dict(sorted(dists.items(), key=lambda item: item[1]))

  # construct a graph and then get sizes of the subgraphs
  g: dict[Point, list[Point]] = defaultdict(list)

  breakpoint = 10 if sample else 1000
  for i, pair in enumerate(dists):
    if i == breakpoint: break

    g[pair[0]].append(pair[1])
    g[pair[1]].append(pair[0])


  visited: dict[Point, bool] = defaultdict(bool)

  # count number of nodes in subgraph
  def dfs(v: Point) -> int:
    visited[v] = True
    sz = 1
    for neighbor in g[v]:
      if not visited[neighbor]:
        sz += dfs(neighbor)
    return sz

  subgraph_sizes: list[int] = []
  for point in points:
    if not visited[point]:
      subgraph_sizes.append(dfs(point))

  subgraph_sizes.sort()

  return subgraph_sizes[-1] * subgraph_sizes[-2] * subgraph_sizes[-3]

def p2(points: list[Point], sample: bool = True):
  ans: int = 0
  dists: dict[tuple[Point, Point], int] = dict()
  for i in range(len(points) - 1):
    for j in range(i + 1, len(points)):
      dists[(points[i], points[j])] = dist(points[i], points[j])

  dists = dict(sorted(dists.items(), key=lambda item: item[1]))

  # dumb solution: binary search untill we find the wanted moment
  l = 0
  r = len(dists) - 1
  breakpoint: int = -1
  while l <= r:
    breakpoint = (l + r) // 2
    # construct a graph and then get sizes of the subgraphs
    g: dict[Point, list[Point]] = defaultdict(list)
    for i, pair in enumerate(dists):
      if i == breakpoint: break
      g[pair[0]].append(pair[1])
      g[pair[1]].append(pair[0])

    visited: dict[Point, bool] = defaultdict(bool)

    # count number of nodes in subgraph
    def dfs(v: Point) -> int:
      visited[v] = True
      sz = 1
      for neighbor in g[v]:
        if not visited[neighbor]:
          sz += dfs(neighbor)
      return sz

    subgraph_sizes: list[int] = []
    for point in points:
      if not visited[point]:
        subgraph_sizes.append(dfs(point))

    components = len(subgraph_sizes)

    if components > 1:
      l = breakpoint + 1
    elif components == 1:
      r = breakpoint - 1

  for i, pair in enumerate(dists):
    if i == breakpoint - 1: # breakpoint minus one by trial and error, seems to work
      ans = pair[0][0] * pair[1][0]
      print(f"from: {pair[0][0]} and {pair[1][0]}")
      break

  return ans

def main():
  sys.setrecursionlimit(10**6)
  ex = sample()
  contents: list[str] | None = None
  file = "sample.txt" if ex else "in.txt"
  part = parse_part()
  with open(file, "r") as f:
    contents = f.read().splitlines()

  points: list[Point] = []
  for line in contents:
    l: list[str] = line.split(',')
    x = int(l[0]); y = int(l[1]); z = int(l[2])
    points.append((x, y, z))

  ans = -1
  if part == Part.ONE:   ans = p1(points, sample=ex)
  elif part == Part.TWO: ans = p2(points, sample=ex)
  print(ans)

if __name__ == "__main__":
  main()

