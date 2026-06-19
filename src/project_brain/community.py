import webbrowser
from rich.console import Console

console = Console()

DISCUSSIONS_URL = (
    "https://github.com/Srujan-Amaragatti05/project-brain/discussions"
)


def open_feedback():
    try:
        opened = webbrowser.open(DISCUSSIONS_URL)

        if opened:
            console.print(
                "[green]Opened GitHub Discussions in browser.[/green]"
            )
        else:
            raise RuntimeError()

    except Exception:
        console.print(
            "[yellow]Unable to open browser automatically.[/yellow]"
        )
        console.print(f"\nFeedback URL:\n{DISCUSSIONS_URL}")

def open_website():
    try:
        opened = webbrowser.open("https://project-brain-web-gamma.vercel.app/")

        if opened:
            console.print(
                "[green]Opened Project Brain website in browser.[/green]"
            )
        else:
            raise RuntimeError()

    except Exception:
        console.print(
            "[yellow]Unable to open browser automatically.[/yellow]"
        )
        console.print(f"\nWebsite URL:\nhttps://project-brain-web-gamma.vercel.app/")