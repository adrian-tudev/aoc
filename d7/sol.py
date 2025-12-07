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

from functools import cache
from parser import Part, parse_part # type: ignore 

def sim(splitters: str, beams: set[int]) -> tuple[int, set[int]]:
  cnt: int = 0
  out: set[int] = set()

  for beam_idx in beams:
    if splitters[beam_idx] == '^':
      out.add(beam_idx - 1)
      out.add(beam_idx + 1)
      cnt += 1
    else:
      # fall through if no splitter found
      out.add(beam_idx)

  return (cnt, out)

def count_paths(map: list[str], start: tuple[int, int]) -> int:
  @cache
  def dfs(r: int, c: int) -> int:
    # hit bottom
    if r + 1 >= len(map): return 1

    below = map[r + 1][c]
    if below == '.':
      return dfs(r + 1, c)
    elif below == '^':
      l = dfs(r + 1, c - 1)
      r = dfs(r + 1, c + 1)
      return l + r
    else:
      # fall through if |
      return dfs(r + 1, c)

  return dfs(*start)

def main():
  part = parse_part()
  contents: list[str] | None = None
  #with open("sample.txt", "r") as f:
  with open("in.txt", "r") as f:
    contents = f.read().splitlines()

  start: int = contents[0].find('S')
  assert start != -1

  ans: int = 0

  # PART ONE
  if part == Part.ONE:
    beams: set[int] = {start}
    for i in range(2, len(contents) - 1, 2):
      cnt, beams = sim(contents[i], beams)
      ans += cnt

  # PART TWO
  elif part == Part.TWO:
    ans = count_paths(contents, (0, start))

  print(ans)

if __name__ == "__main__":
  main()
