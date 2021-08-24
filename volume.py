import typer
import batinfo
from os import getenv
from alsaaudio import Mixer
from pydantic.color import Color
from models import I3Proto, BlockButton

app = typer.Typer()

steps = getenv("steps", 5)
mixer = mixer = Mixer(getenv("mixer", "Master"))

def isMuted():
    return mixer.getmute()[0] == 1

def getVolume():
    return mixer.getvolume()[0]

def render(muted, volume):
    out = I3Proto()

    if(muted):
        out.full_text = "🔇"
    elif(volume < 20):
        out.full_text = "🔈 {}".format(volume)
    elif(volume < 50):
        out.full_text = "🔉 {}".format(volume)
    elif(volume < 101):
        out.full_text = "🔊 {}".format(volume)
    elif(volume < 200):
        out.full_text = "📢 {}".format(volume)
    else:
        out.full_text = "⚠️ {}".format(volume)

    return out

@app.command()
def decVolume():
    vol = getVolume()

    if(vol < steps):
        vol = 0
    else: 
        vol = vol - steps

    mixer.setvolume(vol)

@app.command()
def incVolume():
    vol = getVolume()

    if(vol > 100):
        vol = 100
    else: 
        vol = vol + steps

    mixer.setvolume(vol)

@app.command()
def show():
    button = getenv("BLOCK_BUTTON", 0)

    if(button == BlockButton.scrollUp.value):
        incVolume()
    elif(button == BlockButton.scrollDown.value):
        decVolume()
        
    render(isMuted(), getVolume()).print()


if __name__ == "__main__":
    app()
