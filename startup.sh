#!/usr/bin/env bash
#
# Qtile Wayland startup script

{
    foot --server &

    # wob
    FIFO=/tmp/wob-$WAYLAND_DISPLAY
    test -e $FIFO || mkfifo $FIFO
    tail -f $FIFO | wob \
	-a bottom -M 0 -H 28 -W 1920 -o 0 -b 0 -p 0 \
	--background-color "#00000000" --bar-color "#66CFCCD6" -t 800 &

} &> /dev/null

run_if_new() { ps aux | grep -v grep | grep -q $1 || $@; }

[[ -z "$QTILE_XEPHYR" ]] && {
    # Session setup
    systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP &
    dbus-update-activation-environment --systemd \
	WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP &

    # Services
    kanshi &>> ~/.local/share/qtile/qtile.log &
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
