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

def sol(part: Part, rngs: list[tuple[int, int]]) -> int:
  ans: int = 0

  for rng in rngs:
    mem = {}
    # 1e5 because the largest number in the input was 1e9, 1e5**2 > 1e9
    for i in range(1, 100000):
      id: str | None = None

      if part == Part.ONE:
        # PART ONE
        id = str(i) * 2
        n = int(id)
        if n <= rng[1] and n >= rng[0]:
          ans += n

      elif part == Part.TWO:
        # PART TWO
        upper = len(str(rng[1]))

        # brute force
        for j in range(2, upper + 1):
          id = str(i) * j
          if id in mem: continue
          n = int(id)
          if n <= rng[1] and n >= rng[0]:
            ans += n
            mem[id] = True

  return ans

def main():
  contents: str | None = None
  with open("in.txt", "r") as f:
    contents = f.read()
  formatted: list[tuple[int, int]] = []
  for rng in contents.strip().split(','):
    fst: int = int(rng.split('-')[0])
    snd: int = int(rng.split('-')[1])
    formatted.append((fst, snd))

  print(sol(parse_part(), formatted))

if __name__ == "__main__":
  main()
