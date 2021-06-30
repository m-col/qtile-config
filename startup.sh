#!/usr/bin/env bash
#
# Qtile Wayland startup script

QTILE_PID=$PPID


{
    foot --server &
    swaybg -c '#1B2021' &
} &> /dev/null


# wob
FIFO=/tmp/wob-$WAYLAND_DISPLAY
test -e $FIFO || mkfifo $FIFO
tail -f $FIFO | wob -a bottom \
    -M ${WOB_MARGIN:-0} -H ${WOB_HEIGHT:-32} -W ${WOB_WIDTH:-400} \
    -o ${WOB_OFFSET:-0} -b ${WOB_BORDER:-0} -p ${WOB_PADDING:-0} \
    --background-color ${WOB_BACKGROUND:-#ff000000} \
    --bar-color ${WOB_BAR:-#00ffffff} -t 800 &


# TTY session only
[[ -z "$QTILE_XEPHYR" ]] && {
    keepassxc &
    firefox &
    kanshi &
    wlsunset -t 3100 -T 5700 -l 55.7 -L -3.1 &

    sleep 3
    check_systemd
} &> /dev/null


# Clean up
clean() {
    pkill -P $$
    test -e $FIFO && rm $FIFO
}
trap clean SIGINT SIGTERM
sleep infinity &
wait $!
