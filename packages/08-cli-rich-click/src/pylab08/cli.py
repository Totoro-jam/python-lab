"""文件统计 CLI 工具：演示 typer 子命令、rich 输出、进度条。"""

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

app = typer.Typer(help="pylab08 — 文件统计与管理工具")
console = Console()


@app.command()
def stats(
    directory: Annotated[Path, typer.Argument(help="要统计的目录")] = Path("."),
    pattern: Annotated[str, typer.Option("--pattern", "-p", help="文件 glob 模式")] = "*",
    show_table: Annotated[bool, typer.Option("--table", "-t", help="以表格形式展示")] = False,
) -> None:
    """统计目录下的文件信息。"""
    if not directory.is_dir():
        console.print(f"[red]Error:[/red] {directory} is not a directory")
        raise typer.Exit(1)

    files = list(directory.rglob(pattern))
    files = [f for f in files if f.is_file()]

    if not files:
        console.print("[yellow]No files found.[/yellow]")
        raise typer.Exit(0)

    total_size = sum(f.stat().st_size for f in files)

    if show_table:
        table = Table(title=f"Files in {directory}")
        table.add_column("Name", style="cyan")
        table.add_column("Size (bytes)", justify="right", style="green")
        table.add_column("Suffix", style="magenta")

        for f in sorted(files)[:20]:
            table.add_row(f.name, str(f.stat().st_size), f.suffix or "-")

        if len(files) > 20:
            table.add_row("...", "...", "...")

        console.print(table)
    else:
        console.print(Panel(
            f"[bold]{len(files)}[/bold] files, "
            f"[bold]{total_size:,}[/bold] bytes total",
            title="Statistics",
        ))


@app.command()
def find(
    directory: Annotated[Path, typer.Argument(help="搜索目录")] = Path("."),
    name: Annotated[str, typer.Option("--name", "-n", help="文件名关键字")] = "",
    suffix: Annotated[str, typer.Option("--suffix", "-s", help="文件后缀")] = "",
) -> None:
    """搜索文件。"""
    if not directory.is_dir():
        console.print(f"[red]Error:[/red] {directory} is not a directory")
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Searching...", total=None)

        results = []
        for f in directory.rglob("*"):
            if not f.is_file():
                continue
            if name and name.lower() not in f.name.lower():
                continue
            if suffix and f.suffix != suffix:
                continue
            results.append(f)

    if results:
        for f in results[:50]:
            console.print(f"  [cyan]{f.relative_to(directory)}[/cyan]")
        if len(results) > 50:
            console.print(f"  ... and {len(results) - 50} more")
    else:
        console.print("[yellow]No files matched.[/yellow]")


@app.command()
def version() -> None:
    """显示版本信息。"""
    from pylab08 import __version__
    console.print(f"pylab08 v{__version__}")


if __name__ == "__main__":
    app()
