"""Stdlib test runner. Run: python run_tests.py [name filter]"""

import importlib
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))


def main() -> int:
    pattern = sys.argv[1] if len(sys.argv) > 1 else ""
    passed = failed = 0
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        module = importlib.import_module(path.stem)
        for name in sorted(n for n in dir(module) if n.startswith("test_") and pattern in f"{path.stem}.{n}"):
            try:
                getattr(module, name)()
            except Exception:
                failed += 1
                print(f"FAIL  {path.stem}.{name}")
                traceback.print_exc(limit=-1)
            else:
                passed += 1
                print(f"ok    {path.stem}.{name}")
    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
