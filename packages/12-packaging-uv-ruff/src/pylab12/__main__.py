"""Entry point: `python -m pylab12` or `pylab12` CLI."""

from pylab12.project_info import load_pyproject, summarize


def main() -> None:
    info = load_pyproject()
    print(summarize(info))


if __name__ == "__main__":
    main()
