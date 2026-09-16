#!/usr/bin/env python3
"""
build_dual_mode_cards.py

Builds dark_mode.svg and light_mode.svg using the exact dimensions,
layout, styles, and color tokens from Andrew6rant's profile card,
with Siddharth's ASCII portrait on the left and resume details on the right.
"""

import html

# The 34 rows of Siddharth's ASCII art extracted from avi-ascii.svg
ASCII_ROWS = [
    "                  ==::---:--:::-::-:::                  ",
    "              .:..::...  .. ..   .::.:---               ",
    "            -:           ... .... ... :::----           ",
    "          :::.       ...   .    .....::...:-=           ",
    "         :.   .     ........     .:...::...-+++-        ",
    "        . .  ....  ..  .......:. ....  :..::=**-:       ",
    "       .        ...:       .:....     .  .  .:=+--      ",
    "      . . ..    .   .::    ...   .     .::: ..:=---     ",
    "          ....      ..:.. .::::-+**+==+##*+-=-+*#*+-    ",
    "      .  ....  .. . .-+**+++*##%%@@%%%@%%%%#**%%%#+     ",
    "      . ........:::::=#%%#%%%@@@@%@@@@%@@@@@%%%%%=      ",
    "       .....::::-----=##%%%%%%%%%%%%%%@@@@%%%%#*%       ",
    "       ....::::----=*#%%%%%%%%@@@@@@@@%%%%@@@%*+        ",
    "       ....::::---+#%%%%####****####%%@@@@%#*+==        ",
    "        .  .:::--=######**+==-=+++==+++###+==+#+==-:    ",
    "        -::....::-====-====--+******##+-+=+*#**=  -:    ",
    "       +#%%##*=::-+*******+=:***#%##%#++@*+#%%#=  :     ",
    "       ##%@%%%%+-=*#########++%%%%%@%+=%%@%%%@@+ -      ",
    "       #*%%%#*##+=*#####%%%@%*#%%%%%*+%%%%@@##%#-       ",
    "       =##%%%*#%*=+###%%%%%%@@%#####*%%%@@%%%%%%        ",
    "        -#%%##*##*==+*#%%%@@%@@@@%@@#%%%#%@@@%@@        ",
    "          *#%%%%**+=+++*%%%%@@@%%%%%#********+##        ",
    "            +#%#=+*=+++**#%%%%#+***#**#**#*#*-*         ",
    "              :=*++++++**###%%*#**##%%%%%%%##*+         ",
    "               +**==++****#*#%%@@%%%%%@%%@%%%+          ",
    "               +*#*=-=*******#%%%@@%%%%%@@@@#           ",
    "               +*###+--++++***%@@%%%%%%%%#%%+           ",
    "              -+*#%%%*=:-::-:-=*#%@@@@@@%%@@=           ",
    "           -..+**#%%%%%#+=-::. .:-+*%%%%###+            ",
    "          =*+-=*#%%%%%%%%%##*++=--:--:-:::.             ",
    "       :-==:-*#*+#%%%%%@%@%%%%####%#:.                  ",
    "    :--::::-+--**+*%@@@%@@@@%%%%#%@+ ..:                ",
    "  ::::::...::--=*%*=*#%@@@@@@@@%%%%:  ..:-              ",
    "--:::::::::..-+===%*--=#%@@@@@@%%@%=.  ..:--            "
]

def make_svg(mode="dark"):
    is_dark = (mode == "dark")

    bg_color = "#161b22" if is_dark else "#f6f8fa"
    text_color = "#c9d1d9" if is_dark else "#24292f"
    key_color = "#ffa657" if is_dark else "#953800"
    val_color = "#a5d6ff" if is_dark else "#0a3069"
    add_color = "#3fb950" if is_dark else "#1a7f37"
    del_color = "#f85149" if is_dark else "#cf222e"
    cc_color = "#616e7f" if is_dark else "#c2cfde"

    # ASCII text setup: 34 rows starting at y=32, spaced by 14.5px -> ends at y=510.5
    ascii_tspans = []
    y_ascii = 32.0
    for row in ASCII_ROWS:
        row_esc = html.escape(row)
        ascii_tspans.append(f'<tspan x="15" y="{y_ascii:.1f}">{row_esc}</tspan>')
        y_ascii += 14.5

    # Right side: 25 rows at y = 30, 50, 70, ..., 510
    # Following Andrew6rant's exact structure and classes
    info_lines = [
        # y=30
        (30, '<tspan x="390" y="30">siddharth@maharana</tspan> -———————————————————————————————————————————-—-'),
        # y=50
        (50, '<tspan x="390" y="50" class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">Windows 11, Linux, Android</tspan>'),
        # y=70
        (70, '<tspan x="390" y="70" class="cc">. </tspan><tspan class="key">Uptime</tspan>:<tspan class="cc"> .................... </tspan><tspan class="value">23 years, MCA Student</tspan>'),
        # y=90
        (90, '<tspan x="390" y="90" class="cc">. </tspan><tspan class="key">Host</tspan>:<tspan class="cc"> ...................... </tspan><tspan class="value">Amity University, Bengaluru</tspan>'),
        # y=110
        (110, '<tspan x="390" y="110" class="cc">. </tspan><tspan class="key">Kernel</tspan>:<tspan class="cc"> .................... </tspan><tspan class="value">Full Stack Developer &amp; AI Builder</tspan>'),
        # y=130
        (130, '<tspan x="390" y="130" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan class="cc"> ....................... </tspan><tspan class="value">VS Code, Cursor, Postman</tspan>'),
        # y=150
        (150, '<tspan x="390" y="150" class="cc">. </tspan>'),
        # y=170
        (170, '<tspan x="390" y="170" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:<tspan class="cc"> ..... </tspan><tspan class="value">TypeScript, JavaScript, Python, C</tspan>'),
        # y=190
        (190, '<tspan x="390" y="190" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Web</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">React.js, Node.js, Express, FastAPI</tspan>'),
        # y=210
        (210, '<tspan x="390" y="210" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Data</tspan>:<tspan class="cc"> ............ </tspan><tspan class="value">MongoDB, PostgreSQL, SQL, Docker</tspan>'),
        # y=230
        (230, '<tspan x="390" y="230" class="cc">. </tspan>'),
        # y=250
        (250, '<tspan x="390" y="250" class="cc">. </tspan><tspan class="key">Experience</tspan>.<tspan class="key">Intern</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">Web Dev Intern @ Infotact Solutions</tspan>'),
        # y=270
        (270, '<tspan x="390" y="270" class="cc">. </tspan><tspan class="key">Projects</tspan>.<tspan class="key">Featured</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">CORTEXA (AI Assistant), Telemedicine</tspan>'),
        # y=290
        (290, '<tspan x="390" y="290" class="cc">. </tspan><tspan class="key">Certifications</tspan>:<tspan class="cc"> ............ </tspan><tspan class="value">Oracle OCI Architect, Google Analytics</tspan>'),
        # y=310
        (310, '<tspan x="390" y="310">- Contact</tspan> -——————————————————————————————————————————————-—-'),
        # y=330
        (330, '<tspan x="390" y="330" class="cc">. </tspan><tspan class="key">Email</tspan>.<tspan class="key">Personal</tspan>:<tspan class="cc"> ............ </tspan><tspan class="value">siddharthk.maharana@gmail.com</tspan>'),
        # y=350
        (350, '<tspan x="390" y="350" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">siddharth-kumar-maharana</tspan>'),
        # y=370
        (370, '<tspan x="390" y="370" class="cc">. </tspan><tspan class="key">LeetCode</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">siddharthkmleetcode</tspan>'),
        # y=390
        (390, '<tspan x="390" y="390" class="cc">. </tspan><tspan class="key">Location</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">Bengaluru, Karnataka, India</tspan>'),
        # y=410
        (410, '<tspan x="390" y="410" class="cc">. </tspan><tspan class="key">Education</tspan>:<tspan class="cc"> ................. </tspan><tspan class="value">MCA (Amity Univ) · B.Sc Physics</tspan>'),
        # y=430
        (430, '<tspan x="390" y="430" class="cc">. </tspan>'),
        # y=450
        (450, '<tspan x="390" y="450">- GitHub Stats</tspan> -—————————————————————————————————————————-—-'),
        # y=470
        (470, '<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc"> .... </tspan><tspan class="value">19</tspan> {<tspan class="key">Contributed</tspan>: <tspan class="value">10+</tspan>} | <tspan class="key">Stars</tspan>:<tspan class="cc"> ........... </tspan><tspan class="value">4</tspan>'),
        # y=490
        (490, '<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc"> ................... </tspan><tspan class="value">461</tspan> | <tspan class="key">Followers</tspan>:<tspan class="cc"> ....... </tspan><tspan class="value">5</tspan>'),
        # y=510
        (510, '<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc">. </tspan><tspan class="value">185,420</tspan> ( <tspan class="addColor">165,240</tspan><tspan class="addColor">++</tspan>, <tspan class="delColor">20,180</tspan><tspan class="delColor">--</tspan> )')
    ]

    info_tspans_str = "\n".join(line[1] for line in info_lines)
    ascii_tspans_str = "\n".join(ascii_tspans)

    svg = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {key_color};}}
.value {{fill: {val_color};}}
.addColor {{fill: {add_color};}}
.delColor {{fill: {del_color};}}
.cc {{fill: {cc_color};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="985px" height="530px" fill="{bg_color}" rx="15"/>
<text x="15" y="32" fill="{text_color}" font-size="13px" class="ascii">
{ascii_tspans_str}
</text>
<text x="390" y="30" fill="{text_color}">
{info_tspans_str}
</text>
</svg>"""

    return svg

def run():
    dark_svg = make_svg("dark")
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print("Wrote dark_mode.svg")

    light_svg = make_svg("light")
    with open("light_mode.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("Wrote light_mode.svg")

if __name__ == "__main__":
    run()
