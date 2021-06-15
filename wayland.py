"""
Wayland-specific configuration
"""

import os

from libqtile.backend.wayland import InputConfig
from libqtile.lazy import lazy

IS_XEPHYR = int(os.environ.get("QTILE_XEPHYR", 0))
mod = "mod1" if IS_XEPHYR else "mod4"

term = 'footclient'
keys_backend = []


# Keys to change VT
keys_backend.extend([
    ([mod], 'F1',     lazy.change_vt(1),    "Change to VT 1"),
    ([mod], 'F2',     lazy.change_vt(2),    "Change to VT 2"),
    ([mod], 'F3',     lazy.change_vt(3),    "Change to VT 3"),
    ([mod], 'F4',     lazy.change_vt(4),    "Change to VT 4"),
    ([mod], 'F5',     lazy.change_vt(5),    "Change to VT 5"),
    ([mod], 'F6',     lazy.change_vt(6),    "Change to VT 6"),
])


# Keys to run Wayland-only launchers
keys_backend.extend([
    ([mod], 'd', lazy.spawn('wofi --gtk-dark --show run'), "wofi: run"),
])


# Configure libinput devices
wayland_libinput_config = {
    "type:pointer": InputConfig(drag=True, tap=True)
}
