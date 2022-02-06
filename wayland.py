"""
Wayland-specific configuration
"""

import asyncio
import os
import subprocess

from libqtile import hook, qtile, backend

from libqtile.lazy import lazy
from libqtile.log_utils import logger

IS_XEPHYR = int(os.environ.get("QTILE_XEPHYR", 0))
mod = "mod1" if IS_XEPHYR else "mod4"

term = "footclient"
keys_backend = []


# Keys to change VT
keys_backend.extend(
    [
        ([mod], "F1", lazy.core.change_vt(1), "Change to VT 1"),
        ([mod], "F2", lazy.core.change_vt(2), "Change to VT 2"),
        ([mod], "F3", lazy.core.change_vt(3), "Change to VT 3"),
        ([mod], "F4", lazy.core.change_vt(4), "Change to VT 4"),
    ]
)


# Configure input devices
try:
    from libqtile.backend.wayland import InputConfig

    wl_input_rules = {
        "type:keyboard": InputConfig(
            kb_options="caps:swapescape,altwin:swap_alt_win",
            kb_layout="gb",
            kb_repeat_rate=35,
            kb_repeat_delay=250,
        ),
        "1267:12377:ELAN1300:00 04F3:3059 Touchpad": InputConfig(
            drag=True, tap=True, dwt=False, pointer_accel=0.3
        ),
        "type:pointer": InputConfig(pointer_accel=-0.9),
    }
except ImportError:
    wl_input_rules = None


@hook.subscribe.client_new
def _(win):
    # Auto-float some windows
    if isinstance(win, base.Window):
        state = win.surface.toplevel._ptr.current
        if 0 < state.max_width < 1920:
            win.floating = True


@hook.subscribe.client_managed
def _(win):
    if win.name == "Firefox — Sharing Indicator":
        win.place(win.x + win.borderwidth, 0, win.width, win.height, 0, None)


@hook.subscribe.startup_once
async def _():
    # Run a startup script
    env = os.environ.copy()
    env["WOB_HEIGHT"] = "28"
    env["WOB_WIDTH"] = "1920"
    env["WOB_MARGIN"] = "0"
    env["WOB_OFFSET"] = "0"
    env["WOB_BORDER"] = "0"
    env["WOB_PADDING"] = "0"
    env["WOB_BACKGROUND"] = "#00000000"
    env["WOB_BAR"] = "#66CFCCD6"
    HOME = os.path.expanduser("~")
    p = subprocess.Popen(f"{HOME}/.config/qtile/startup.sh", shell=True, env=env)
    hook.subscribe.shutdown(p.terminate)


if IS_XEPHYR:
    # To adapt to whatever window size it was given
    @hook.subscribe.startup_once
    async def _():
        await asyncio.sleep(0.5)
        qtile.cmd_reconfigure_screens()
