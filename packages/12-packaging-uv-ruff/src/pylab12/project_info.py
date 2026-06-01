"""Parse and summarize a pyproject.toml file."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def load_pyproject(path: Path | None = None) -> dict[str, Any]:
    if path is None:
        path = Path("pyproject.toml")
    with path.open("rb") as f:
        return tomllib.load(f)


def get_project_name(data: dict[str, Any]) -> str:
    return data.get("project", {}).get("name", "<unknown>")


def get_python_requires(data: dict[str, Any]) -> str:
    return data.get("project", {}).get("requires-python", "unspecified")


def get_dependencies(data: dict[str, Any]) -> list[str]:
    return data.get("project", {}).get("dependencies", [])


def get_build_backend(data: dict[str, Any]) -> str:
    return data.get("build-system", {}).get("build-backend", "unspecified")


def summarize(data: dict[str, Any]) -> str:
    name = get_project_name(data)
    python = get_python_requires(data)
    deps = get_dependencies(data)
    backend = get_build_backend(data)
    lines = [
        f"Project:  {name}",
        f"Python:   {python}",
        f"Backend:  {backend}",
        f"Deps:     {', '.join(deps) if deps else '(none)'}",
    ]
    return "\n".join(lines)
