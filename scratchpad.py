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

HOME: str = os.path.expanduser("~")
IS_WAYLAND: bool = qtile.core.name == "wayland"
IS_XEPHYR: bool = int(os.environ.get("QTILE_XEPHYR", 0)) > 0
mod = "mod1" if IS_XEPHYR else "mod4"


if IS_WAYLAND:
    term = "foot "
else:
    term = "xterm -e "


conf = {
    "warp_pointer": False,
    "on_focus_lost_hide": False,
    "opacity": 1,
}

GHCI = "ghci"
# GHCI = "ghci-9.2.2"

dropdowns = [
    DropDown("tmux", term + "tmux", height=0.4, **conf),
    DropDown(
        "ncmpcpp", term + "ncmpcpp", x=0.12, y=0.2, width=0.56, height=0.7, **conf
    ),
    DropDown("python", term + "python", x=0.05, y=0.1, width=0.2, height=0.3, **conf),
    DropDown(GHCI, term + GHCI, y=0.6, height=0.4, **conf),
]


# Keybindings to open each DropDown
keys_scratchpad = [
    (
        [mod, "shift"],
        "Return",
        lazy.group["scratchpad"].dropdown_toggle("tmux"),
        "Toggle tmux scratchpad",
    ),
    (
        [mod, "control"],
        "m",
        lazy.group["scratchpad"].dropdown_toggle("ncmpcpp"),
        "Toggle ncmpcpp scratchpad",
    ),
    (
        [mod],
        "c",
        lazy.group["scratchpad"].dropdown_toggle("python"),
        "Toggle python scratchpad",
    ),
    (
        [mod],
        "g",
        lazy.group["scratchpad"].dropdown_toggle(GHCI),
        "Toggle GHCI scratchpad",
    ),
]

scratchpad = ScratchPad("scratchpad", dropdowns)
