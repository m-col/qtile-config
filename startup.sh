#!/usr/bin/env bash
#
# Qtile Wayland startup script

foot --server &
swaybg -c '#1B2021' &

FIFO=/tmp/wob-$WAYLAND_DISPLAY
test -e $FIFO || mkfifo $FIFO
tail -f $FIFO | wob -a left -a right -a bottom &


# Things after this are only run on a TTY
[[ -n "$QTILE_XEPHYR" ]] && exit  


run_if_new() { pgrep $1 &> /dev/null || $@ &; }

run_if_new mako
run_if_new keepassxc

pgrep wlsunset && pkill -SIGKILL wlsunset
wlsunset -t 3100 -T 5700 -l 55.7 -L -3.1 &> /dev/null

sleep 5
check_systemd
kanshi &> /dev/null &
