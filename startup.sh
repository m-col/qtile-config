#!/usr/bin/env bash
#
# Qtile Wayland startup script

QTILE_PID=$PPID


{
    foot --server &

    # wob
    FIFO=/tmp/wob-$WAYLAND_DISPLAY
    test -e $FIFO || mkfifo $FIFO
    tail -f $FIFO | wob -a bottom \
	-M ${WOB_MARGIN:-0} -H ${WOB_HEIGHT:-32} -W ${WOB_WIDTH:-400} \
	-o ${WOB_OFFSET:-0} -b ${WOB_BORDER:-0} -p ${WOB_PADDING:-0} \
	--background-color ${WOB_BACKGROUND:-#ff000000} \
	--bar-color ${WOB_BAR:-#00ffffff} -t 800 &

} &> /dev/null

run_if_new() { ps aux | grep -v grep | grep -q $1 || $@; }

[[ -z "$QTILE_XEPHYR" ]] && {
    # Session setup
    systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP &
    dbus-update-activation-environment --systemd \
	WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP &

    # Services
    kanshi &
    wlsunset &
    swayidle &
    mpDris2 &
    sway-mpris-idle-inhibit &
    playerctld daemon &
    kdeconnect-indicator &

    # Startup programs
    run_if_new firefox &
    run_if_new geary &

    # Notify me if any systemd services failed
    check_systemd &
} &> /dev/null


# Clean up
clean() {
    pkill -P $$
    test -e $FIFO && rm $FIFO
}
trap clean SIGINT SIGTERM
sleep infinity &
wait $!
