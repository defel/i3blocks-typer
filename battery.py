import typer
import batinfo
from pydantic.color import Color

from models import I3Proto

app = typer.Typer()


@app.command()
def show():
    bat = batinfo.Batteries()

    out = I3Proto()

    if bat.stat[0].status == "Full":
        out.full_text = "{} ✅".format(bat.stat[0].name)
        out.short_text = "✅"
    elif bat.stat[0].status == "Discharging":
        out.full_text = "{} 🔋 {}%".format(bat.stat[0].name, bat.stat[0].capacity)
        out.short_text = "🔋{}%".format(bat.stat[0].capacity)

        if bat.stat[0].capacity < 10:
            out.background = "#ff0000"
        elif bat.stat[0].capacity < 50:
            out.color = "#FF8000"

    else:
        out.full_text = "{} ⚡ {}%".format(bat.stat[0].name, bat.stat[0].capacity)
        out.short_text = "⚡ {}%".format(bat.stat[0].capacity)
        out.color = "#00fa00"

    out.print()

if __name__ == "__main__":
    app()
