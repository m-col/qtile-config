"""
Qtile main config file
======================
"""

from __future__ import annotations

import asyncio
import importlib
import os
import subprocess
import sys
from typing import TYPE_CHECKING

from libqtile import bar, hook, layout, qtile, widget
from libqtile.backend import base
from libqtile.config import Drag, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.widget.backlight import ChangeDirection
from libqtile.widget.battery import Battery, BatteryState

if TYPE_CHECKING:
    from typing import Any, List, Tuple

    from libqtile.core.manager import Qtile


# Config imports
def reload(module):
    if module in sys.modules:
        importlib.reload(sys.modules[module])

import traverse

reload("groups")
from groups import groups, keys_group

reload("scratchpad")
from scratchpad import keys_scratchpad, scratchpad

IS_WAYLAND: bool = qtile.core.name == "wayland"
IS_XEPHYR: bool = int(os.environ.get("QTILE_XEPHYR", 0)) > 0

reload(qtile.core.name)
if IS_WAYLAND:
    from wayland import keys_backend, term, wayland_libinput_config  # noqa: F401
else:
    from x11 import keys_backend, term, wmname  # noqa: F401


# Colours
theme = dict(
    foreground='#CFCCD6',
    background='#1B2021',
    color0='#030405',
    color8='#1f1c32',
    color1='#8742a5',
    color9='#9a5eb3',
    color2='#406794',
    color10='#5fd75f',
    color3='#653c21',
    color11='#6e9fcd',
    color4='#8f4ff0',
    color12='#BBC2E2',
    color5='#5d479d',
    color13='#998dd1',
    color6='#3e3e73',
    color14='#9a9dcc',
    color7='#495068',
    color15='#e1e1e4',
)

colours = [theme[f'color{n}'] for n in range(16)]
background = theme['background']
foreground = theme['foreground']
bw = 6
cw = 5
colour_focussed = '#6fa3e0'
colour_unfocussed = '#0e101c'
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
my_keys: List[Tuple[List[str], str, Any, str]] = []
my_keys.extend(keys_backend)
my_keys.extend(keys_group)
my_keys.extend(keys_scratchpad)


def float_to_front(qtile: Qtile) -> None:
    """ Bring all floating windows of the group to front """
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()


my_keys.extend([
    # Window management
    ([mod, 'control'],  'q',        lazy.window.kill(),                 "Close window"),
    ([mod],             'f',        lazy.window.toggle_fullscreen(),    "Toggle fullscreen"),
    ([mod, 'shift'],    'space',    lazy.window.toggle_floating(),      "Toggle floating"),
    ([mod],             'space',    lazy.function(float_to_front),      "Move floating windows to the front"),
    ([mod],             'j',        lazy.function(traverse.down),       "Traverse down"),
    ([mod],             'k',        lazy.function(traverse.up),         "Traverse up"),
    ([mod],             'h',        lazy.function(traverse.left),       "Traverse left"),
    ([mod],             'l',        lazy.function(traverse.right),      "Traverse right"),
    ([mod, 'shift'],    'j',        lazy.layout.shuffle_down(),         "Shuffle down"),
    ([mod, 'shift'],    'k',        lazy.layout.shuffle_up(),           "Shuffle up"),
    ([mod, 'shift'],    'h',        lazy.layout.shuffle_left(),         "Shuffle left"),
    ([mod, 'shift'],    'l',        lazy.layout.shuffle_right(),        "Shuffle right"),
    ([mod, alt],        'j',        lazy.layout.grow_down(),            "Grow down"),
    ([mod, alt],        'k',        lazy.layout.grow_up(),              "Grow up"),
    ([mod, alt],        'h',        lazy.layout.grow_left(),            "Grow left"),
    ([mod, alt],        'l',        lazy.layout.grow_right(),           "Grow right"),
    ([mod, 'shift'],    'r',        lazy.reload_config(),               "Reload the config"),
    ([mod, 'control'],  'r',        lazy.restart(),                     "Restart Qtile"),
    ([mod],             'Tab',      lazy.next_layout(),                 "Next layout"),
    ([mod, 'control'],  'h',        lazy.window.toggle_minimize(),      "Minimise window"),
    ([mod],             's',        lazy.window.static(),               "Make window static"),
    ([mod, 'control'],  'Escape',   lazy.shutdown(),                    "Shutdown Qtile"),

    # Volume control - MyVolume widget is defined further down
    ([], 'XF86AudioMute',         lazy.widget['myvolume'].mute(),         "Mute audio"),
    ([], 'F10',                   lazy.widget['myvolume'].mute(),         "Mute audio"),
    ([], 'XF86AudioRaiseVolume',  lazy.widget['myvolume'].increase_vol(), "Increase volume"),
    ([], 'F12',                   lazy.widget['myvolume'].increase_vol(), "Increase volume"),
    ([], 'XF86AudioLowerVolume',  lazy.widget['myvolume'].decrease_vol(), "Decrease volume"),
    ([], 'F11',                   lazy.widget['myvolume'].decrease_vol(), "Decrease volume"),

    # Backlight control
    ([], 'XF86MonBrightnessUp',
        lazy.widget['backlight'].change_backlight(ChangeDirection.UP, 5),   "Increase backlight"),
    ([], 'XF86MonBrightnessDown',
        lazy.widget['backlight'].change_backlight(ChangeDirection.DOWN, 5), "Decrease backlight"),
    ([], 'F6',
        lazy.widget['backlight'].change_backlight(ChangeDirection.UP, 5),   "Increase backlight"),
    ([], 'F5',
        lazy.widget['backlight'].change_backlight(ChangeDirection.DOWN, 5), "Decrease backlight"),

    # Launchers
    ([mod],             'd',        lazy.spawncmd(),                            "Spawn with Prompt"),
    ([mod],             'Return',   lazy.spawn(term),                           "Spawn terminal"),
    ([mod, 'shift'],    'f',        lazy.spawn("firefox"),                      "Spawn Firefox"),
    ([mod, 'control'],  'f',        lazy.spawn("tor-browser --allow-remote"),   "Spawn Tor Browser"),
    ([],                'Print',    lazy.spawn("screenshot copy"),              "Screenshot to clipboard"),
    (['shift'],         'Print',    lazy.spawn('screenshot'),                   "Screenshot to file"),
    ([mod],             'p',        lazy.spawn('get_password_rofi'),            "Keepass passwords"),
    ([mod],             'i',        lazy.spawn('systemctl suspend -i'),         "Suspend system"),
])


# Mouse control
mouse = [
    Drag([mod], "Button1",      lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod, alt], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]


# Layouts
border_focus = [colours[13], colours[5]]
border_normal = background

#import qtools.borders
#qtools.borders.enable('cde')
#border_focus = [border_focus, colours[5]]
#border_normal = [colours[0], colours[8]]


layouts = [
    layout.Columns(
        insert_position=1,
        border_width=bw,
        border_focus=border_focus,
        border_normal=border_normal,
        border_on_single=False,
        wrap_focus_columns=False,
        wrap_focus_rows=False,
        margin=inner_gaps,
        margin_on_single=0,
        corner_radius=cw,
    ),
]

floating_layout = layout.Floating(
    border_width=bw,
    border_focus=border_focus,
    border_normal=border_normal,
    corner_radius=cw,
    float_rules=[
        Match(title='Open File'),
        Match(title='Unlock Database - KeePassXC'),  # Wayland
        Match(title='File Operation Progress', wm_class='thunar'),  # Wayland
        Match(wm_class='Arandr'),
        Match(wm_class='org.kde.ark'),
        Match(wm_class='confirm'),
        Match(wm_class='dialog'),
        Match(wm_class='download'),
        Match(wm_class='error'),
        Match(wm_class='fiji-Main'),
        Match(wm_class='file_progress'),
        Match(wm_class='imv'),
        Match(wm_class='lxappearance'),
        Match(wm_class='mpv'),
        Match(wm_class='notification'),
        Match(wm_class='pavucontrol'),
        Match(wm_class='Pinentry-gtk-2'),
        Match(wm_class='qt5ct'),
        Match(wm_class='ssh-askpass'),
        Match(wm_class='Dragon'),
        Match(wm_class='Dragon-drag-and-drop'),
        Match(wm_class='toolbar'),
        Match(wm_class='wlroots'),
        Match(wm_class='Xephyr'),
        Match(wm_type='dialog'),
        Match(role='gimp-file-export'),
        Match(func=lambda c: c.has_fixed_size()),
        Match(func=lambda c: bool(c.is_transient_for())),
    ]
)


# Screens and Bars
widget_defaults = {
    'padding': 10,
    'foreground': foreground,
    'font': 'Font Awesome 5 Free',
    'fontsize': 16,
}

groupbox_config = {
    'active': foreground,
    'highlight_method': 'block',
    'this_current_screen_border': colour_focussed,
    'other_current_screen_border': colours[5],
    'highlight_color': [background, colours[5]],
    'disable_drag': True,
    'padding': 4,
    'font': 'TamzenForPowerline Bold',
    'fontsize': 12,
}

mpd2 = widget.Mpd2(
    no_connection='',
    status_format='mpd here' if IS_XEPHYR else '{artist} - {title}',
    status_format_stopped='',
    foreground=colours[12],
    idle_format='',
    font='TamzenForPowerline Bold',
    update_interval=10,
)
import libqtile.widget.mpd2widget
mpd2.mouse_buttons = {v:k for k, v in widget.mpd2widget.keys.items()}

cpugraph = widget.CPUGraph(
    graph_color=colours[12],
    fill_color=colour_unfocussed,
    border_width=0,
    margin_x=10,
    margin_y=4,
    samples=50,
    line_width=4,
    width=50 if IS_XEPHYR else 200,
    type='box',
    frequency=1,
)

bklight = widget.Backlight(
    backlight_name=os.listdir('/sys/class/backlight')[0],
    step=1,
    update_interval=None,
    format="",
    change_command=None,
    foreground=colours[3],
)


class MyVolume(widget.Volume):
    def _configure(self, qtile, bar):
        widget.Volume._configure(self, qtile, bar)
        self.volume = self.get_volume()
        if self.volume <= 0:
            self.text = ''
        elif self.volume <= 15:
            self.text = ''
        elif self.volume < 50:
            self.text = ''
        else:
            self.text = ''
        # drawing here crashes Wayland

        if IS_WAYLAND:
            self.wob = "/tmp/wob-" + qtile.core.display_name

    def _update_drawer(self, wob=False):
        if self.volume <= 0:
            self.text = ''
        elif self.volume <= 15:
            self.text = ''
        elif self.volume < 50:
            self.text = ''
        else:
            self.text = ''
        self.draw()

        if wob:
            with open(self.wob, 'a') as f:
                f.write(str(self.volume) + "\n")

    def cmd_increase_vol(self):
        subprocess.call('amixer set PCM 4%+'.split())
        self.volume = self.get_volume()
        self._update_drawer(wob=IS_WAYLAND)

    def cmd_decrease_vol(self):
        subprocess.call('amixer set PCM 4%-'.split())
        self.volume = self.get_volume()
        self._update_drawer(wob=IS_WAYLAND)

    def cmd_mute(self):
        subprocess.call('amixer set Master toggle'.split())
        self.channel = 'Master'
        self.volume = self.get_volume()
        self.channel = 'PCM'
        if self.volume == 0:
            self.volume = self.get_volume()
        self._update_drawer(wob=False)


volume = MyVolume(
    fontsize=18,
    channel='PCM',
    font='Font Awesome 5 Free',
    foreground=colours[4],
    update_interval=60,
)

if IS_WAYLAND:
    systray = widget.TextBox('')
else:
    systray = widget.Systray(padding=20)

wlan = widget.Wlan(
    format='',
    disconnected_message='',
    foreground=colours[5],
    update_interval=5,
)


class MyBattery(Battery):
    def build_string(self, status):
        if self.layout is not None:
            if status.state == BatteryState.DISCHARGING and status.percent < self.low_percentage:
                self.layout.colour = self.low_foreground
            else:
                self.layout.colour = self.foreground
        if status.state == BatteryState.DISCHARGING:
            if status.percent > 0.75:
                char = ''
            elif status.percent > 0.45:
                char = ''
            else:
                char = ''
        elif status.percent >= 1 or status.state == BatteryState.FULL:
            char = ''
        elif status.state == BatteryState.EMPTY or \
                (status.state == BatteryState.UNKNOWN and status.percent == 0):
            char = ''
        else:
            char = ''
        return self.format.format(char=char, percent=status.percent)

    def restore(self):
        self.format = '{char}'
        self.font = 'Font Awesome 5 Free'
        self.timer_setup()

    def button_press(self, x, y, button):
        self.format = '{percent:2.0%}'
        self.font = 'TamzenForPowerline Bold'
        self.timer_setup()
        self.timeout_add(1, self.restore)


battery = MyBattery(
    format='{char}',
    low_foreground=colours[1],
    show_short_text=False,
    low_percentage=0.12,
    foreground=colours[6],
    notify_below=12,
)

date = widget.Clock(
    format='%e/%m/%g',
    fontsize=16,
    font='TamzenForPowerline Bold',
    foreground=colours[7],
    update_interval=60,
)
time = widget.Clock(
    fontsize=20,
    font='TamzenForPowerline Medium',
    update_interval=60,
)

groupboxes = [
    widget.GroupBox(**groupbox_config, visible_groups=['1', '2', '3', 'q', 'w', 'e']),
    widget.GroupBox(**groupbox_config, visible_groups=['q', 'w', 'e']),
]


@hook.subscribe.startup
def _():
    # Set up initial GroupBox visible groups
    if len(qtile.screens) > 1:
        groupboxes[0].visible_groups = ['1', '2', '3']
    else:
        groupboxes[0].visible_groups = ['1', '2', '3', 'q', 'w', 'e']


@hook.subscribe.client_focus
def _(_):
    # Keep Static windows on top
    for window in qtile.windows_map.values():
        if isinstance(window, base.Static):
            if hasattr(window, "cmd_bring_to_front"):
                window.cmd_bring_to_front()


@hook.subscribe.screen_change
async def _(_):
    # Reconfigure GroupBox visible groups
    await asyncio.sleep(1)  # Am I gonna fix this?
    if len(qtile.screens) > 1:
        groupboxes[0].visible_groups = ['1', '2', '3']
    else:
        groupboxes[0].visible_groups = ['1', '2', '3', 'q', 'w', 'e']
    if hasattr(groupboxes[0], 'bar'):
        groupboxes[0].bar.draw()


prompt = widget.Prompt(
    fontsize=20,
    font='TamzenForPowerline Medium',
    cursor_color=foreground,
    visual_bell_color=foreground,
    background=colours[5],
    bell_style='visual',
)

screens = [
    Screen(
        bottom=bar.Bar(
            [
                groupboxes[0], cpugraph, prompt, # Left
                widget.Spacer(),
                mpd2, # Centre
                widget.Spacer(),
                systray, bklight, volume, wlan, battery, date, time,  # Right
            ],
            28,
            background=background,
        ),
        top=bar.Gap(outer_gaps),
        left=bar.Gap(outer_gaps),
        right=bar.Gap(outer_gaps),
        wallpaper="~/pictures/Wallpapers/qtile-wallpaper.png",
    ),
    Screen(
        bottom=bar.Bar(
            [
                groupboxes[1], cpugraph, prompt,  # Left
                widget.Spacer(),
                mpd2, # Centre
                widget.Spacer(),
                bklight, volume, wlan, battery, date, time,  # Right
            ],
            28,
            background=background,
        ),
        wallpaper="~/pictures/Wallpapers/qtile-wallpaper.png",
        wallpaper_mode="fill",
        top=bar.Gap(outer_gaps),
        left=bar.Gap(outer_gaps),
        right=bar.Gap(outer_gaps),
    ),
]


# Notification server
if True:
    reload("notification")
    import notification

# Remove defunct callbacks left when reloading the config
    import libqtile.notify
    libqtile.notify.notifier.callbacks.clear()
    libqtile.notify.notifier.close_callbacks.clear()

    notifier = notification.Server(
        background=colours[12],
        foreground=background,
        x=50,
        y=50,
        width=320,
        height=100,
        font_size=18,
        font='TamzenForPowerline Bold',
    )

    my_keys.extend([
        ([mod],             'grave',    notifier.lazy_prev,     "Previous notification"),
        ([mod, 'shift'],    'grave',    notifier.lazy_next,     "Next notification"),
        (['control'],       'space',    notifier.lazy_close,    "Close notification"),
    ])



# Config variables
reconfigure_screens = True
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = 'smart'
keys = [Key(mods, key, cmd, desc=desc) for mods, key, cmd, desc in my_keys]
groups.append(scratchpad)
