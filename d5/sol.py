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

def sol(part: Part, rngs: list[tuple[int, int]], queries: list[int]) -> int:
  ans: int = 0

  # PART ONE
  if part == Part.ONE:
    for query in queries:
      for (l, r) in rngs:
        if query >= l and query <= r:
          ans += 1
          break

  # PART TWO
  elif part == Part.TWO:
    rngs.sort()
    i = 0
    while i < len(rngs):
      j = i + 1
      mx = rngs[i][1]
      while j < len(rngs) and rngs[j - 1][1] >= rngs[j][0]:
        mx = max(rngs[j][1], mx)
        j += 1
      ans += mx - rngs[i][0] + 1
      i = j

  return ans

def main():
  contents: list[str] | None = None
  #with open("sample.txt", "r") as f:
  with open("in.txt", "r") as f:
    contents = f.read().splitlines()

  rngs: list[tuple[int, int]] = []
  queries: list[int] = []

  nxt = 0
  for line in contents:
    nxt += 1
    if line == '': 
      break
    splitted = line.split('-')
    rngs.append((int(splitted[0]), int(splitted[1])))

  for i in range(nxt, len(contents)):
    queries.append(int(contents[i]))

  print(sol(parse_part(), rngs, queries))

if __name__ == "__main__":
  main()
