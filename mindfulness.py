# Copyright (c) 2022 Matt Colligan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from urllib import request
from random import randint

import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

from libqtile.log_utils import logger
from libqtile.widget import base
from libqtile.utils import get_cache_dir

Gst.init(None)


class ReMindfulness(base.ThreadPoolText):
    """
    Mindfulness reminder widget (Proof of concept / work in progress)

    Inspired by Kyle MacLeod's mindfulnotifier Android app
    (https://github.com/kmac/mindfulnotifier). The widget will periodically play a
    calming tone at semi-random intervals.

    Note, if the specified audio_file does not exist (i.e. the first time the widget is
    configured, leaving the default value for ``audio_file``), one will be downloaded.
    It is fetched via the mindfulnotifier app's github repository.
    """

    default_path = os.path.join(get_cache_dir(), "tibetan_bell_ding_b.mp3")
    default_url = "https://github.com/kmac/mindfulnotifier/raw/master/media/tibetan_bell_ding_b.mp3"

    defaults = [
        ("audio_file", default_path, "Lower bound for the interval between reminders"),
        ("interval_minimum", 60 * 60, "Lower bound for the interval between reminders"),
        ("interval_maximum", 90 * 60, "Upper bound for the interval between reminders"),
        ("reminder_background", "ff0000", "Background colour when reminding"),
        ("reminder_foreground", "ff0000", "Foreground colour when reminding"),
        ("reminder_duration", 5, "Duration of reminders (i.e. for appearance change)"),
        ("reminder_text", None, "Text"),
    ]

    def __init__(self, text="", **config):
        base.ThreadPoolText.__init__(self, text, **config)
        self.add_defaults(ReMindfulness.defaults)
        self._just_started = True
        self._original_foreground = self.foreground
        self._original_background = self.background

        self.add_callbacks(
            {
                "Button1": self._reset_colours,
            }
        )

    def _configure(self, qtile, bar):
        self._just_started = not self.configured
        base.ThreadPoolText._configure(self, qtile, bar)

    def poll(self):
        self.update_interval = randint(self.interval_minimum, self.interval_maximum)

        if self._just_started:
            return self.text

        if not os.path.exists(self.audio_file):
            logger.info("Downloading default tone for ReMindfulness widget")
            request.urlretrieve(self.default_url, self.audio_file)

        playbin = Gst.ElementFactory.make("playbin", "playbin")
        playbin.props.uri = "file://" + self.audio_file
        playbin.set_state(Gst.State.PLAYING)

        self.foreground = self.reminder_foreground
        self.background = self.reminder_background
        self.timeout_add(self.reminder_duration, self._reset_colours)

        return self.text

    def _reset_colours(self):
        self.foreground = self._original_foreground
        self.background = self._original_background
