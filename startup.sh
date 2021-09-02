#!/usr/bin/env bash
#
# Qtile Wayland startup script

QTILE_PID=$PPID


{
    foot --server &
    #swaybg -c '#1B2021' &
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

run_if_new() { ps aux | grep -v grep | grep -q $1 || $@; }

[[ -z "$QTILE_XEPHYR" ]] && {
    wlsunset -t 2500 -T 5700 -l 55.7 -L -3.1 &
    kanshi &
    run_if_new keepassxc &
    run_if_new firefox &
    run_if_new irc &

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
