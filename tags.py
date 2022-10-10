"""
Tags
====

This workflow replaces groups. There is only one group defined per (possible) screen. No
keybindings are defined to switch between groups or to move windows between groups. If
only one monitor is connected then only the first group is ever used, etc.

"""

from __future__ import annotations

import os
from collections import defaultdict
from typing import TYPE_CHECKING

from libqtile import hook, qtile
from libqtile.backend.base import Window
from libqtile.config import Group, Match
from libqtile.lazy import lazy
from libqtile.log_utils import logger

if TYPE_CHECKING:
    from typing import List, Tuple


groups: List[Group] = [Group("")]

tags: List[Tuple[str, Match, List[Window]]] = [
    ("terms", Match(wm_class="foot"), []),
    ("firefox", Match(wm_class="firefox"), []),
    ("thunar", Match(wm_class="thunar"), []),
]


@hook.subscribe.client_new
def _(window):
    """
    This adds windows to any tags that match it.
    """
    if isinstance(window, Window):  # Static windows ignored
        for name, match, windows in tags:
            if match.compare(window):
                windows.append(window)
                tag_hidden = windows[0].minimized
                window.minimized = tag_hidden
                qtile.current_screen.group.add(
                    window, focus=window.can_steal_focus and tag_hidden
                )


def _toggle_tag(_qtile, to_toggle: str):
    """
    This is bound to keys to show/hide all windows of a given tag. It toggles their
    minimized state.
    """
    for name, match, windows in tags:
        if name == to_toggle:
            for window in windows:
                window.toggle_minimize()
            return


mod = "mod1" if int(os.environ.get("QTILE_XEPHYR", 0)) else "mod4"

keys_group: Tuple[List[str], str, Any, str] = []

for i, (name, _, _) in enumerate(tags):
    keys_group.extend(
        [
            ([mod], str(i + 1), lazy.function(_toggle_tag, name), f"Toggle tag {name}"),
        ]
    )
