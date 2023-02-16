#!/usr/bin/env bash
#
# Qtile Wayland startup script

foot --server &

# Wallpaper
(
    swww init
    sleep 1
    swww img --filter Nearest --transition-step=1 --transition-fps 60 \
	--transition-duration 12 ~/pictures/Wallpapers/Leuh6wm-slow.gif
) &

run_if_new() { ps aux | grep -v grep | grep -q $1 || $@; }

[[ -z "$QTILE_XEPHYR" ]] && {
    # Session setup
    systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP &
    dbus-update-activation-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP &

    # Services
    kanshi  &
    wlsunset &
    swayidle &
    swaync &
    mpDris2 &
    sway-mpris-idle-inhibit &
    playerctld daemon &
    nm-applet --indicator &
    #kdeconnect-indicator &
    darkman run &

    # Startup programs
    run_if_new keepassxc &
    sleep 2
    run_if_new firefox &
    run_if_new evolution &

    # Notify me if any systemd services failed
    check_systemd &

# Send all output to Qtile's log
} &>> ~/.local/share/qtile/qtile.log


# Clean up
clean() {
    pkill -P $$
}
trap clean SIGINT SIGTERM
sleep infinity &
wait $!
