"""
X11-specific configuration
"""

import os

from libqtile.lazy import lazy

IS_XEPHYR = int(os.environ.get("QTILE_XEPHYR", 0))
mod = "mod1" if IS_XEPHYR else "mod4"


term = 'xterm' if IS_XEPHYR else 'urxvt'  # urxvt doesn't like xephyr
wmname = 'LG3D'
keys_backend = []


# Keys to run X11-only launchers
keys_backend.extend([
    ([mod],             'd',    lazy.spawn('rofi -show run -theme ~/.config/rofi/common-large.rasi'), "rofi: run"),
    ([],    'XF86PowerOff',     lazy.spawn('power-menu'),                   "Power menu"),
    ([mod, 'shift'],    'x',    lazy.spawn('set_monitors'),                 "Configure monitors"),
    ([mod, 'shift'],    'i',    lazy.spawn('slock systemctl suspend -i'),   "Suspend system and lock"),
])
