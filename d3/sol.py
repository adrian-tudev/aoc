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

DIGITS = 12

def rec(s: str, n: int) -> str:
  if n == 0: return ""
  slice = len(s) - n + 1
  d = max(s[:slice])

  for i, digit in enumerate(s):
    if digit == d:
      return d + rec(s[i + 1:], n - 1)

def sol(part: Part, banks: list[str]) -> int:
  ans: int = 0

  for bank in banks:
    # PART ONE
    if part == Part.ONE:
      fst: str = max(bank[:-1])
      snd: str = ""
      for i, digit in enumerate(bank):
        if digit == fst:
          snd = max(bank[i+1:])
          break
      ans += int(fst + snd)
      """
      (part one is also solvable through part 2 solution)
      ans += int(rec(bank, 2))
      """

    # PART TWO
    elif part == Part.TWO:
      ans += int(rec(bank, DIGITS))

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
