"""把包当 CLI 跑：python -m pylab01 add 1 2

argparse 是 stdlib 自带、零依赖。
真实项目推荐 typer/click，第 08 章会讲。
"""

import argparse
import sys

from .calculator import add, divide, is_even


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pylab01")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="两数相加")
    p_add.add_argument("a", type=float)
    p_add.add_argument("b", type=float)

    p_div = sub.add_parser("divide", help="两数相除")
    p_div.add_argument("a", type=float)
    p_div.add_argument("b", type=float)

    p_even = sub.add_parser("even", help="判断是否偶数")
    p_even.add_argument("n", type=int)

    args = parser.parse_args(argv)

    try:
        if args.cmd == "add":
            print(add(args.a, args.b))
        elif args.cmd == "divide":
            print(divide(args.a, args.b))
        elif args.cmd == "even":
            print(is_even(args.n))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
