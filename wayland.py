"""
Wayland-specific configuration
"""

import asyncio
import os
import subprocess

from libqtile import hook, qtile
from libqtile.backend.wayland.window import Window
from libqtile.lazy import lazy
from libqtile.log_utils import logger

IS_XEPHYR = int(os.environ.get("QTILE_XEPHYR", 0))
mod = "mod1" if IS_XEPHYR else "mod4"

term = 'footclient'
keys_backend = []


# Keys to change VT
keys_backend.extend([
    ([mod], 'F1',     lazy.core.change_vt(1),    "Change to VT 1"),
    ([mod], 'F2',     lazy.core.change_vt(2),    "Change to VT 2"),
    ([mod], 'F3',     lazy.core.change_vt(3),    "Change to VT 3"),
    ([mod], 'F4',     lazy.core.change_vt(4),    "Change to VT 4"),
])


# Configure libinput devices
try:
    from libqtile.backend.wayland import InputConfig
    wayland_libinput_config = {
            "type:pointer": InputConfig(pointer_accel=-0.9),
            "1267:12377:ELAN1300:00 04F3:3059 Touchpad": InputConfig(drag=True,
                tap=True, swt=False, pointer_accel=0.3),
    }
except ImportError:
    wayland_libinput_config = None


@hook.subscribe.client_new
def _(window):
    # Auto-float some windows
    if type(window) is Window:
        state = window.surface.toplevel._ptr.current
        if 0 < state.max_width < 1920:
            window.floating = True


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
    HOME = os.path.expanduser('~')
    p = subprocess.Popen(f"{HOME}/.config/qtile/startup.sh", shell=True, env=env)
    hook.subscribe.shutdown(p.terminate)


if IS_XEPHYR:
    # To adapt to whatever window size it was given
    @hook.subscribe.startup_once
    async def _():
        await asyncio.sleep(0.5)
        qtile.cmd_reconfigure_screens()
