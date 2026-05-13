from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def section(title: str):
    console.rule(f"[bold cyan]{title}")


def success(message: str, next_step: str | None = None):
    console.print(f"[bold green]✅ {message}[/bold green]")

    if next_step:
        console.print(
            Panel(
                f"[bold]Next:[/bold]\n{next_step}",
                border_style="cyan",
            )
        )


def error(message: str, suggestion: str | None = None):
    console.print(f"[bold red]❌ {message}[/bold red]")

    if suggestion:
        console.print(
            Panel(
                suggestion,
                title="Try",
                border_style="yellow",
            )
        )


def info(message: str):
    console.print(f"[cyan]ℹ {message}[/cyan]")


def key_value_table(title: str, rows: list[tuple[str, str]]):
    table = Table(title=title)

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    for k, v in rows:
        table.add_row(k, v)

    console.print(table)