import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from schemas import PromptRequest
from agent import run_coding_agent
from database import init_db, save_interaction, get_recent_history

app = typer.Typer(help="DevPilot: Autonomous AI Coding CLI powered by OpenAI, Pydantic & PostgreSQL.")
console = Console()

@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Your coding instruction or question for the AI agent"),
    workdir: str = typer.Option(".", "--dir", "-d", help="Working directory for the agent"),
):
    """Send a coding task to the AI Agent, execute file tools, and log to PostgreSQL."""
    init_db()

    request = PromptRequest(prompt=prompt, working_dir=workdir)
    console.print(Panel(f"[bold green]Task:[/bold green] {request.prompt}", title="🚀 DevPilot AI Agent"))

    with console.status("[bold magenta]Agent is thinking and inspecting workspace...[/bold magenta]"):
        result = run_coding_agent(request)

    console.print("\n[bold cyan]💡 Explanation:[/bold cyan]")
    console.print(result.explanation)

    if result.code_snippet.strip():
        console.print("\n[bold cyan]💻 Code / Command:[/bold cyan]")
        syntax = Syntax(result.code_snippet, result.language, theme="monokai", line_numbers=True)
        console.print(syntax)

    if result.files_touched:
        table = Table(title="📂 Files Inspected or Modified")
        table.add_column("File Path", style="cyan")
        table.add_column("Action", style="magenta")
        table.add_column("Summary", style="white")
        for f in result.files_touched:
            table.add_row(f.file_path, f.action_taken, f.summary)
        console.print("\n", table)

    if result.next_steps:
        console.print("\n[bold green]⏭️ Next Steps:[/bold green]")
        for idx, step in enumerate(result.next_steps, 1):
            console.print(f"  {idx}. {step}")

    record_id = save_interaction(request.prompt, result)
    console.print(f"\n[dim]✔ Saved to PostgreSQL history (Log ID: #{record_id})[/dim]")


@app.command()
def history(limit: int = typer.Option(5, "--limit", "-n", help="Number of past logs to fetch")):
    """Fetch past coding tasks and responses from the PostgreSQL database."""
    init_db()
    records = get_recent_history(limit=limit)

    if not records:
        console.print("[yellow]No history found in PostgreSQL yet. Run 'python cli.py ask ...' first![/yellow]")
        return

    table = Table(title=f"📜 Last {len(records)} DevPilot Interactions (from PostgreSQL)")
    table.add_column("ID", style="bold cyan", width=6)
    table.add_column("Timestamp (UTC)", style="dim", width=20)
    table.add_column("Prompt", style="green")
    table.add_column("Language", style="magenta", width=10)
    table.add_column("Explanation Summary", style="white")

    for row in records:
        short_exp = (row.explanation[:75] + "...") if len(row.explanation) > 75 else row.explanation
        table.add_row(
            str(row.id),
            row.created_at.strftime("%Y-%m-%d %H:%M"),
            row.prompt,
            row.language,
            short_exp,
        )

    console.print(table)


if __name__ == "__main__":
    app()