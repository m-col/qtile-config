"""
X11-specific configuration
"""

import os

from libqtile import hook, qtile
from libqtile.lazy import lazy

IS_XEPHYR = int(os.environ.get("QTILE_XEPHYR", 0))
mod = "mod1" if IS_XEPHYR else "mod4"


term = 'xterm' if IS_XEPHYR else 'urxvt'  # urxvt doesn't like xephyr
wmname = 'LG3D'
keys_backend = []


# Keys to run X11-only launchers
keys_backend.extend([
    #([mod],             'd',
    #   lazy.spawn('rofi -show run -theme ~/.config/rofi/common-large.rasi'), "rofi: run"),
    ([],    'XF86PowerOff',     lazy.spawn('power-menu'),                   "Power menu"),
    ([mod, 'shift'],    'x',    lazy.spawn('set_monitors'),                 "Configure monitors"),
    ([mod, 'shift'],    'i',    lazy.spawn('slock systemctl suspend -i'),   "Suspend system and lock"),
])


# Auto-float some windows
@hook.subscribe.client_new
def _(window):
    if window.window.get_wm_type() == "desktop":
        window.cmd_static(qtile.current_screen.index)
        return

    hints = window.window.get_wm_normal_hints()
    if hints and 0 < hints['max_width'] < 1920:
        window.floating = True
