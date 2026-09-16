#!/usr/bin/env python3
"""
build_dual_mode_cards.py

Builds dark_mode.svg and light_mode.svg with pixel-perfect alignment,
matching Andrew6rant's layout down to the character:
- Left: Siddharth's ASCII portrait (25 rows x 37 cols, perfectly scaled and centered).
- Right: System neofetch card where EVERY single row is flush-right aligned
  at exactly column 58 (no overflow, no clipping, straight vertical margins on both sides).
"""

import html

# 25 rows of Siddharth's ASCII portrait, trimmed & centered to 37 chars
ASCII_25_ROWS = [
    "        ....      ..:.. .::::-+**+==+",
    "    .  ....  .. . .-+**+++*##%%@@%%%@",
    "    . ........:::::=#%%#%%%@@@@%@@@@%",
    "     .....::::-----=##%%%%%%%%%%%%%%@",
    "     ....::::----=*#%%%%%%%%@@@@@@@@%",
    "     ....::::---+#%%%%####****####%%@",
    "      .  .:::--=######**+==-=+++==+++",
    "      -::....::-====-====--+******##+",
    "     +#%%##*=::-+*******+=:***#%##%#+",
    "     ##%@%%%%+-=*#########++%%%%%@%+=",
    "     #*%%%#*##+=*#####%%%@%*#%%%%%*+%",
    "     =##%%%*#%*=+###%%%%%%@@%#####*%%",
    "      -#%%##*##*==+*#%%%@@%@@@@%@@#%%",
    "        *#%%%%**+=+++*%%%%@@@%%%%%#**",
    "          +#%#=+*=+++**#%%%%#+***#**#",
    "            :=*++++++**###%%*#**##%%%",
    "             +**==++****#*#%%@@%%%%%@",
    "             +*#*=-=*******#%%%@@%%%%",
    "             +*###+--++++***%@@%%%%%%",
    "            -+*#%%%*=:-::-:-=*#%@@@@@",
    "         -..+**#%%%%%#+=-::. .:-+*%%%",
    "        =*+-=*#%%%%%%%%%##*++=--:--:-",
    "     :-==:-*#*+#%%%%%@%@%%%%####%#:. ",
    "  :--::::-+--**+*%@@@%@@@@%%%%#%@+ ..",
    "::::::...::--=*%*=*#%@@@@@@@@%%%%:  ."
]

TOTAL_LEN = 58

def format_kv_line(k, v):
    prefix = ". "
    if "." in k:
        parts = k.split(".", 1)
        k_markup = f'<tspan class="key">{html.escape(parts[0])}</tspan>.<tspan class="key">{html.escape(parts[1])}</tspan>:'
    else:
        k_markup = f'<tspan class="key">{html.escape(k)}</tspan>:'
    
    used = len(prefix) + len(k) + 1  # 1 for ':'
    num_dots = TOTAL_LEN - used - len(v)
    dots = " " + "." * max(2, num_dots - 2) + " "
    v_escaped = html.escape(v)
    return f'<tspan class="cc">{prefix}</tspan>{k_markup}<tspan class="cc">{dots}</tspan><tspan class="value">{v_escaped}</tspan>'

def make_svg(mode="dark"):
    is_dark = (mode == "dark")

    bg_color = "#161b22" if is_dark else "#f6f8fa"
    text_color = "#c9d1d9" if is_dark else "#24292f"
    key_color = "#ffa657" if is_dark else "#953800"
    val_color = "#a5d6ff" if is_dark else "#0a3069"
    add_color = "#3fb950" if is_dark else "#1a7f37"
    del_color = "#f85149" if is_dark else "#cf222e"
    cc_color = "#616e7f" if is_dark else "#c2cfde"

    # Left side: 25 rows for ASCII art at y = 30, 50, ..., 510 (step 20)
    ascii_tspans = []
    for i, row in enumerate(ASCII_25_ROWS):
        y = 30 + i * 20
        row_padded = row.ljust(37)
        row_esc = html.escape(row_padded)
        ascii_tspans.append(f'<tspan x="15" y="{y}">{row_esc}</tspan>')

    # Right side: 25 rows, each ending flush-right at column 58
    dashes_head = "-" * (TOTAL_LEN - len("siddharth@maharana") - 1)
    dashes_contact = "-" * (TOTAL_LEN - len("- Contact "))
    dashes_stats = "-" * (TOTAL_LEN - len("- GitHub Stats "))

    info_lines = [
        # y=30
        (30, f'<tspan x="390" y="30">siddharth@maharana</tspan> {dashes_head}'),
        # y=50
        (50, f'<tspan x="390" y="50">{format_kv_line("OS", "Windows 11, Linux, Android")}</tspan>'),
        # y=70
        (70, f'<tspan x="390" y="70">{format_kv_line("Uptime", "23 years, MCA Student")}</tspan>'),
        # y=90
        (90, f'<tspan x="390" y="90">{format_kv_line("Host", "Amity University, Bengaluru")}</tspan>'),
        # y=110
        (110, f'<tspan x="390" y="110">{format_kv_line("Kernel", "Full Stack & AI Developer")}</tspan>'),
        # y=130
        (130, f'<tspan x="390" y="130">{format_kv_line("IDE", "VS Code, Cursor, Postman")}</tspan>'),
        # y=150
        (150, '<tspan x="390" y="150" class="cc">. </tspan>'),
        # y=170
        (170, f'<tspan x="390" y="170">{format_kv_line("Languages.Programming", "TypeScript, Python, JS, C")}</tspan>'),
        # y=190
        (190, f'<tspan x="390" y="190">{format_kv_line("Languages.Web", "React, Node, Express, FastAPI")}</tspan>'),
        # y=210
        (210, f'<tspan x="390" y="210">{format_kv_line("Languages.Data", "MongoDB, Postgres, SQL, Docker")}</tspan>'),
        # y=230
        (230, '<tspan x="390" y="230" class="cc">. </tspan>'),
        # y=250
        (250, f'<tspan x="390" y="250">{format_kv_line("Hobbies.Software", "AI Agents, Automation, Bots")}</tspan>'),
        # y=270
        (270, f'<tspan x="390" y="270">{format_kv_line("Projects.Featured", "CORTEXA, Telemedicine EHR")}</tspan>'),
        # y=290
        (290, f'<tspan x="390" y="290">{format_kv_line("Certifications", "Oracle OCI 2025, Google Cert")}</tspan>'),
        # y=310
        (310, f'<tspan x="390" y="310">- Contact</tspan> {dashes_contact}'),
        # y=330
        (330, f'<tspan x="390" y="330">{format_kv_line("Email.Personal", "siddharthk.maharana@gmail.com")}</tspan>'),
        # y=350
        (350, f'<tspan x="390" y="350">{format_kv_line("LinkedIn", "siddharth-kumar-maharana")}</tspan>'),
        # y=370
        (370, f'<tspan x="390" y="370">{format_kv_line("LeetCode", "siddharthkmleetcode")}</tspan>'),
        # y=390
        (390, f'<tspan x="390" y="390">{format_kv_line("Location", "Bengaluru, Karnataka, India")}</tspan>'),
        # y=410
        (410, f'<tspan x="390" y="410">{format_kv_line("Education", "MCA (Amity) | B.Sc Physics")}</tspan>'),
        # y=430
        (430, '<tspan x="390" y="430" class="cc">. </tspan>'),
        # y=450
        (450, f'<tspan x="390" y="450">- GitHub Stats</tspan> {dashes_stats}'),
        # y=470
        (470, '<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc"> .... </tspan><tspan class="value">19</tspan> {<tspan class="key">Contributed</tspan>: <tspan class="value">10+</tspan>} | <tspan class="key">Stars</tspan>:<tspan class="cc"> ........... </tspan><tspan class="value">4</tspan>'),
        # y=490
        (490, '<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc"> ................. </tspan><tspan class="value">461</tspan> | <tspan class="key">Followers</tspan>:<tspan class="cc"> .......... </tspan><tspan class="value">5</tspan>'),
        # y=510
        (510, '<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc"> </tspan><tspan class="value">185,420</tspan> ( <tspan class="addColor">165,240++</tspan>, <tspan class="delColor">20,180--</tspan> )')
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
<text x="15" y="30" fill="{text_color}" class="ascii">
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
