"""
Groups
======

 - 8 groups
 - 4 bound to each screen when using two monitors

"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from libqtile import hook, qtile
from libqtile.config import Group, Match
from libqtile.lazy import lazy

if TYPE_CHECKING:
    from typing import Any, Callable

    from libqtile.core.manager import Qtile


mod = "mod1" if int(os.environ.get("QTILE_XEPHYR", 0)) else "mod4"

keys_group: list[tuple[list[str], str, Any, str]] = []


groups: list[Group] = [
    Group("1", label="html"),
    Group("2", label="disc", matches=[Match(wm_class="discord")]),
    Group("3", label="mail", matches=[Match(wm_class="evolution")]),
    Group("4", label="tune", matches=[
        Match(wm_class="dev.alextren.Spot"), Match(title="Spotify"),
    ]),
    Group("q", label="term"),
    Group("w", label="term"),
    Group("e", label="term"),
    Group("r", label="term"),
]


def _go_to_group(qtile: Qtile, name: str) -> None:
    """
    This creates lazy functions that jump to a given group. When there is more than one
    screen, the first 4 and second 4 groups are kept on the first and second screen.
    E.g. going to the fifth group when the first group (and first screen) is focussed
    will also change the screen to the second screen.
    """
    if len(qtile.screens) == 1:
        qtile.groups_map[name].toscreen(toggle=True)
        return

    old = qtile.current_screen.group.name
    if name in "1234":
        qtile.focus_screen(0)
        if old in "1234" or qtile.current_screen.group.name != name:
            qtile.groups_map[name].toscreen(toggle=True)
    else:
        qtile.focus_screen(1)
        if old in "qwer" or qtile.current_screen.group.name != name:
            qtile.groups_map[name].toscreen(toggle=True)


for i in groups:
    keys_group.extend(
        [
            (
                [mod],
                i.name,
                lazy.function(_go_to_group, i.name),
                f"Go to group {i.name}",
            ),
            (
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                f"Send window to group {i.name}",
            ),
        ]
    )


def _scroll_screen(qtile: Qtile, direction: int) -> None:
    """
    Scroll to the next/prev group of the subset allocated to a specific screen. This
    will rotate between e.g. 1->2->3->4->1 when the first screen is focussed.
    """
    if len(qtile.screens) == 1:
        current = qtile.groups.index(qtile.current_group)
        destination = (current + direction) % 8
        qtile.groups[destination].toscreen()
        return

    current = qtile.groups.index(qtile.current_group)
    if current < 4:
        destination = (current + direction) % 4
    else:
        destination = ((current - 4 + direction) % 4) + 4
    qtile.groups[destination].toscreen()


keys_group.extend(
    [
        ([mod], "m", lazy.function(_scroll_screen, 1), "Screen groups forward"),
        ([mod], "n", lazy.function(_scroll_screen, -1), "Screen groups backward"),
    ]
)


@hook.subscribe.startup
def _():
    # Set initial groups
    if len(qtile.screens) > 1:
        qtile.groups_map["1"].toscreen(0, toggle=False)
        qtile.groups_map["q"].toscreen(1, toggle=False)
        qtile.focus_screen(1)


@hook.subscribe.screens_reconfigured
def _():
    # Set groups to screens
    if len(qtile.screens) > 1:
        if qtile.screens[0].group.name not in "1234":
            qtile.groups_map["1"].toscreen(0, toggle=False)
        if qtile.screens[1].group.name in "1234":
            qtile.groups_map["q"].toscreen(1, toggle=False)
