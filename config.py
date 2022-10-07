# python libs
import os
import subprocess

# qtile libs
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

mod = "mod1"
mod4 = "mod4"
terminal = guess_terminal()

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Spawn a command using rofi"),

    # custom keybindings
    Key([mod4], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Change keyboard layout"),
    Key([mod4], "e", lazy.spawn("emacs"), desc="Run editor"),
    Key([mod4], "b", lazy.spawn("firefox"), desc="Run browser"),
    Key([mod4], "m", lazy.spawn("firefox --new-window https://open.spotify.com"), desc="Runs spotify in browser"),
]

groupDict = [
    {"number": "1", "name": "Code"},
    {"number": "2", "name": "Music"},
    {"number": "3", "name": "Browser"},
    {"number": "4", "name": "Terminal"},
]

groups = [Group(i["name"]) for i in groupDict]

for i in groupDict:
    keys.extend(
        [
            Key(
                [mod],
                i["number"],
                lazy.group[i["name"]].toscreen(),
                desc="Switch to group {}".format(i["name"]),
            ),
            Key(
                [mod, "shift"],
                i["number"],
                lazy.window.togroup(i["name"], switch_group=True),
                desc="Switch to & move focused window to group {}".format(i["name"]),
            ),
        ]
    )

layouts = [
    #layout.Columns(border_focus="#FFFFFF", border_normal="#000000", border_width=2, margin=10),
    layout.MonadTall(
        border_focus="#FFFFFF",
        border_normal="#000000",
        border_width=2,
        margin=10,
        ratio=0.6,
        change_ratio=0.1,
    ),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    layout.VerticalTile(border_focus="#FFFFFF", border_normal="#000000", border_width=2, margin=10),
    # layout.Zoomy(),
    layout.Max(),
]

# MonadTall layout keys
keys.extend([
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "space", lazy.layout.flip()), 
])

barFontSize = 17 
barFont = "Hack"
barBoldFont = "Hack Bold"

#colors
background = "#282A36"
background2 = "383A59"
foreground = "#F4F4EF"
primary = "#BD93F9"
orange = "#FF9C32"
majenta = "#FF79C6"
blue = "#7CCCDF"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    foreground = background,
                    padding = 10,
                ),
                widget.CurrentLayout(
                    fontsize = barFontSize,
                    font = barFont,
                    foreground = foreground, 
                ),
                widget.Sep(
                    foreground = background,
                    padding = 10,
                ),
                widget.GroupBox(
                    fontsize = barFontSize,
                    font = barFont,
                    highlight_method = "line",
                    padding = 15,
                    borderwidth = 4,
                    this_current_screen_border = primary,
                ),
                widget.Prompt(
                    fontsize = barFontSize,
                    font = barFont,
                ),
                widget.WindowName(
                    fontsize = barFontSize,
                    font = barFont,
                ),
                widget.Sep(
                    foreground = primary,
                    padding = 0,
                    linewidth = 10,
                    size_percent = 100,
                ),
                widget.CheckUpdates(
                    background = primary,
                    foreground = background,
                    distro = "Arch",
                    no_update_string = "Updates not found",
                    fontsize = barFontSize,
                    font = barBoldFont,
                ),
                widget.Sep(
                    foreground = primary,
                    padding = 0,
                    linewidth = 10,
                    size_percent = 100,
                ),
                widget.TextBox(
                    text = "RAM:",
                    fontsize = barFontSize,
                    font = barBoldFont,
                    foreground = background,
                    background = orange,
                ),
                widget.Memory(
                    background = orange,
                    foreground = background,
                    fontsize = barFontSize,
                    font = barBoldFont,
                    format = '{MemUsed: .0f}{mm} of{MemTotal: .0f}{mm}',
                ),
                widget.Sep(
                    foreground = orange,
                    padding = 0,
                    linewidth = 10,
                    size_percent = 100,
                ),
                widget.Sep(
                    foreground = blue,
                    padding = 0,
                    linewidth = 10,
                    size_percent = 100,
                ),
                widget.TextBox(
                    text = "CPU:",
                    fontsize = barFontSize,
                    font = barBoldFont,
                    foreground = background,
                    background = blue,
                ),
                widget.CPU(
                    fontsize = barFontSize,
                    font = barBoldFont,
                    format = "{load_percent}%",
                    background = blue,
                    foreground = background,
                ),
                widget.Sep(
                    foreground = blue,
                    padding = 0,
                    linewidth = 10,
                    size_percent = 100,
                ),
                widget.Sep(
                    foreground = majenta,
                    padding = 0,
                    linewidth = 10,
                    size_percent = 100,
                ),
                widget.KeyboardLayout(
                    configured_keyboards=["us", "ru"],
                    fontsize = barFontSize,
                    font = barBoldFont,
                    background = majenta,
                    foreground = background,
                ),
                widget.Sep(
                    foreground = majenta,
                    padding = 0,
                    linewidth = 10,
                    size_percent = 100,
                ),
                widget.Sep(
                    foreground = background2,
                    padding = 0,
                    linewidth = 10,
                    size_percent = 100,
                ),
                widget.Systray(
                    fontsize = barFontSize,
                    font = barFont,
                ),
                widget.Clock(
                    format="%d.%m.%Y | %I:%M:%S",
                    fontsize = barFontSize,
                    font = barBoldFont,
                    background = background2,
                    foreground = primary,
                ),
            ],
            30,
            margin=[5, 10, 0, 10],
            background = background,
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget.Sep(
                    foreground = background,
                    padding = 10,
                ),
                widget.CurrentLayout(
                    fontsize = barFontSize,
                    font = barFont,
                    foreground = foreground, 
                ),
                widget.GroupBox(
                    fontsize = barFontSize,
                    font = barFont,
                    highlight_method = "line",
                    padding = 15,
                    borderwidth = 4,
                    this_current_screen_border = primary,
                ),
            ],
            30,
            margin=[0, 10, 5, 10],
            background = background,
        ),
    )
]

@hook.subscribe.layout_change
def layoutChange (layout, group):
    if (layout.name == 'max'):
        group.screen.top.show(False)
    else:
        group.screen.top.show(True)


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = False 
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
