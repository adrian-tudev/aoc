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

def count(diagram: list[str]) -> list[tuple[int, int]]:
  res = []
  for i, row in enumerate(diagram):
    for j, col in enumerate(row):
      if col != '@': continue
      dx = (-1, 0, 1)
      dy = (-1, 0, 1)

      if i == 0: dy = (0, 1)
      elif i == len(diagram) - 1: dy = (-1, 0)
      if j == 0: dx = (0, 1)
      elif j == len(row) - 1: dx = (-1, 0)

      cnt = 0
      for y in dy:
        for x in dx:
          if x == 0 and y == 0: continue
          if diagram[i + y][j + x] == '@':
            cnt += 1

      if cnt < 4:
        res.append((i, j))
  return res

def remove_paper(diagram: list[str], papers: list[tuple[int, int]]) -> list[str]:
  for paper in papers:
    (i, j) = paper
    diagram[i] = diagram[i][:j] + 'X' + diagram[i][j + 1:]

  return diagram

def sol(part: Part, diagram: list[str]) -> int:
  ans: int = 0

  if part == Part.ONE:
    ans = len(count(diagram))
  elif part == Part.TWO:
    while True:
      removable = count(diagram)
      if len(removable) == 0: break
      ans += len(removable)
      diagram = remove_paper(diagram, removable)

  return ans

def main():
  contents: str | None = None
  #with open("sample.txt", "r") as f:
  with open("in.txt", "r") as f:
    contents = f.read()
  formatted: list[str] = contents.splitlines()

  print(sol(parse_part(), formatted))

if __name__ == "__main__":
  main()
