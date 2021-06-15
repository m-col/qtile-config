#!/usr/bin/env bash
#
# Qtile Wayland startup script

foot --server &
swaybg -c '#1B2021' &

FIFO=/tmp/wob-$WAYLAND_DISPLAY
test -e $FIFO || mkfifo $FIFO

tail -f $FIFO | wob -a bottom \
    -M ${WOB_MARGIN:-0} -H ${WOB_HEIGHT:-32} -W ${WOB_WIDTH:-400} \
    -o ${WOB_OFFSET:-0} -b ${WOB_BORDER:-0} -p ${WOB_PADDING:-0} \
    --background-color ${WOB_BACKGROUND:-#ff000000} \
    --bar-color ${WOB_BAR:-#00ffffff} &


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
