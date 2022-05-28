from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupImage, PopupText

from libqtile.lazy import lazy


def show_power_menu(qtile):
    controls = [
        PopupImage(
            filename="~/pictures/icons/lock.svg",
            pos_x=0.15,
            pos_y=0.1,
            width=0.1,
            height=0.5,
            mouse_callbacks={"Button1": lazy.spawn("swaylock")},
        ),
        PopupImage(
            filename="~/pictures/icons/sleep.svg",
            pos_x=0.45,
            pos_y=0.1,
            width=0.1,
            height=0.5,
            mouse_callbacks={"Button1": lazy.spawn("systemctl suspend", shell=True)},
        ),
        PopupImage(
            filename="~/pictures/icons/shutdown.svg",
            pos_x=0.75,
            pos_y=0.1,
            width=0.1,
            height=0.5,
            highlight="A00000",
            mouse_callbacks={"Button1": lazy.spawn("backup-home-and-poweroff")},
        ),
        PopupText(
            text="Lock", pos_x=0.1, pos_y=0.7, width=0.2, height=0.2, h_align="center"
        ),
        PopupText(
            text="Sleep", pos_x=0.4, pos_y=0.7, width=0.2, height=0.2, h_align="center"
        ),
        PopupText(
            text="Shutdown",
            pos_x=0.7,
            pos_y=0.7,
            width=0.2,
            height=0.2,
            h_align="center",
        ),
    ]
    PopupRelativeLayout(
        qtile,
        width=1000,
        height=200,
        controls=controls,
        background="000000c0",
        initial_focus=2,
    ).show(centered=True)


keys_power_menu = [
    ([], "XF86PowerOff", lazy.function(show_power_menu), "Display the power menu.")
]
