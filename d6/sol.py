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

from collections.abc import Callable
from functools import reduce

def calc(nums: list[list[int]], ops: list[Callable]) -> int:
  assert len(nums) == len(ops)
  return sum(map(lambda x: reduce(x[0], x[1]), zip(ops, nums)))

def main():
  part = parse_part()

  contents: list[str] | None = None
  #with open("sample.txt", "r") as f:
  with open("in.txt", "r") as f:
    contents = f.read().splitlines()

  def _add(a: int, b: int):
    return a + b

  def _mul(a: int, b: int):
    return a * b

  nums: list[list[int]] = []
  ops: list[Callable] = []
  h: int = len(contents)

  if part == Part.ONE:
    nums: list[list[int]] = [[] for _ in range(len(contents[0].split()))]
    for k in range(h - 1):
      line = contents[k]
      for i, num in enumerate(line.split()):
        nums[i].append(int(num))

  elif part == Part.TWO:
    hw: list[int] = []
    for j in range(len(contents[0])):
      num: str = ""
      empty: bool = True
      for i in range(h - 1):
        if contents[i][j] != ' ': empty = False
        num += contents[i][j]
      if not empty:
        hw.append(int(num))
      else:
        nums.append(hw)
        hw = []
    nums.append(hw)

  for op in contents[h - 1].split():
    if op == '*': ops.append(_mul)
    elif op == '+': ops.append(_add)

  print(calc(nums, ops))

if __name__ == "__main__":
  main()
