"""
Qtile main config file
======================
"""

from __future__ import annotations

import asyncio
import os
import sys
import subprocess
from functools import partial
from typing import TYPE_CHECKING

from libqtile import layout, hook, bar, widget, qtile
from libqtile.config import Key, EzKey, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.widget.backlight import ChangeDirection

import traverse
from groups import groups, keys_group

if TYPE_CHECKING:
    from typing import List, Tuple


## Basic vars
IS_WAYLAND = qtile.core.name == "wayland"

if IS_WAYLAND:
    term = 'footclient'
else:
    term = 'xterm'

xephyr = int(os.environ.get("QTILE_XEPHYR", 0))
if xephyr:
    mod = "mod1"
    alt = "control"
    if not IS_WAYLAND:
        # urxvt doesn't like xephyr
        term = 'xterm'
else:
    mod = "mod4"
    alt = "mod1"

HOME = os.path.expanduser('~')

## Colours
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
bw = 5
cw = 5
colour_focussed = '#6fa3e0'
colour_unfocussed = '#0e101c'
inner_gaps = 4
outer_gaps = 4

# https://coolors.co/1b2021-cfccd6-bbc2e2-b7b5e4-847979


## Keys


@lazy.function
def float_to_front(qtile):
    """ Bring all floating windows of the group to front """
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()


my_keys: Tuple[List[str], str, Any, str] = [
    # Window management
    ([mod, 'control'],  'q',        lazy.window.kill(),                 "Close window"),
    ([mod],             'f',        lazy.window.toggle_fullscreen(),    "Toggle fullscreen"),
    ([mod, 'shift'],    'space',    lazy.window.toggle_floating(),      "Toggle floating"),
    ([mod],             'space',    float_to_front,                     "Move floating windows to the front"),
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
    ([mod, 'shift'],    'r',        lazy.restart(),                     "Restart Qtile"),
    ([mod],             'Tab',      lazy.next_layout(),                 "Next layout"),
    ([mod, 'control'],  'h',        lazy.window.toggle_minimize(),      "Minimise window"),
    ([mod],             's',        lazy.window.static(),               "Make window static"),
    ([mod, 'control'],  'Escape',   lazy.shutdown(),                    "Shutdown Qtile"),

    # Volume control
    ([], 'XF86AudioMute',         lazy.widget['myvolume'].mute(),         "Mute audio"),
    ([], 'F10',                   lazy.widget['myvolume'].mute(),         "Mute audio"),
    ([], 'XF86AudioRaiseVolume',  lazy.widget['myvolume'].increase_vol(), "Increase volume"),
    ([], 'F12',                   lazy.widget['myvolume'].increase_vol(), "Increase volume"),
    ([], 'XF86AudioLowerVolume',  lazy.widget['myvolume'].decrease_vol(), "Decrease volume"),
    ([], 'F11',                   lazy.widget['myvolume'].decrease_vol(), "Decrease volume"),

    # Backlight control
    ([], 'XF86MonBrightnessUp',   lazy.widget['backlight'].change_backlight(ChangeDirection.UP, 3),   "Increase backlight"),
    ([], 'XF86MonBrightnessDown', lazy.widget['backlight'].change_backlight(ChangeDirection.DOWN, 3), "Decrease backlight"),
    ([], 'F6',                    lazy.widget['backlight'].change_backlight(ChangeDirection.UP, 3),   "Increase backlight"),
    ([], 'F5',                    lazy.widget['backlight'].change_backlight(ChangeDirection.DOWN, 3), "Decrease backlight"),

    # Launchers
    ([mod],             'Return',   lazy.spawn(term),                           "Spawn terminal"),
    ([mod, 'shift'],    'f',        lazy.spawn("firefox"),                      "Spawn Firefox"),
    ([mod, 'control'],  'f',        lazy.spawn("tor-browser --allow-remote") ,  "Spawn Tor Browser"),
    ([],                'Print',    lazy.spawn("screenshot copy"),              "Screenshot to clipboard"),
    (['shift'],         'Print',    lazy.spawn('screenshot'),                   "Screenshot to file"),
    ([mod],             'p',        lazy.spawn('get_password_rofi'),            "Keepass passwords"),
    ([mod],             'i',        lazy.spawn('systemctl suspend -i'),         "Suspend system"),
]


# Backend-specific launchers
if IS_WAYLAND:
    my_keys.extend([
        ([mod], 'd', lazy.spawn('wofi --gtk-dark --show run'), "wofi: run"),
    ])

else:
    my_keys.extend([
        ([mod],             'd',    lazy.spawn('rofi -show run -theme ~/.config/rofi/common-large.rasi'), "rofi: run"),
        ([],    'XF86PowerOff',     lazy.spawn('power-menu'),                   "Power menu"),
        ([mod, 'shift'],    'x',    lazy.spawn('set_monitors'),                 "Configure monitors"),
        ([mod, 'shift'],    'i',    lazy.spawn('slock systemctl suspend -i'),   "Suspend system and lock"),
    ])


# Changing VT
if IS_WAYLAND:
    my_keys.extend([
        ([mod], 'F1',     lazy.change_vt(1),    "Change to VT 1"),
        ([mod], 'F2',     lazy.change_vt(2),    "Change to VT 2"),
        ([mod], 'F3',     lazy.change_vt(3),    "Change to VT 3"),
        ([mod], 'F4',     lazy.change_vt(4),    "Change to VT 4"),
        ([mod], 'F5',     lazy.change_vt(5),    "Change to VT 5"),
        ([mod], 'F6',     lazy.change_vt(6),    "Change to VT 6"),
    ])


## Mouse control
mouse = [
    Drag([mod], "Button1",      lazy.window.set_position_floating(),    start=lazy.window.get_position()),
    Drag([mod, alt], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button4",     lazy.layout.grow_up()),
    Click([mod], "Button5",     lazy.layout.grow_down()),
]


## Layouts
border_focus = [colours[13], colours[5]]
#border_focus = colours[13]
border_normal = background
#border_normal = colours[8]
border_width = 6

#import qtools.borders
#qtools.borders.enable('cde')
#border_focus = [border_focus, colours[5]]
#border_normal = [colours[0], colours[8]]


layouts = [
    layout.Columns(
        insert_position = 1,
        border_width = border_width,
        border_focus = border_focus,
        border_normal = border_normal,
        border_on_single = True,
        wrap_focus_columns = False,
        wrap_focus_rows = False,
        margin = inner_gaps,
        corner_radius = cw,
    ),
    layout.Max(),
]

floating_layout = layout.Floating(
    border_width = border_width,
    border_focus = border_focus,
    border_normal = border_normal,
    corner_radius = cw,
    float_rules=[
        Match(title='wlroots - X11-1'),
        Match(title='wlroots - X11-2'),
        Match(title='Open File'),
        Match(wm_class='Arandr'),
        Match(wm_class='confirm'),
        Match(wm_class='dialog'),
        Match(wm_class='download'),
        Match(wm_class='Dragon'),
        Match(wm_class='error'),
        Match(wm_class='fiji-Main'),
        Match(wm_class='file_progress'),
        Match(wm_class='fontforge'),
        Match(wm_class='imv'),
        Match(wm_class='love'),
        Match(wm_class='lxappearance'),
        Match(wm_class='mpv'),
        Match(wm_class='Nm-connection-editor'),
        Match(wm_class='notification'),
        Match(wm_class='Oomox'),
        Match(wm_class='Pavucontrol'),
        Match(wm_class='Pinentry-gtk-2'),
        Match(wm_class='qt5ct'),
        Match(wm_class='ssh-askpass'),
        Match(wm_class='tinyterm'),
        Match(wm_class='Dragon-drag-and-drop'),
        Match(wm_class='toolbar'),
        Match(wm_class='Xephyr'),
        Match(wm_type='dialog'),
        Match(role='gimp-file-export'),
        Match(func=lambda c: c.has_fixed_size()),
        Match(func=lambda c: bool(c.is_transient_for())),
    ]
)


## Screens and Bars
widget_defaults = {
    'padding': 10,
    'foreground': foreground,
    'font': 'Font Awesome 5 Free',
    'fontsize': 16,
}

groupbox_config = {
    'active': foreground,
    'highlight_method': 'line',
    'this_current_screen_border': colour_focussed,
    'other_current_screen_border': colours[5],
    'highlight_color': [background, colours[5]],
    'disable_drag': True,
    'padding': 8,
}

mpd2 = widget.Mpd2(
    no_connection='',
    status_format='{artist} - {title}',
    status_format_stopped='',
    foreground=colours[12],
    idle_format='',
    fontsize=16,
    font='TamzenForPowerline Bold',
    update_interval=10,
)
 
cpugraph = widget.CPUGraph(
    graph_color=colours[12],
    fill_color=colour_unfocussed,
    border_width=0,
    margin_x=10,
    margin_y=4,
    samples=50,
    line_width=4,
    width=200,
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

        self.wob = "/tmp/wob-" + qtile.core.display_name

    def _update_drawer(self):
        if self.volume <= 0:
            self.text = ''
        elif self.volume <= 15:
            self.text = ''
        elif self.volume < 50:
            self.text = ''
        else:
            self.text = ''
        self.draw()
        with open(self.wob, 'a') as f:
            f.write(str(self.volume) + "\n")

    def cmd_increase_vol(self):
        subprocess.call('amixer set PCM 4%+'.split())
        self.volume = self.get_volume()
        self._update_drawer()
    def cmd_decrease_vol(self):
        subprocess.call('amixer set PCM 4%-'.split())
        self.volume = self.get_volume()
        self._update_drawer()
    def cmd_mute(self):
        subprocess.call('amixer set Master toggle'.split())
        self.channel = 'Master'
        self.volume = self.get_volume()
        self.channel = 'PCM'
        if self.volume == 0:
            self.volume = self.get_volume()
        self._update_drawer()

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
    mouse_callbacks={
        'Button1': partial(qtile.cmd_spawn, 'nm-connection-editor'),
    },
    foreground=colours[5],
    update_interval=5,
)

from libqtile.widget.battery import Battery, BatteryState
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
        old = self.format
        self.format = '{percent:2.0%}'
        self.font='TamzenForPowerline Bold'
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

screens = [
    Screen(
        bottom=bar.Bar(
            [
                groupboxes[0], cpugraph, widget.Spacer(), mpd2,
                widget.Spacer(), systray, bklight, volume, wlan,
                battery, date, time, 
            ],
            32,
            background=background,
        ),
        top=bar.Gap(outer_gaps),
        left=bar.Gap(outer_gaps),
        right=bar.Gap(outer_gaps),
    ),
    Screen(
        bottom=bar.Bar(
            [
                groupboxes[1], cpugraph, widget.Spacer(), mpd2,
                widget.Spacer(), bklight, volume, wlan,
                battery, date, time
            ],
            32,
            background=background,
        ),
        top=bar.Gap(outer_gaps),
        left=bar.Gap(outer_gaps),
        right=bar.Gap(outer_gaps),
    ),
]


# Dropdowns and Scratchpad

dd_defaults = {
    "warp_pointer": False,
    "on_focus_lost_hide": True,
    "opacity": 1,
}

if IS_WAYLAND:
    dropdowns = [
        DropDown("tmux", "foot tmux", height=0.4, **dd_defaults),
        DropDown("email", f"foot -D {HOME}/Downloads mutt", x=0.1, y=0.05, width=0.8, height=0.9, **dd_defaults),
        DropDown("irc", "foot irc", x=0.1, y=0.05, width=0.8, height=0.9, **dd_defaults),
        DropDown("ncmpcpp", "foot ncmpcpp", x=0.12, y=0.2, width=0.56, height=0.7, **dd_defaults),
        DropDown("python", "foot python", x=0.05, y=0.1, width=0.2, height=0.3, **dd_defaults),
        #DropDown("newsboat", "foot newsboat", x=0.2, y=0.05, width=0.6, height=0.9, **dd_defaults),
    ]
else:
    dropdowns = [
        DropDown("tmux", "urxvt -e tmux", height=0.4, **dd_defaults),
        DropDown("email", f"urxvt -cd {HOME}/Downloads -e mutt", x=0.1, y=0.05, width=0.8, height=0.9, **dd_defaults),
        DropDown("irc", "urxvt -b 100 -e irc", x=0.1, y=0.05, width=0.8, height=0.9, **dd_defaults),
        DropDown("ncmpcpp", "urxvt -e ncmpcpp", x=0.12, y=0.2, width=0.56, height=0.7, **dd_defaults),
        DropDown("python", "urxvt -e python", x=0.05, y=0.1, width=0.2, height=0.3, **dd_defaults),
        #DropDown("newsboat", "urxvt -e newsboat", x=0.2, y=0.05, width=0.6, height=0.9, **dd_defaults),
    ]

groups.append(ScratchPad("scratchpad", dropdowns))

my_keys.extend([
    ([mod, 'shift'],     'Return',   lazy.group['scratchpad'].dropdown_toggle('tmux'), "Toggle tmux scratchpad"),
    ([mod, 'control'],   'e',        lazy.group['scratchpad'].dropdown_toggle('email'), "Toggle email scratchpad"),
    ([mod, 'control'],   'w',        lazy.group['scratchpad'].dropdown_toggle('irc'), "Toggle irc scratchpad"),
    ([mod, 'control'],   'm', lazy.group['scratchpad'].dropdown_toggle('ncmpcpp'), "Toggle ncmpcpp scratchpad"),
    ([mod],              'c',        lazy.group['scratchpad'].dropdown_toggle('python'), "Toggle python scratchpad"),
    #([mod, 'control'],   'n', lazy.group['scratchpad'].dropdown_toggle('newsboat'), "Toggle newsboat scratchpad"),
])


# Hooks

@hook.subscribe.startup
def _():
    # Set initial groups
    if len(qtile.screens) > 1:
        qtile.groups_map['1'].cmd_toscreen(0, toggle=False)
        qtile.groups_map['q'].cmd_toscreen(1, toggle=False)
        groupboxes[0].visible_groups = ['1', '2', '3']
    else:
        groupboxes[0].visible_groups = ['1', '2', '3', 'q', 'w', 'e']


if IS_WAYLAND:
    from libqtile.backend.wayland.window import Window
    @hook.subscribe.client_new
    def _(window):
        # Auto-float windows
        if type(window) is Window:
            state = window.surface.toplevel._ptr.current
            if 0 < state.max_width < 1920:
                window.floating = True
            else:
                # Just incase I find something new I want to auto-float
                logger.warning(
                    (window.name, window.get_wm_class(), (state.min_width, state.max_width))
                )

else:
    @hook.subscribe.client_new
    def _(window):
        # Auto-float windows
        hints = window.window.get_wm_normal_hints()
        if hints and 0 < hints['max_width'] < 1920:
            window.floating = True


@hook.subscribe.screen_change
async def _(_):
    # Set up GroupBox visible groups
    await asyncio.sleep(1)
    if len(qtile.screens) > 1:
        groupboxes[0].visible_groups = ['1', '2', '3']
        if qtile.screens[0].group.name not in "123":
            qtile.groups_map['1'].cmd_toscreen(0, toggle=False)
        qtile.groups_map['q'].cmd_toscreen(1, toggle=False)
    else:
        groupboxes[0].visible_groups = ['1', '2', '3', 'q', 'w', 'e']
    if hasattr(groupboxes[0], 'bar'):
        groupboxes[0].bar.draw()


## Startup script for Wayland
if IS_WAYLAND:
    @hook.subscribe.startup_once
    async def _():
        env = os.environ.copy()
        env["WOB_HEIGHT"] = "32"
        env["WOB_WIDTH"] = "1920"
        env["WOB_MARGIN"] = "0"
        env["WOB_OFFSET"] = "0"
        env["WOB_BORDER"] = "0"
        env["WOB_PADDING"] = "0"
        env["WOB_BACKGROUND"] = "#00000000"
        env["WOB_BAR"] = "#ff" + foreground[1:]
        subprocess.Popen(f"{HOME}/.config/qtile/startup.sh", shell=True, env=env)

    if xephyr:
        # To adapt to whatever window size it was given
        hook.subscribe.startup_once(qtile.cmd_reconfigure_screens)


## General settings
reconfigure_screens = True
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = 'smart'
wmname = 'LG3D'


# Reformat keys
my_keys.extend(keys_group)
keys = [Key(mods, key, cmd, desc=desc) for mods, key, cmd, desc in my_keys]


# Configure libinput devices
if IS_WAYLAND:
    from libqtile.backend.wayland import InputConfig

    wayland_libinput_config = {
        "type:pointer": InputConfig(drag=True, tap=True)
    }
