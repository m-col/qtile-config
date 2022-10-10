"""
Wayland-specific configuration
"""

import asyncio
import os
import subprocess

from libqtile import hook, qtile
from libqtile.backend.wayland import InputConfig
from libqtile.backend.wayland.xdgwindow import XdgWindow
from libqtile.backend.wayland.xwindow import XWindow
from libqtile.lazy import lazy

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

# Inputs configuration
wl_input_rules = {
    "type:keyboard": InputConfig(
        kb_options="caps:swapescape,altwin:swap_alt_win",
        kb_layout="gb",
        kb_repeat_rate=50,
        kb_repeat_delay=250,
    ),
    # Zenbook touchpad
    "1267:12377:ELAN1300:00 04F3:3059 Touchpad": InputConfig(
        drag=True, tap=True, dwt=False, pointer_accel=0.3
    ),
    # Roccat Kiro mouse
    "7805:11320:ROCCAT ROCCAT Kiro Mouse": InputConfig(
        left_handed=True,
        pointer_accel=-1.0,
    ),
    # Anker mouse
    "7119:5:USB Optical Mouse": InputConfig(pointer_accel=-1.0),
}


# Shadows configuration
# wl_shadows = {
#    "radius": 12,
#    "color": "#05001088",
#    "offset": (-6, -6),
# }
wl_shadows = {
    "radius": 5,
    "color": "#ff000044",
    "offset": (0, 0),
}


@hook.subscribe.client_new
def _(win):
    # Auto-float some windows
    if isinstance(win, XdgWindow):
        max_width = win.surface.toplevel._ptr.current.max_width
        if 0 < max_width < 1920:
            win.floating = True
    elif isinstance(win, XWindow):
        if hints := win.surface.size_hints:
            max_width = hints.max_width
            if 0 < max_width < 1920:
                win.floating = True


@hook.subscribe.client_managed
async def _(win):
    # Some other miscellaneous rules
    if win.name == "Firefox — Sharing Indicator":
        win.place(win.x + win.borderwidth, 0, win.width, win.height, 0, None)
        return

    wm_class = win.get_wm_class() or []
    if win.name == "Navigator" and "libreoffice-startcenter" in wm_class:
        x = qtile.current_screen.x
        win.place(x, 240, 450, 600, win.borderwidth, win.bordercolor)
        return

    if "mpv" in wm_class:
        # Resizing mpv if it's sized itself too big to fit on screen
        sw = qtile.current_screen.width
        sh = qtile.current_screen.height
        x = y = w = h = None
        if win.height > sh:
            h = sh
            y = qtile.current_screen.y
        if win.width > sw:
            w = sw
            x = qtile.current_screen.x
        if w is not None or h is not None:
            if h is None:
                h = win.height
                y = win.y
            else:
                w = win.width
                x = win.x
            bw = win.borderwidth
            win.place(x - bw, y - bw, w + 2 * bw, h + 2 * bw, 0, None)
        return


@hook.subscribe.startup_once
async def _():
    # Run a startup script
    HOME = os.path.expanduser("~")
    p = subprocess.Popen(f"{HOME}/.config/qtile/startup.sh")
    hook.subscribe.shutdown(p.terminate)


@hook.subscribe.screen_change
def _(*_):
    # Temporary hacky fix for the dell monitor on my desk which for some mysterious
    # reason doesn't advertise that it supports any HD mode. Qtile does support setting
    # custom modes via the protocol, but neither kanshi nor wdisplays do. So instead,
    # I'll detect if that monitor is present and set the desired custom mode here.
    for output in qtile.core.outputs:
        wlr_output = output.wlr_output
        # Not only does this monitor not report modes correctly, it ALSO doesn't report
        # a make or model.
        if wlr_output.make == wlr_output.model == "<Unknown>":
            if wlr_output.current_mode.width == 1024:
                break
    else:
        return

    wlr_output.set_custom_mode(1920, 1080, 0)
    # Lastly, while cmd_reconfigure_screens will be fired right after this hook, as it
    # gets subscribed to this hook right after the config is loaded, the backend doesn't
    # get a change to actually apply the mode, so let's flush it.
    qtile.core.flush()


if IS_XEPHYR:
    # To adapt to whatever window size it was given
    @hook.subscribe.startup_once
    async def _():
        await asyncio.sleep(0.5)
        qtile.reconfigure_screens()
