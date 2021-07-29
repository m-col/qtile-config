"""
Scratchpad and DropDowns
========================

The scratchpads are the same with either backend, but the terminal used differs. I
prefer these terminals over something like alacritty, which would be an easier
alternative to configure because it works under both Wayland and X.
"""

import os

from libqtile import qtile
from libqtile.config import DropDown, ScratchPad
from libqtile.lazy import lazy

HOME: str = os.path.expanduser('~')
IS_WAYLAND: bool = qtile.core.name == "wayland"
IS_XEPHYR: bool = int(os.environ.get("QTILE_XEPHYR", 0)) > 0
mod = "mod1" if IS_XEPHYR else "mod4"


if IS_WAYLAND:
    term = "foot "
    mutt = f"foot -D {HOME}/Downloads mutt"
else:
    if IS_XEPHYR:
        term = "xterm -e "
    else:
        term = "urxvt -e "
    mutt = f"urxvt -cd {HOME}/Downloads -e mutt"


conf = {
    "warp_pointer": False,
    "on_focus_lost_hide": True,
    "opacity": 1,
}

dropdowns = [
    DropDown("tmux", term + "tmux", height=0.4, **conf),
    #DropDown("irc", term + "irc", x=0.1, y=0.05, width=0.8, height=0.9, **conf),
    DropDown("ncmpcpp", term + "ncmpcpp", x=0.12, y=0.2, width=0.56, height=0.7, **conf),
    DropDown("python", term + "python", x=0.05, y=0.1, width=0.2, height=0.3, **conf),
    #DropDown("email", mutt, x=0.1, y=0.05, width=0.8, height=0.9, **conf),
    #DropDown("newsboat", term + "newsboat", x=0.2, y=0.05, width=0.6, height=0.9, **conf),
]


# Keybindings to open each DropDown
keys_scratchpad = [
    ([mod, 'shift'],     'Return',
        lazy.group['scratchpad'].dropdown_toggle('tmux'), "Toggle tmux scratchpad"),
    ([mod, 'control'],   'e',
        lazy.group['scratchpad'].dropdown_toggle('email'), "Toggle email scratchpad"),
    ([mod, 'control'],   'w',
        lazy.group['scratchpad'].dropdown_toggle('irc'), "Toggle irc scratchpad"),
    ([mod, 'control'],   'm',
        lazy.group['scratchpad'].dropdown_toggle('ncmpcpp'), "Toggle ncmpcpp scratchpad"),
    ([mod],              'c',
        lazy.group['scratchpad'].dropdown_toggle('python'), "Toggle python scratchpad"),
    #([mod, 'control'],   'n',
    #    lazy.group['scratchpad'].dropdown_toggle('newsboat'), "Toggle newsboat scratchpad"),
]

scratchpad = ScratchPad("scratchpad", dropdowns)
