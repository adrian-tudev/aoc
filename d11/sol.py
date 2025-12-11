from collections import defaultdict
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

from parser import Part, parse_part, sample # type: ignore 

class Graph:
  def __init__(self):
    self.graph = defaultdict(list)

  def add_edge(self, u, v):
    self.graph[u].append(v)

  def dfs_sort(self, v, visited, stack):
    visited.add(v)
    for nbr in self.graph[v]:
      if nbr not in visited:
        self.dfs_sort(nbr, visited, stack)
    stack.append(v)

  def topo_sort(self):
    visited = set()
    stack = []

    all_nodes = set(self.graph.keys())
    for adj in self.graph.values():
      all_nodes.update(adj)

    for node in all_nodes:
      if node not in visited:
        self.dfs_sort(node, visited, stack)

    return list(reversed(stack))

  def count_paths(self, start, end) -> int:
    order = self.topo_sort()
    dp = [0 for _ in range(len(order))]

    start_idx = order.index(start)
    dp[start_idx] = 1

    end_idx = order.index(end)
    for i in range(start_idx, len(order)):
      if i == end_idx: break
      for child in self.graph[order[i]]: 
        dp[order.index(child)] += dp[i]

    return dp[end_idx]

  def __str__(self) -> str:
    return str(self.graph)

def p1(g: Graph, sample: bool) -> int:
  return g.count_paths("you", "out")

"""
get the order FFT and DAC appear in and find number of paths between
SVR -> FFT/DAC -> DAC/FFT -> OUT
"""
def p2(g: Graph, sample: bool) -> int:
  ans: int = 1

  topo = g.topo_sort()
  visiting_order = ["svr"]
  for node in topo:
    if node == "dac" or node == "fft":
      visiting_order.append(node)
  visiting_order.append("out")

  for i in range(1, len(visiting_order)):
    ans *= g.count_paths(visiting_order[i - 1], visiting_order[i])

  return ans

def main():
  ex = sample()
  part = parse_part()
  contents: list[str] | None = None
  file = "sample.txt" if ex else "in.txt"
  if part == Part.TWO and ex:
    file = "sample2.txt"
  with open(file, "r") as f:
    contents = f.read().splitlines()
  assert contents != None

  g: Graph = Graph()
  for line in contents:
    devices = line.split()
    u = devices[0][:-1]
    for i in range(1, len(devices)):
      g.add_edge(u, devices[i])
  g.graph["out"] = []

  ans = -1
  if part == Part.ONE:   ans = p1(g, sample=ex)
  elif part == Part.TWO: ans = p2(g, sample=ex)
  print(f"ans: {ans}")

if __name__ == "__main__":
  main()

