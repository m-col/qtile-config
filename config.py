"""
Qtile main config file
======================
"""

from __future__ import annotations

import importlib
import os
import re
import subprocess
import sys
from typing import TYPE_CHECKING

from libqtile import bar, hook, layout, qtile, utils, widget
from libqtile.backend import base
from libqtile.config import Click, Drag, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.widget.backlight import ChangeDirection
from libqtile.widget.battery import Battery, BatteryState

import qtile_extras.widget as widget_extras

assert qtile is not None

if TYPE_CHECKING:
    from typing import Any

    from libqtile.core.manager import Qtile


# Config imports
def reload(module):
    if module in sys.modules:
        importlib.reload(sys.modules[module])


import traverse
from toggle_debug import toggle_debug

use_tags = False

if use_tags:
    reload("tags")
    from tags import groups, keys_group
else:
    reload("groups")
    from groups import groups, keys_group

reload("scratchpad")
from scratchpad import keys_scratchpad, scratchpad

reload("power_menu")
from power_menu import keys_power_menu

IS_WAYLAND: bool = qtile.core.name == "wayland"
IS_XEPHYR: bool = int(os.environ.get("QTILE_XEPHYR", 0)) > 0

reload(qtile.core.name)
if IS_WAYLAND:
    from wayland import keys_backend, term, wl_input_rules, wl_shadows  # noqa: F401
else:
    from x11 import keys_backend, term, wmname  # noqa: F401

# Colours
theme = dict(
    foreground="#CFCCD6",
    background="#0C1F20",
    color0="#030405",
    color8="#1f1c32",
    color1="#8742a5",
    color9="#9a5eb3",
    color2="#406794",
    color10="#5fd75f",
    color3="#653c21",
    color11="#6e9fcd",
    color4="#8f4ff0",
    color12="#BBC2E2",
    color5="#5d479d",
    color13="#998dd1",
    color6="#3e3e73",
    color14="#9a9dcc",
    color7="#495068",
    color15="#e1e1e4",
)

colours = [theme[f"color{n}"] for n in range(16)]
background = theme["background"]
foreground = theme["foreground"]
colour_focussed = "#6fa3e0"
colour_unfocussed = "#0e101c"
inner_gaps = 8
outer_gaps = 0

# https://coolors.co/1b2021-cfccd6-bbc2e2-b7b5e4-847979


# Keys

if IS_XEPHYR:
    mod = "mod1"
    alt = "control"
else:
    mod = "mod4"
    alt = "mod1"

# My keybindings - they are converted at the bottom of this file
my_keys: list[tuple[list[str], str, Any, str]] = []
my_keys.extend(keys_backend)
my_keys.extend(keys_group)
my_keys.extend(keys_scratchpad)
my_keys.extend(keys_power_menu)


def float_to_front(qtile: Qtile) -> None:
    """Bring all floating windows of the group to front"""
    for window in qtile.current_group.windows:
        if window.floating:
            window.bring_to_front()


my_keys.extend(
    [
        # Window management
        ([mod, "control"], "q", lazy.window.kill(), "Close window"),
        ([mod], "f", lazy.window.toggle_fullscreen(), "Toggle fullscreen"),
        ([mod, "shift"], "space", lazy.window.toggle_floating(), "Toggle floating"),
        ([mod], "s", lazy.spawn("ddg_rofi"), "Search web via rofi"),
        ([mod, "shift"], "s", lazy.window.static(), "Make window static"),
        (
            [mod],
            "space",
            lazy.function(float_to_front),
            "Move floating windows to the front",
        ),
        ([mod], "j", lazy.function(traverse.down), "Traverse down"),
        ([mod], "k", lazy.function(traverse.up), "Traverse up"),
        ([mod], "h", lazy.function(traverse.left), "Traverse left"),
        ([mod], "l", lazy.function(traverse.right), "Traverse right"),
        ([mod, "shift"], "j", lazy.layout.shuffle_down(), "Shuffle down"),
        ([mod, "shift"], "k", lazy.layout.shuffle_up(), "Shuffle up"),
        ([mod, "shift"], "h", lazy.layout.shuffle_left(), "Shuffle left"),
        ([mod, "shift"], "l", lazy.layout.shuffle_right(), "Shuffle right"),
        ([mod, alt], "j", lazy.layout.grow_down(), "Grow down"),
        ([mod, alt], "k", lazy.layout.grow_up(), "Grow up"),
        ([mod, alt], "h", lazy.layout.grow_left(), "Grow left"),
        ([mod, alt], "l", lazy.layout.grow_right(), "Grow right"),
        ([mod, "control"], "r", lazy.reload_config(), "Reload the config"),
        ([mod, "control"], "Escape", lazy.shutdown(), "Shutdown Qtile"),
        ([mod], "Tab", lazy.next_layout(), "Next layout"),
        ([mod], "b", lazy.hide_show_bar("bottom"), "Hide bar"),
        ([mod, "control"], "d", lazy.function(toggle_debug), "Toggle debug logging"),
        # Volume control - MyVolume widget is defined further down
        ([], "XF86AudioMute", lazy.widget["myvolume"].mute(), "Mute audio"),
        ([mod], "F10", lazy.widget["myvolume"].mute(), "Mute audio"),
        (
            [],
            "XF86AudioRaiseVolume",
            lazy.widget["myvolume"].increase_vol(),
            "Increase volume",
        ),
        ([mod], "F12", lazy.widget["myvolume"].increase_vol(), "Increase volume"),
        (
            [],
            "XF86AudioLowerVolume",
            lazy.widget["myvolume"].decrease_vol(),
            "Decrease volume",
        ),
        ([mod], "F11", lazy.widget["myvolume"].decrease_vol(), "Decrease volume"),
        # Backlight control
        (
            [],
            "XF86MonBrightnessUp",
            lazy.widget["backlight"].change_backlight(ChangeDirection.UP, 3),
            "Increase backlight",
        ),
        (
            [],
            "XF86MonBrightnessDown",
            lazy.widget["backlight"].change_backlight(ChangeDirection.DOWN, 3),
            "Decrease backlight",
        ),
        (
            [mod],
            "F6",
            lazy.widget["backlight"].change_backlight(ChangeDirection.UP, 3),
            "Increase backlight",
        ),
        (
            [mod],
            "F5",
            lazy.widget["backlight"].change_backlight(ChangeDirection.DOWN, 3),
            "Decrease backlight",
        ),
        # Music control
        (
            [mod],
            "bracketright",
            lazy.spawn("playerctl next"),
            "Next song",
        ),
        ([], "XF86AudioNext", lazy.spawn("playerctl next"), "Next song"),
        (
            [mod],
            "bracketleft",
            lazy.spawn("playerctl previous"),
            "Previous song",
        ),
        ([], "XF86AudioPrev", lazy.spawn("playerctl previous"), "Previous song"),
        ([], "Pause", lazy.spawn("playerctl play-pause"), "Play/unpause music"),
        ([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), "Play/unpause music"),
        # Launchers
        (
            [mod],
            "d",
            lazy.spawn("rofi -show run -theme ~/.config/rofi/common.rasi"),
            "Spawn with rofi",
        ),
        ([mod], "Return", lazy.spawn(term), "Spawn terminal"),
        ([mod, "shift"], "f", lazy.spawn("firefox"), "Spawn Firefox"),
        (
            [mod, "control"],
            "f",
            lazy.spawn("cleanfox"),
            "Spawn Firefox in clean profile",
        ),
        ([], "Print", lazy.spawn("screenshot copy"), "Screenshot to clipboard"),
        (["shift"], "Print", lazy.spawn("screenshot"), "Screenshot to file"),
        ([mod], "p", lazy.spawn("get_password_rofi"), "Keepass passwords"),
        ([mod], "i", lazy.spawn("systemctl suspend -i"), "Suspend system"),
        (
            [mod, "shift"],
            "i",
            lazy.spawn("gtklock & systemctl suspend -i", shell=True),
            "Suspend and lock",
        ),
        (
            ["control"],
            "space",
            lazy.spawn("swaync-client -t -sw"),
            "Toggle notification panel",
        ),
        (
            [mod, "control"],
            "y",
            lazy.spawn("yt-first"),
            "yt-first script",
        ),
    ]
)


# Mouse control
mouse = [
    Click([mod], "Button2", lazy.window.kill()),

    # Move with drag or swipe
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    #Swipe(
    #    [mod],
    #    3,
    #    lazy.window.set_position_floating(),
    #    start=lazy.window.get_position(),
    #),

    # Resize with drag or swipe
    Drag(
        [mod, alt],
        "Button1",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    #Swipe(
    #    [mod, alt],
    #    3,
    #    lazy.window.set_size_floating(),
    #    start=lazy.window.get_size(),
    #),

    # Slide between groups
    Drag(
        [mod, "shift"],
        "Button1",
        lazy.screen.group_slide(),
        start=lazy.screen.start_group_slide(scale=2.5),
    ),
]

if IS_WAYLAND:
    try:
        from libqtile.config import Swipe
    except ImportError:
        pass
    else:

        def _slide(qtile):
            groups = qtile.groups
            if len(qtile.screens) > 1:
                if qtile.current_screen.index == 0:
                    groups = groups[:4]
                else:
                    groups = groups[4:]
            return qtile.current_screen.start_group_slide(
                groups=groups, scale=1.6, inertia_threshold=15,
            )

        mouse.append(
            Swipe(
                [],
                3 if IS_XEPHYR else 4,
                lazy.screen.group_slide(),
                start=lazy.function(_slide),
            ),
        )


## Firefox 3-finger vertical swipe to zoom
#def swipe_zoom(qtile, _dx: int, dy: int) -> None:
#    if dy % 3:
#        # Only send key every 10 steps
#        return
#    if dy < 0:
#        qtile.spawn("wlrctl keyboard type +", shell=True)
#    else:
#        qtile.spawn("wlrctl keyboard type -", shell=True)
#
#
#mouse.append(
#    Swipe(
#        [],
#        3,
#        lazy.function(swipe_zoom).when(focused=Match(wm_class="firefox")),
#    )
#)

# Layouts
border_focus = [colours[5], "323974"]
border_normal = "001122"


class MyColumns(layout.Columns):
    """
    I only override this method so I can make 'foot' have wide margins at each side if
    it's the only window open.
    """

    def configure(self, client, screen_rect):
        pos = 0
        for col in self.columns:
            if client in col:
                break
            pos += col.width
        else:
            client.hide()
            return
        if client.has_focus:
            color = self.border_focus if col.split else self.border_focus_stack
        else:
            color = self.border_normal if col.split else self.border_normal_stack
        border = self.border_width
        margin_size = self.margin
        if len(self.columns) == 1 and (len(col) == 1 or not col.split):
            if not self.border_on_single:
                border = 0
            if "foot" in (client.get_wm_class() or []):
                margin_size = [0, 200, 0, 200]
        width = int(0.5 + col.width * screen_rect.width * 0.01 / len(self.columns))
        x = screen_rect.x + int(
            0.5 + pos * screen_rect.width * 0.01 / len(self.columns)
        )
        if col.split:
            pos = 0
            for c in col:
                if client == c:
                    break
                pos += col.heights[c]
            height = int(
                0.5 + col.heights[client] * screen_rect.height * 0.01 / len(col)
            )
            y = screen_rect.y + int(0.5 + pos * screen_rect.height * 0.01 / len(col))
            client.place(
                x,
                y,
                width - 2 * border,
                height - 2 * border,
                border,
                color,
                margin=margin_size,
            )
            client.unhide()
        elif client == col.cw:
            client.place(
                x,
                screen_rect.y,
                width - 2 * border,
                screen_rect.height - 2 * border,
                border,
                color,
                margin=margin_size,
            )
            client.unhide()
        else:
            client.hide()


# Weird custom behaviour here but isn't that what qtile is for?
# I want a Columns layout but also sometimes i want 'foot' windows to be thinner and
# centred in a 'central' column, so I define a whole new MyColumns layout that does that
# and I just jump between the two when I want that.
col_opts = dict(
    insert_position=1,
    border_width=5,
    border_focus=border_focus,
    border_normal="00000000",
    border_on_single=False,
    wrap_focus_columns=False,
    wrap_focus_rows=False,
    margin=0,
    # margin_on_single=30,  # 4
)

layouts = [
    MyColumns(**col_opts),
    layout.Columns(**col_opts),
]

floating_layout = layout.Floating(
    border_width=3,
    border_focus=border_focus,
    border_normal="00000000",
    fullscreen_border_width=0,
    float_rules=[
        Match(func=base.Window.has_fixed_size),
        Match(func=base.Window.has_fixed_ratio),
        Match(func=lambda c: bool(c.is_transient_for())),
        Match(role="gimp-file-export"),
        Match(title="Bluetooth Devices"),
        Match(title="File Operation Progress", wm_class=re.compile("[Tt]hunar")),
        Match(title="Firefox — Sharing Indicator"),
        Match(title="KDE Connect Daemon"),
        Match(title="Open File"),
        Match(title="Unlock Database - KeePassXC"),
        Match(title="KeePassXC -  Access Request"),
        Match(title=re.compile("Presenting: .*"), wm_class="libreoffice-impress"),
        Match(wm_class="Arandr"),
        Match(wm_class="Dragon"),
        Match(wm_class="Dragon-drag-and-drop"),
        Match(wm_class="Pinentry-gtk-2"),
        Match(wm_class="Xephyr"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="eog"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="imv"),
        Match(wm_class="io.github.celluloid_player.Celluloid"),
        Match(wm_class="lxappearance"),
        Match(wm_class="matplotlib"),
        #Match(wm_class="mpv"),
        Match(wm_class="nm-connection-editor"),
        Match(wm_class="notification"),
        Match(wm_class="org.gnome.clocks"),
        Match(wm_class="org.kde.ark"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="qt5ct"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="thunar"),
        Match(wm_class="toolbar"),
        Match(wm_class="tridactyl"),
        Match(wm_class="wdisplays"),
        Match(wm_class="wlroots"),
        Match(wm_class="zoom"),
        Match(wm_type="dialog"),
    ],
)


# Screens and Bars
widget_defaults = {
    "padding": 10,
    "foreground": colours[6],
    "font": "Font Awesome 5 Free",
    "fontsize": 16,
}

icon_font_size = 22

groupbox_config = {
    "active": foreground,
    "highlight_method": "block",
    "this_current_screen_border": colour_focussed,
    "other_current_screen_border": colours[5],
    "highlight_color": [background, colours[5]],
    "disable_drag": True,
    "padding": 4,
    "font": "TamzenForPowerline Bold",
    "fontsize": 12,
}

# mpd2 = widget.Mpd2(
#    no_connection="",
#    status_format="{artist} - {title}",
#    status_format_stopped="",
#    foreground=colours[12],
#    idle_format="",
#    font="TamzenForPowerline Bold",
#    update_interval=10,
#    scroll=True,
# )

mpd2 = widget.Mpris2(
    name="mpris",
    width=1000,
    objname=None,
    format="{xesam:title} - {xesam:artist}",
    font="TamzenForPowerline Bold",
)


class MyVolume(widget.Volume):
    def _configure(self, qtile, bar):
        widget.Volume._configure(self, qtile, bar)
        self.volume = self.get_volume()
        if self.volume <= 0:
            self.text = ""
        elif self.volume <= 15:
            self.text = ""
        elif self.volume < 50:
            self.text = ""
        else:
            self.text = ""

    def _update_drawer(self):
        if self.volume <= 0:
            self.text = ""
        elif self.volume <= 15:
            self.text = ""
        elif self.volume < 50:
            self.text = ""
        else:
            self.text = ""
        self.draw()

    def increase_vol(self):
        subprocess.run("amixer -c PCH set PCM 3%+".split(), capture_output=True)
        self.volume = self.get_volume()

    def decrease_vol(self):
        subprocess.run("amixer -c PCH set PCM 3%-".split(), capture_output=True)
        self.volume = self.get_volume()

    def mute(self):
        subprocess.run("amixer -c PCH set PCM toggle".split(), capture_output=True)
        self.volume = self.get_volume()


bklight = widget.Backlight(
    backlight_name=os.listdir("/sys/class/backlight")[-1],
    step=1,
    update_interval=None,
    format="",
    fontsize=icon_font_size,
    change_command=None,
)

volume = MyVolume(
    fontsize=icon_font_size,
    channel="PCM",
    font="Font Awesome 5 Free",
    update_interval=60,
    cardid="PCH",
    device=None,
)

if IS_WAYLAND:
    systray = widget_extras.StatusNotifier(padding=20)
else:
    systray = widget.Systray(padding=20, icon_size=24)


class MyBattery(Battery):
    """
    This is basically the Battery widget except it uses some icons, and if you click it
    it will show the percentage numerically for 1 second.
    """

    def build_string(self, status):
        if self.layout is not None:
            self.layout.colour = self.foreground
            if (
                status.state == BatteryState.DISCHARGING
                and status.percent < self.low_percentage
            ):
                self.background = self.low_background
            else:
                self.background = self.normal_background
        if status.state == BatteryState.DISCHARGING:
            if status.percent > 0.75:
                char = ""
            elif status.percent > 0.45:
                char = ""
            elif status.percent > 0.25:
                char = ""
            else:
                char = ""
        elif status.percent >= 1 or status.state == BatteryState.FULL:
            char = ""
        elif status.state == BatteryState.EMPTY or (
            status.state == BatteryState.UNKNOWN and status.percent == 0
        ):
            char = ""
        else:
            char = ""
        return self.format.format(char=char, percent=status.percent)

    def restore(self):
        self.format = "{char}"
        self.font = "Font Awesome 5 Free"
        self.timer_setup()

    def button_press(self, x, y, button):
        self.format = "{percent:2.0%}"
        self.font = "TamzenForPowerline Bold"
        self.timer_setup()
        self.timeout_add(1, self.restore)


battery = MyBattery(
    format="{char}",
    low_background=colours[1],
    show_short_text=False,
    low_percentage=0.12,
    notify_below=12,
    fontsize=icon_font_size + 10,
)

date = widget.Clock(
    format="%e/%m/%g",
    fontsize=16,
    font="TamzenForPowerline Bold",
    update_interval=60,
    name="date",
)

time = widget.Clock(
    fontsize=20,
    font="TamzenForPowerline Medium",
    update_interval=60,
    name="time",
)

groupboxes = [
    widget.GroupBox(**groupbox_config),
    widget.GroupBox(**groupbox_config, visible_groups=["q", "w", "e", "r"]),
]


@hook.subscribe.startup
def _():
    # Set up initial GroupBox visible groups
    if len(qtile.screens) > 1:
        groupboxes[0].visible_groups = ["1", "2", "3", "4"]
    else:
        groupboxes[0].visible_groups = None


@hook.subscribe.screens_reconfigured
def _():
    # Reconfigure GroupBox visible groups
    if len(qtile.screens) > 1:
        groupboxes[0].visible_groups = ["1", "2", "3", "4"]
    else:
        groupboxes[0].visible_groups = None
    if hasattr(groupboxes[0], "bar"):
        groupboxes[0].bar.draw()


#bar_border_width = [0, 3, 0, 3]
#bar_border_color = ["000000", colours[5], "000000", colours[5]]

screens = [
    Screen(
        top=bar.Bar(
            [
                groupboxes[0],
                widget.Spacer(name="s1"),
                mpd2,
                widget.Spacer(name="s2"),
                systray,
                volume,
                bklight,
                battery,
                date,
                time,
            ],
            28,
            background=background,
        ),
        bottom=bar.Gap(outer_gaps),
        left=bar.Gap(outer_gaps),
        right=bar.Gap(outer_gaps),
        #wallpaper="~/pictures/Wallpapers/fractal.bmp",
        #wallpaper_mode="fill",
    ),
    Screen(
        top=bar.Bar(
            [
                groupboxes[1],
                widget.Spacer(name="s3"),
                mpd2,
                widget.Spacer(name="s4"),
                volume,
                bklight,
                battery,
                date,
                time,
            ],
            28,
            background=background,
        ),
        #wallpaper="~/pictures/Wallpapers/fractal.bmp",
        #wallpaper_mode="fill",
        bottom=bar.Gap(outer_gaps),
        left=bar.Gap(outer_gaps),
        right=bar.Gap(outer_gaps),
    ),
]


@hook.subscribe.client_focus
def _(_):
    # Keep Static windows on top
    for window in qtile.windows_map.values():
        if isinstance(window, base.Static):
            window.bring_to_front()


reconfigure_screens = True
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "focus"

keys = [Key(mods, key, cmd, desc=desc) for mods, key, cmd, desc in my_keys]
groups.append(scratchpad)
