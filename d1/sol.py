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

MOD = 100

def sign(n: int) -> int:
  if n > 0: return 1
  elif n < 0: return -1
  return 0

def wrap_cnt(dial: int, n: int) -> int:
  ans = abs(n) // MOD
  if dial == 0: return ans
  n = sign(n) * (abs(n) % MOD)
  nxt = n + dial
  if n < 0 and nxt <= 0: ans += 1
  elif n > 0 and nxt >= 100: ans += 1
  return ans

def main():
  contents: str | None = None
  with open("in.txt", "r") as f:
    contents = f.read()
  data: list[str] = contents.split()
  formatted: list[int] = []
  for line in data:
    key: int = -1 if line[0] == 'L' else 1
    val: int = int(line[1:])
    formatted.append(key * val)

  print(sol(parse_part(), formatted))

def sol(part: Part, data: list[int]):
  p: int = 50
  ans: int = 0
  for e in data:
    nxt: int = (p + e) % MOD
    match part:
      case Part.ONE:
        ans += nxt == 0
      case Part.TWO:
        ans += wrap_cnt(p, e)
    p = nxt
  return ans

if __name__ == "__main__":
  main()
