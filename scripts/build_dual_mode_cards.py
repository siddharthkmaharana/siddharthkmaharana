#!/usr/bin/env python3
"""
build_dual_mode_cards.py

Builds dark_mode.svg and light_mode.svg with pixel-perfect alignment,
matching Andrew6rant's layout down to the character:
- Left: Siddharth's full ASCII portrait (all 25 rows x 37 cols from head/hair
  down to neck/shoulders, fully scaled - not cropped or half-faced), with
  smooth SMIL row-by-row typing animation.
- Right: System neofetch card where EVERY single row is flush-right aligned
  at exactly column 60, with section breathing gaps at y=290 and y=430
  matching Andrew6rant's exact vertical rhythm.
- GitHub Stats: Dynamically synced (Repos, Streak replacing Stars, Commits,
  Followers, Lines of Code) fetched via fetch_github_stats.py with caching.
- Cache Busting: Automatically updates README.md with a fresh cache-buster
  timestamp on every run so GitHub's CDN proxy and browsers never serve
  stale cached SVGs.
"""

import os
import sys
import re
import html
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from fetch_github_stats import get_live_stats

# Full 25-row resampled portrait of Siddharth (complete head, hair, glasses, face, shoulders)
ASCII_25_ROWS = [
    "              -=:--:-::-:-:.         ",
    "          .......  .... .:.:-:..     ",
    "         ::.    ..  .   ...:..:-     ",
    "        ..      .....   .:..:..=+=   ",
    "             . .    ....    ...:=+-. ",
    "         .   .  :.  ..  .   .:: .--- ",
    "         ...    .-:.---+#*++##*==*#*:",
    "      . .....::.-*#*#%%@%@@@@@@%#%%= ",
    "       ...:::---=#%%%%%%%%%%@@%%%#%  ",
    "       ...::--=+#%%%%#%%%%@@%%@%#+   ",
    "        . ::--*####*+==+*+**#%*++*--:",
    "       .--::::======-=****#*-++#*+ .:",
    "       *%%%#=-+******=##%%%+*%#%%* . ",
    "       ##%#*#++###%%@##%%%#*%%@%##-  ",
    "       -#%%*#*+*#%%%%@%%#%*%%@%%%%   ",
    "        :#%%#*+=+*%%%@@%%%######*%   ",
    "          -##=*=++*#%%#+*******#--   ",
    "            -*+++**##%#%##%%%%%#*:   ",
    "            -**==****#%%@%%%%@@%:    ",
    "            -*##=-+++*#@%%%%%%%#     ",
    "          ..+*%%#*=-:::=+#%%%%%+     ",
    "         =+-+#%%%%%#*+=---=---:      ",
    "     ..:---+*+#%%%%@%%###%:.         ",
    "    .:::..--=***%%@@@@@%%# ...       ",
    "  :-::::::.-==#+-+%@@@@%@#. ..-:     ",
]

TOTAL_LEN = 60
STAGGER = 0.22      # Delay between each row starting to type (seconds)
ROW_DUR = 0.022     # Seconds per character typed in a row
ASCII_X = 20        # Left padding for ASCII art (centers the portrait in left half)

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

def make_solid_rule(title, prefix="", suffix=""):
    """Creates a continuous solid divider line using Unicode em-dashes like Andrew6rant"""
    label = f"{prefix}{title}{suffix}"
    needed = TOTAL_LEN - len(label)
    if needed <= 0:
        return label
    # Standard Andrew rule format: '-————————————————————————————-—-'
    dashes = "-" + "—" * (needed - 4) + "-—-"
    return f"{label}{dashes}"

def make_svg(mode="dark", stats=None):
    if stats is None:
        stats = get_live_stats("siddharthkmaharana")

    is_dark = (mode == "dark")

    bg_color = "#161b22" if is_dark else "#f6f8fa"
    text_color = "#c9d1d9" if is_dark else "#24292f"
    key_color = "#ffa657" if is_dark else "#953800"
    val_color = "#a5d6ff" if is_dark else "#0a3069"
    add_color = "#3fb950" if is_dark else "#1a7f37"
    del_color = "#f85149" if is_dark else "#cf222e"
    cc_color = "#616e7f" if is_dark else "#c2cfde"

    # Left side: 25 rows animated row-by-row via SMIL clip-paths
    defs = ["<defs>"]
    ascii_elements = []
    max_w = 360.0  # covers full 37-column width in 16px Consolas

    for i, row in enumerate(ASCII_25_ROWS):
        y = 30 + i * 20
        clip_y = y - 16
        clip_id = f"face-clip-{mode}-{i}"
        
        row_len = max(1, len(row.rstrip()))
        dur = max(0.18, ROW_DUR * row_len)
        begin = STAGGER * i

        defs.append(
            f'  <clipPath id="{clip_id}">\n'
            f'    <rect x="{ASCII_X}" y="{clip_y}" width="0" height="20">\n'
            f'      <animate attributeName="width" from="0" to="{max_w:.1f}" '
            f'begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.25 0 0.3 1" keyTimes="0;1"/>\n'
            f'    </rect>\n'
            f'  </clipPath>'
        )

        row_esc = html.escape(row)
        ascii_elements.append(
            f'  <text x="{ASCII_X}" y="{y}" clip-path="url(#{clip_id})">{row_esc}</text>'
        )

    defs.append("</defs>")
    defs_str = "\n".join(defs)
    ascii_elements_str = "\n".join(ascii_elements)

    # Right side: 23 active rows with empty gaps at y=290 and y=430, all exactly 60 chars
    head_rule = make_solid_rule("siddharth@maharana", suffix=" ")
    contact_rule = make_solid_rule("Contact", prefix="- ", suffix=" ")
    stats_rule = make_solid_rule("GitHub Stats", prefix="- ", suffix=" ")

    # Dynamic GitHub stats values
    repos_val = stats.get("repos", 20)
    contrib_val = stats.get("contributed", "10+")
    streak_val = stats.get("streak", 19)
    commits_val = stats.get("commits", 534)
    followers_val = stats.get("followers", 0)
    loc_total_val = stats.get("loc_total", 185420)
    loc_add_val = stats.get("loc_add", 165240)
    loc_del_val = stats.get("loc_del", 20180)

    # 1. Repos & Streak row (Daily streak count replacing Stars, pipe '|' at col 36)
    left_repos = ". Repos:"
    contrib_suffix = f" {{Contributed: {contrib_val}}} | Streak:"
    dots_r_count = 35 - len(left_repos) - len(str(repos_val)) - len(f" {{Contributed: {contrib_val}}}")
    dots_r = " " + "." * max(1, dots_r_count - 2) + " "
    row1_left = f"{left_repos}{dots_r}{repos_val}{contrib_suffix}"
    dots_s_count = TOTAL_LEN - len(row1_left) - len(str(streak_val))
    dots_s = " " + "." * max(1, dots_s_count - 2) + " "
    row1_markup = (
        f'<tspan class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc">{dots_r}</tspan>'
        f'<tspan class="value">{repos_val}</tspan> {{<tspan class="key">Contributed</tspan>: '
        f'<tspan class="value">{contrib_val}</tspan>}} | <tspan class="key">Streak</tspan>:'
        f'<tspan class="cc">{dots_s}</tspan><tspan class="value">{streak_val}</tspan>'
    )

    # 2. Commits & Followers row (pipe '|' at col 36)
    left_commits = ". Commits:"
    dots_c_count = 35 - len(left_commits) - len(str(commits_val))
    dots_c = " " + "." * max(1, dots_c_count - 2) + " "
    row2_left = f"{left_commits}{dots_c}{commits_val} | Followers:"
    dots_f_count = TOTAL_LEN - len(row2_left) - len(str(followers_val))
    dots_f = " " + "." * max(1, dots_f_count - 2) + " "
    row2_markup = (
        f'<tspan class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc">{dots_c}</tspan>'
        f'<tspan class="value">{commits_val}</tspan> | <tspan class="key">Followers</tspan>:'
        f'<tspan class="cc">{dots_f}</tspan><tspan class="value">{followers_val}</tspan>'
    )

    # 3. Lines of Code row (ends at col 60)
    loc_key = ". Lines of Code on GitHub:"
    loc_str = f"{loc_total_val:,}"
    add_str = f"{loc_add_val:,}"
    del_str = f"{loc_del_val:,}"
    paren_part = f" ( {add_str}++,  {del_str}-- )"
    dots_loc_count = TOTAL_LEN - len(loc_key) - len(loc_str) - len(paren_part)
    dots_loc = "." * max(0, dots_loc_count - 1) + " "
    row3_markup = (
        f'<tspan class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:'
        f'<tspan class="cc">{dots_loc}</tspan><tspan class="value">{loc_str}</tspan> '
        f'( <tspan class="addColor">{add_str}++</tspan>,  <tspan class="delColor">{del_str}--</tspan> )'
    )

    info_lines = [
        # System Info block (y=30 to y=130)
        (30, f'<tspan x="390" y="30">{head_rule[:len("siddharth@maharana")]}</tspan> {head_rule[len("siddharth@maharana")+1:]}'),
        (50, f'<tspan x="390" y="50">{format_kv_line("OS", "Windows 11, Linux, Android")}</tspan>'),
        (70, f'<tspan x="390" y="70">{format_kv_line("Uptime", "23 years, MCA Student")}</tspan>'),
        (90, f'<tspan x="390" y="90">{format_kv_line("Host", "Amity University, Bengaluru")}</tspan>'),
        (110, f'<tspan x="390" y="110">{format_kv_line("Kernel", "Full Stack & AI Developer")}</tspan>'),
        (130, f'<tspan x="390" y="130">{format_kv_line("IDE", "VS Code, Cursor, Postman")}</tspan>'),
        (150, '<tspan x="390" y="150" class="cc">. </tspan>'),
        # Languages block (y=170 to y=210)
        (170, f'<tspan x="390" y="170">{format_kv_line("Languages.Programming", "TypeScript, Python, JS, C")}</tspan>'),
        (190, f'<tspan x="390" y="190">{format_kv_line("Languages.Web", "React, Node, Express, FastAPI")}</tspan>'),
        (210, f'<tspan x="390" y="210">{format_kv_line("Languages.Data", "MongoDB, Postgres, SQL, Docker")}</tspan>'),
        (230, '<tspan x="390" y="230" class="cc">. </tspan>'),
        # Hobbies block (y=250 to y=270)
        (250, f'<tspan x="390" y="250">{format_kv_line("Hobbies.Software", "AI Agents, Automation, Bots")}</tspan>'),
        (270, f'<tspan x="390" y="270">{format_kv_line("Projects.Featured", "CORTEXA, Merkle-Tree-Visualizer")}</tspan>'),
        # y=290 is an EMPTY gap (creates clean breathing room above Contact, matching Andrew6rant)
        # Contact block (y=310 to y=410)
        (310, f'<tspan x="390" y="310">{contact_rule[:len("- Contact")]}</tspan> {contact_rule[len("- Contact")+1:]}'),
        (330, f'<tspan x="390" y="330">{format_kv_line("Email.Personal", "siddharthk.maharana@gmail.com")}</tspan>'),
        (350, f'<tspan x="390" y="350">{format_kv_line("LinkedIn", "siddharth-kumar-maharana")}</tspan>'),
        (370, f'<tspan x="390" y="370">{format_kv_line("LeetCode", "siddharthkmleetcode")}</tspan>'),
        (390, f'<tspan x="390" y="390">{format_kv_line("Location", "Bengaluru, Karnataka, India")}</tspan>'),
        (410, f'<tspan x="390" y="410">{format_kv_line("Education", "MCA (Amity) | B.Sc Physics")}</tspan>'),
        # y=430 is an EMPTY gap (creates clean breathing room above GitHub Stats, matching Andrew6rant)
        # GitHub Stats block (y=450 to y=510)
        (450, f'<tspan x="390" y="450">{stats_rule[:len("- GitHub Stats")]}</tspan> {stats_rule[len("- GitHub Stats")+1:]}'),
        (470, f'<tspan x="390" y="470">{row1_markup}</tspan>'),
        (490, f'<tspan x="390" y="490">{row2_markup}</tspan>'),
        (510, f'<tspan x="390" y="510">{row3_markup}</tspan>')
    ]

    info_tspans_str = "\n".join(line[1] for line in info_lines)

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
{defs_str}
<g class="ascii" fill="{text_color}">
{ascii_elements_str}
</g>
<text x="390" y="30" fill="{text_color}">
{info_tspans_str}
</text>
</svg>"""

    return svg

def update_readme_cache_buster():
    """
    Updates README.md with a fresh cache-busting timestamp on the raw image URLs
    so that GitHub's CDN and web browsers immediately display the newly generated SVGs.
    """
    readme_path = os.path.join(REPO_ROOT, "README.md")
    if not os.path.exists(readme_path):
        return
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    ts = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    
    # Standardize the picture block to use raw.githubusercontent.com URLs with ?v=<timestamp>
    dark_url = f"https://raw.githubusercontent.com/siddharthkmaharana/siddharthkmaharana/main/dark_mode.svg?v={ts}"
    light_url = f"https://raw.githubusercontent.com/siddharthkmaharana/siddharthkmaharana/main/light_mode.svg?v={ts}"

    pattern = r'<picture>\s*<source media="\(prefers-color-scheme: dark\)" srcset="[^"]+">\s*(?:<source media="\(prefers-color-scheme: light\)" srcset="[^"]+">\s*)?<img alt="Siddharth Kumar Maharana\'s Profile" src="[^"]*"[^>]*>\s*</picture>'
    replacement = (
        f'<picture>\n'
        f'  <source media="(prefers-color-scheme: dark)" srcset="{dark_url}">\n'
        f'  <source media="(prefers-color-scheme: light)" srcset="{light_url}">\n'
        f'  <img alt="Siddharth Kumar Maharana\'s Profile" src="{dark_url}" />\n'
        f'</picture>'
    )

    new_content = re.sub(pattern, replacement, content, count=1)
    if new_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[build_dual_mode_cards] Updated README.md with cache buster ?v={ts}")

def run():
    stats = get_live_stats("siddharthkmaharana")
    print(f"[build_dual_mode_cards] Generating cards with stats: Repos={stats.get('repos')}, Streak={stats.get('streak')}, Commits={stats.get('commits')}, Followers={stats.get('followers')}")

    dark_svg = make_svg("dark", stats=stats)
    dark_path = os.path.join(REPO_ROOT, "dark_mode.svg")
    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print(f"Wrote {dark_path}")

    light_svg = make_svg("light", stats=stats)
    light_path = os.path.join(REPO_ROOT, "light_mode.svg")
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(light_svg)
    print(f"Wrote {light_path}")

    update_readme_cache_buster()

if __name__ == "__main__":
    run()
