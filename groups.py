"""
Groups
======

 - 6 groups
 - 3 bound to each screen when using two monitors

"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from libqtile import hook, qtile
from libqtile.config import Group, Match
from libqtile.lazy import lazy

if TYPE_CHECKING:
    from typing import Any, Callable, List, Tuple

    from libqtile.core.manager import Qtile


mod = "mod1" if int(os.environ.get("QTILE_XEPHYR", 0)) else "mod4"

keys_group: Tuple[List[str], str, Any, str] = []


groups: List[Group] = [
    Group('1', label='term'),
    Group('2', label='term'),
    Group('3', label='term'),
    Group('q', label='surf', matches=[Match(wm_class='firefox')]),
    Group('w', label='mail', matches=[Match(wm_class='geary'), Match(title='Geary')]),
    Group('e', label='chat', matches=[Match(title='irc')]),
]


def _go_to_group(name: str) -> Callable:
    """
    This creates lazy functions that jump to a given group. When there is more than one
    screen, the first 3 and second 3 groups are kept on the first and second screen.
    E.g. going to the fourth group when the first group (and first screen) is focussed
    will also change the screen to the second screen.
    """
    def _inner(qtile: Qtile) -> None:
        if len(qtile.screens) == 1:
            qtile.groups_map[name].cmd_toscreen()
            return

        old = qtile.current_screen.group.name
        if name in '123':
            qtile.focus_screen(0)
            if old in '123' or qtile.current_screen.group.name != name:
                qtile.groups_map[name].cmd_toscreen()
        else:
            qtile.focus_screen(1)
            if old in 'qwe' or qtile.current_screen.group.name != name:
                qtile.groups_map[name].cmd_toscreen()

    return _inner


for i in groups:
    keys_group.extend([
        ([mod],             i.name, lazy.function(_go_to_group(i.name)), f"Go to group {i.name}"),
        ([mod, 'shift'],    i.name, lazy.window.togroup(i.name), f"Send window to group {i.name}"),
    ])


def _scroll_screen(direction: int) -> Callable:
    """
    Scroll to the next/prev group of the subset allocated to a specific screen. This
    will rotate between e.g. 1->2->3->1 when the first screen is focussed.
    """
    def _inner(qtile: Qtile):
        if len(qtile.screens) == 1:
            current = qtile.groups.index(qtile.current_group)
            destination = (current + direction) % 6
            qtile.groups[destination].cmd_toscreen()
            return

        current = qtile.groups.index(qtile.current_group)
        if current < 3:
            destination = (current + direction) % 3
        else:
            destination = ((current - 3 + direction) % 3) + 3
        qtile.groups[destination].cmd_toscreen()

    return _inner


keys_group.extend([
    ([mod], 'm', lazy.function(_scroll_screen(1)),  "Screen groups forward"),
    ([mod], 'n', lazy.function(_scroll_screen(-1)), "Screen groups backward"),
])


@hook.subscribe.startup
def _():
    # Set initial groups
    if len(qtile.screens) > 1:
        qtile.groups_map['1'].cmd_toscreen(0, toggle=False)
        qtile.groups_map['q'].cmd_toscreen(1, toggle=False)


@hook.subscribe.screen_change
def _(_):
    # Set groups to screens
    if len(qtile.screens) > 1:
        if qtile.screens[0].group.name not in '123':
            qtile.groups_map['1'].cmd_toscreen(0, toggle=False)
        qtile.groups_map['q'].cmd_toscreen(1, toggle=False)
