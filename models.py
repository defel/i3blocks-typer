from pydantic import BaseModel
from pydantic.color import Color
from enum import Enum

# see:
# - https://vivien.github.io/i3blocks/#_format
# - https://i3wm.org/docs/i3bar-protocol.html#_blocks_in_detail
class I3Proto(BaseModel):
    full_text: str = ""
    short_text: str = None
    color: str = None
    background: str = None

    def print(self):
        print(self.full_text)
        print(self.short_text if self.short_text is not None else self.full_text)
        print(self.color if self.color is not None else "#ffffff")
        print(self.background if self.background is not None else "#000000")

# 1 = Left, 2 = Middle, 3 = Right, 4 = Scroll Up, 5 = Scroll Down, 6 = Custom, 7 = Custom, 8 = Upper Thumb, 9 = Lower Thumb, 10+ = Custom
class BlockButton(Enum):
    undefined = "0"
    left = "1"
    middle = "2"
    right = "3"
    scrollUp = "4"
    scrollDown = "5"
    upperThumb = "8"
    lowerThumb = "9"