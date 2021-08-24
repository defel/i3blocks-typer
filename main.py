#!/usr/bin/python
import typer

import battery
import volume

app = typer.Typer()
app.add_typer(battery.app, name="battery")
app.add_typer(volume.app, name="volume")

if __name__ == "__main__":
    app()