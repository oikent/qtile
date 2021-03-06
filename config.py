# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
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


from logging import shutdown
import os
import re
import socket
import subprocess
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, qtile
from libqtile.widget import Spacer
import arcobattery

# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [

    # Most of our keybindings are in sxhkd file - except these

    # SUPER + FUNCTION KEYS
    Key([mod], "p", lazy.spawn('passmenu -fn "NotoMonoRegular:bold:pixelsize=21"')),
    Key([mod], "e", lazy.spawn('code')),
    Key([mod], "w", lazy.spawn('brave')),
    Key([mod], "Return", lazy.spawn('alacritty')),
    Key([mod], "x", lazy.spawn('arcolinux-logout')),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),

    # xrandr
    Key([mod], "z", lazy.spawn(home + '/.screenlayout/dual.sh')),


    # SUPER + SHIFT KEYS
    Key([mod, "shift"], "d", lazy.spawn(
        "dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=21'")),

    Key([mod, "shift"], "q", lazy.window.kill()),

    # Run SUPER + CTRL + r if qtile has crashed
    Key([mod, "shift"], "r", lazy.restart()),

    # CTRL + ALT KEYS
    Key(["control", "mod1"], "b", lazy.spawn('thunar')),
    Key(["control", "mod1"], "f", lazy.spawn('firefox')),
    Key(["control", "mod1"], "g", lazy.spawn('google-chrome-stable')),
    Key(["control", "mod1"], "o", lazy.spawn(
        home + '/.config/qtile/scripts/picom-toggle.sh')),
    Key(["control", "mod1"], "s", lazy.spawn(
        'alacritty -e htop')),


    # MULTIMEDIA KEYS
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master 1+ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "amixer set Master 10%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "amixer set Master 10%+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn(
            "xbacklight -dec 10")),
    Key([], "XF86MonBrightnessUp", lazy.spawn(
            "xbacklight -inc 10")),


    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating())

]

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ]

# FOR AZERTY KEYBOARDS
# group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

# group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
group_labels = ["???", "???", "???", "???", "???", "???", "???", "???", "???", "???", ]
# group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall",
                 "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", ]
# group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

        # CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(
            i.name), lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin": 5,
            "border_width": 2,
            "border_focus": "#1aafc7",
            "border_normal": "#000a29"
            # "border_focus": "#5e81ac",
            # "border_normal": "#4c566a"
            }


layout_theme = init_layout_theme()


layouts = [
    # layout.MonadTall(margin=8, border_width=2,
    #                  border_focus="#5e81ac", border_normal="#4c566a"),
    # layout.MonadWide(margin=8, border_width=2,
    #                  border_focus="#5e81ac", border_normal="#4c566a"),
    # layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    # layout.Floating(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Max(**layout_theme)
]

# COLORS FOR THE BAR


def init_colors():
    return [["#2e3440", "#3b4252"],  # color 0
            ["#1A73E8", "#1A73E8"],  # color 1
            ["#d8dee9", "#d8dee9"],  # color 2
            ["#ebcb8b", "#ebcb8b"],  # color 3
            ["#8fbcbb", "#8fbcbb"],  # color 4
            ["#f3f4f5", "#f3f4f5"],  # color 5
            ["#d08770", "#d08770"],  # color 6
            ["#62BB00", "#62BB00"],  # color 7
            ["#6790eb", "#6790eb"],  # color 8
            ["#a3be8c", "#a3be8c"],  # color 9
            ["#000a29", "#000a29"],  # color 10
            ["#1aafc7", "#1aafc7"],  # color 11
            ['#00226b', '#00226b'],  # color 12
            ["#000c4f", '#000c4f'],  # color 13
            ["#2F343F", "#2F343F"],  # color 14
            ["#c0c5ce", "#c0c5ce"],  # color 15
            ["#fba922", "#fba922"],  # color 16
            ["#3384d0", "#3384d0"],  # color 17
            ["#cd1f3f", "#cd1f3f"],  # color 18
            ["#e6d3f0", "#e6d3f0"],  # color 19
            ["#00aaff", "#00aaff"],  # color 20
            ["#dd1f3f", "#dd1f3f"]   # color 21
            ]


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans Bold",
                fontsize=18,
                padding=0,
                update_interval=5,
                background="#ffffff00"
                )


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    # prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

    widgets_list = [
        widget.GroupBox(font="FontAwesome",
                        margin_y=-1,
                        margin_x=0,
                        padding_y=6,
                        padding_x=5,
                        borderwidth=0,
                        disable_drag=True,
                        active=colors[9],
                        inactive=colors[5],
                        rounded=False,
                        highlight_method="text",
                        this_current_screen_border=colors[8],
                        foreground=colors[2],
                        background="#ffffff00"
                        ),
        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"
        ),
        widget.CurrentLayout(
            foreground=colors[5],
            background="#ffffff00"
        ),
        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"
        ),
        widget.TaskList(
            background="#ffffff00"
        ),

        widget.Pomodoro(
            update_interval=1,
            color_inactive=colors[14],
            length_pomodori=30,
            background="#ffffff00"
        ),
        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"
        ),
        widget.TextBox(
            font="FontAwesome",
            text=" ??? ",
            foreground=colors[19],
            background="#ffffff00"
        ),
        widget.Volume(
            update_interval=0.2,
            foreground=colors[19],
            background="#ffffff00"
        ),
        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"
        ),
        widget.TextBox(
            font="FontAwesome",
            text=" ??? ",
            foreground=colors[9],
            background="#ffffff00"
        ),
        widget.Backlight(
            backlight_name='intel_backlight',
            update_interval=0.5,
            foreground=colors[9],
            background="#ffffff00"

        ),

        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"

        ),
        widget.TextBox(
            font="FontAwesome",
            text=" ??? ",
            foreground=colors[8],
            padding=0,
            background="#ffffff00"
        ),
        widget.ThermalSensor(
            foreground=colors[8],
            foreground_alert=colors[16],
            metric=True,
            threshold=80,
            background="#ffffff00"
        ),

        # # battery option 2  from Qtile
        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"
        ),

        widget.TextBox(
            font="FontAwesome",
            text=" ??? ",
            foreground=colors[6],
            background="#ffffff00"
        ),

        widget.CPU(
            format='{load_percent}%',
            foreground=colors[6],
            background="#ffffff00",
        ),
        #    widget.CPUGraph(
        #             border_color = colors[2],
        #             fill_color = colors[8],
        #             graph_color = colors[8],
        #             background=colors[1],
        #             border_width = 1,
        #             line_width = 1,
        #             core = "all",
        #             type = "box"
        #             ),
        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"

        ),
        widget.TextBox(
            font="FontAwesome",
            text=" ???",
            foreground=colors[4],
            background="#ffffff00"

        ),
        widget.Memory(
            format='{MemUsed: .0f}M /{MemTotal: .0f}M',
            foreground=colors[4],
            background="#ffffff00"
        ),
        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"
        ),
        widget.TextBox(
            font="FontAwesome",
            text=" ???  ",
            foreground=colors[3],
            background="#ffffff00"

        ),
        widget.Clock(
            foreground=colors[3],
            format="%d/%m/%y %H:%M",
            background="#ffffff00"
        ),

        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background="#ffffff00"
        ),


    ]
    return widgets_list
######################################
# widget list bottom bar


def spawn_blueberry():
    qtile.cmd_spawn('blueberry')


def open_mail():
    qtile.cmd_spawn('thunderbird')


def open_wifi():
    qtile.cmd_spawn('alacritty -e nmtui')


def poweroff():
    qtile.cmd_spawn('alacritty -e shutdown +0')


def update():
    qtile.cmd_spawn('sudo .config/qtile/scripts/update.sh')


def widgets_list_bottom():
    # prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list_bottom = [
        widget.Spacer(length=bar.STRETCH),

        # widget.CheckUpdates(
        #     display_format='updates:{updates}',
        #     foreground=colors[0],
        #     colour_have_updates=colors[21],
        #     mouse_callbacks={
        #         'Button1': update
        #     },
        #     no_update_string='No Updates',
        # ),
        widget.Sep(
            linewidth=0,
            padding=20,
        ),
        widget.OpenWeather(
            app_key='334622f52a1318ed62d42b3b90b199e2',
            cityid=2147714,
            foreground=colors[15],
        ),
        widget.Sep(
            linewidth=0,
            padding=20,
        ),
        widget.Net(
            format='{down} \u2193\u2191 {up}',
            interface="wlp0s20f3",
            foreground=colors[9],

        ),
        widget.Sep(
            linewidth=0,
            padding=20,
        ),
        widget.GmailChecker(
            username='oikent37@gmail.com',
            password='waueriuzsjcrsnfa',
            status_only_unseen=True,
            display_fmt='Unread {0}',
            foreground=colors[16],
            mouse_callbacks={
                'Button1': open_mail}
        ),


        widget.Sep(
            linewidth=0,
            padding=20,
        ),
        widget.Battery(
            foreground=colors[7],
            format='{watt:0.2f}W  {hour}:{min}  {percent:2.0%}'

        ),
        arcobattery.BatteryIcon(

            scale=0.7,
            y_poss=2,
            theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
            format='{percent}'


        ),
        # widget.NetGraph(
        #     fontsize=12,
        #     bandwidth="down",
        #     interface="auto",
        #     fill_color=colors[8],
        #     foreground=colors[2],
        #     graph_color=colors[8],
        #     border_color=colors[2],
        #     padding=0,
        #     border_width=1,
        #     line_width=1,
        # ),
        widget.TextBox(
            font="FontAwesome",
            text=" ??? ",
            foreground=colors[20],
            mouse_callbacks={
                "Button1": spawn_blueberry
            }

        ),
        widget.Sep(
            linewidth=0,
            padding=5,
        ),

        widget.TextBox(
            font="FontAwesome",
            text=" ??? ",
            foreground=colors[2],
            mouse_callbacks={
                'Button1': open_wifi
            }

        ),
        widget.Sep(
            linewidth=0,
            padding=5,
        ),
        widget.TextBox(
            font="FontAwesome",
            text=" ??? ",
            foreground=colors[18],
            mouse_callbacks={
                'Button2': poweroff
            }
        )

    ]
    return widgets_list_bottom

####################################################


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_list(), size=30, margin=[0, 5, 0, 5], background="#ffffff00"),
                   bottom=bar.Bar(widgets=widgets_list_bottom(),
                                  size=30, margin=[0, 5, 0, 5], background="#ffffff00")


                   )]


screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())


]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #####################################################################################
#     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#     #####################################################################################
#     d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d[group_names[3]] = ["Gimp", "gimp" ]
#     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d[group_names[5]] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d[group_names[6]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d[group_names[7]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d[group_names[8]] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d[group_names[9]] = ["Srpotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ######################################################################################
#
# wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME


main = None


@ hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])
    # start arandr script
    subprocess.call([home + '/.screenlayout/dual.sh'])
    # Run picom toggle
    # subprocess.call([home + '/.config/qtile/scripts/picom-toggle.sh'])
    # subprocess.call([home + '/.config/qtile/scripts/picom-toggle.sh'])


@ hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@ hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'Arcolinux-welcome-app.py'},
    {'wmclass': 'Arcolinux-tweak-tool.py'},
    {'wmclass': 'Arcolinux-calamares-tool.py'},
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wmclass': 'Arandr'},
    {'wmclass': 'feh'},
    {'wmclass': 'Galculator'},
    {'wmclass': 'arcolinux-logout'},
    {'wmclass': 'xfce4-terminal'},
    {'wname': 'branchdialog'},
    {'wname': 'Open File'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},

],  fullscreen_border_width=0, border_width=0)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
