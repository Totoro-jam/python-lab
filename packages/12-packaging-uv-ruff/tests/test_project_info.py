"""Tests for pylab12.project_info — pyproject.toml parsing utilities."""

from __future__ import annotations

from pathlib import Path

from pylab12.project_info import (
    get_build_backend,
    get_dependencies,
    get_project_name,
    get_python_requires,
    load_pyproject,
    summarize,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_pyproject_self():
    data = load_pyproject(Path(__file__).resolve().parents[1] / "pyproject.toml")
    assert get_project_name(data) == "pylab12"


def test_get_project_name_missing():
    assert get_project_name({}) == "<unknown>"


def test_get_python_requires():
    data = {"project": {"requires-python": ">=3.11"}}
    assert get_python_requires(data) == ">=3.11"


def test_get_python_requires_missing():
    assert get_python_requires({}) == "unspecified"


def test_get_dependencies():
    data = {"project": {"dependencies": ["httpx>=0.27", "rich"]}}
    assert get_dependencies(data) == ["httpx>=0.27", "rich"]


def test_get_dependencies_empty():
    assert get_dependencies({"project": {}}) == []


def test_get_build_backend():
    data = {"build-system": {"build-backend": "hatchling.build"}}
    assert get_build_backend(data) == "hatchling.build"


def test_summarize():
    data = {
        "project": {
            "name": "demo",
            "requires-python": ">=3.12",
            "dependencies": ["click"],
        },
        "build-system": {"build-backend": "hatchling.build"},
    }
    text = summarize(data)
    assert "demo" in text
    assert ">=3.12" in text
    assert "click" in text
    assert "hatchling.build" in text


def test_summarize_no_deps():
    data = {"project": {"name": "empty", "requires-python": ">=3.11"}}
    text = summarize(data)
    assert "(none)" in text
