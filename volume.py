import typer
import batinfo
from os import getenv
from alsaaudio import Mixer, ALSAAudioError
from pydantic.color import Color
from models import I3Proto, BlockButton

app = typer.Typer()

steps = getenv("steps", 5)
mixer = mixer = Mixer(getenv("mixer", "Master"))

# print(mixer.volumecap())

def isMuted():
    try:
        return mixer.getmute()[0] == 1
    except ALSAAudioError:
        return False

def getDirection():
    if "Capture Volume" in mixer.volumecap():
        return 1
    else:
        return 0

def getVolume():
    try:
        return mixer.getvolume(getDirection())[0]
    except IndexError:
        return 0

def setVolume(volume):
    return mixer.setvolume(
        volume,
        -1,
        getDirection()
    )

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

    setVolume(vol)

@app.command()
def incVolume():
    vol = getVolume()

    if(vol > 95):
        vol = 100
    else: 
        vol = vol + steps

    setVolume(vol)

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
