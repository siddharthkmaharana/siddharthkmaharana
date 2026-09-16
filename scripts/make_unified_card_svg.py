#!/usr/bin/env python3
"""
make_unified_card_svg.py

Creates profile-card.svg — a single, unified, seamless terminal card
combining Siddharth's animated ASCII portrait on the left and the
neofetch info card on the right, inside ONE outer card with no internal
dividers or borders, exactly matching Andrew6rant's profile style.
"""

import re
import html

def build_unified_card(out_path="profile-card.svg"):
    # 1. Read avi-ascii.svg to extract ASCII art elements
    with open("avi-ascii.svg", "r", encoding="utf-8") as f:
        avi_svg = f.read()

    clips = re.findall(r'(<clipPath id="clip\d+">.*?</clipPath>)', avi_svg, re.DOTALL)
    texts = re.findall(r'(<text class="ascii-row"[^>]*>.*?</text>)', avi_svg)
    cursors = re.findall(r'(<rect class="cursor"[^>]*/>)', avi_svg)

    card_w = 960
    card_h = 420
    info_x = 480.0
    info_start_y = 30.0
    line_h = 14.2
    val_col = 25
    total_chars = 65
    font_size = 9.8

    # Resume data for right side
    data = [
        ("header", "siddharth@maharana", ""),
        ("kv", "OS", "Windows 11, Linux, Android"),
        ("kv", "Uptime", "23 years, MCA Student"),
        ("kv", "Host", "Amity University, Bengaluru"),
        ("kv", "Kernel", "Full Stack Developer & AI Builder"),
        ("kv", "IDE", "VS Code, Cursor, Postman"),
        
        ("gap",),
        ("kv", "Languages.Code", "TypeScript, JavaScript, Python, C"),
        ("kv", "Frameworks.Web", "React.js, Node.js, Express, FastAPI"),
        ("kv", "Databases", "MongoDB Atlas, PostgreSQL, MySQL"),
        ("kv", "Cloud.DevOps", "AWS (EC2, S3), Docker, CI/CD, Vercel"),
        
        ("gap",),
        ("section", "Experience & Projects", ""),
        ("kv", "Work.Intern", "Web Dev Intern @ Infotact Solutions"),
        ("kv", "Projects.AI", "CORTEXA (AI Desktop Assistant)"),
        ("kv", "Projects.Web", "Telemedicine EHR, Food Delivery App"),
        ("kv", "Research", "Amity Nexus 2026 (Data Integrity)"),
        ("kv", "Certifications", "Oracle OCI 2025, Google Analytics"),
        
        ("gap",),
        ("section", "Contact", ""),
        ("kv", "Email.Personal", "siddharthk.maharana@gmail.com"),
        ("kv", "LinkedIn", "siddharth-kumar-maharana"),
        ("kv", "LeetCode", "siddharthkmleetcode"),
        ("kv", "Location", "Bengaluru, Karnataka, India"),
        
        ("gap",),
        ("section", "Stats & Education", ""),
        ("kv", "GitHub.Streak", "461 contributions (in last year)", "green"),
        ("kv", "Education.Master", "MCA @ Amity Univ | CGPA: 8.5", "highlight"),
        ("kv", "Education.Grad", "B.Sc Physics @ Berhampur Univ (7.5)")
    ]

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_w} {card_h}" width="100%" font-family="Consolas, \'SF Mono\', \'Roboto Mono\', Menlo, monospace">')
    svg.append('''<style>
  .bg { fill: #0d1117; }
  .border { stroke: #30363d; fill: none; }
  .user { fill: #79c0ff; font-weight: bold; }
  .sec { fill: #c9d1d9; font-weight: bold; }
  .dash { fill: #30363d; }
  .dot { fill: #484f58; }
  .prefix { fill: #484f58; }
  .key { fill: #ffa657; }
  .val { fill: #a5d6ff; }
  .highlight { fill: #e6edf3; }
  .green { fill: #3fb950; font-weight: bold; }
  .ascii-row {
    font-family: 'Consolas','SF Mono','Menlo',monospace;
    font-size: 8px;
    fill: #c9d1d9;
    white-space: pre;
  }
  .info-text {
    font-size: 9.8px;
  }
  .cursor {
    fill: #c9d1d9;
    animation: blink 1s steps(1) infinite;
    animation-delay: 25.53s;
    opacity: 0;
  }
  @keyframes blink {
    0%   { opacity: 1; }
    50%  { opacity: 0; }
    100% { opacity: 1; }
  }
  text, tspan { white-space: pre; }
</style>''')

    # Single unified outer container
    svg.append(f'<rect width="{card_w}" height="{card_h}" rx="12" class="bg"/>')
    svg.append(f'<rect x="0.5" y="0.5" width="{card_w-1}" height="{card_h-1}" rx="12" class="border"/>')

    # Left side: Animated ASCII portrait (shifted by y_offset +15px to center in 420px card)
    y_offset = 15.0
    x_offset = 8.0

    # Output clip paths (with adjusted y)
    for c in clips:
        # adjust rect y in clipPath
        def adj_rect(m):
            x = float(m.group(1)) + x_offset
            y = float(m.group(2)) + y_offset
            w = m.group(3)
            h = m.group(4)
            rest = m.group(5)
            return f'<rect x="{x:.1f}" y="{y:.2f}" width="{w}" height="{h}"{rest}'
        
        c_mod = re.sub(r'<rect x="([\d\.]+)" y="([\d\.]+)" width="([\d\.]+)" height="([\d\.]+)"([^>]*)', adj_rect, c)
        svg.append(c_mod)

    # Output text rows (with adjusted x and y)
    for t in texts:
        def adj_text(m):
            cls_ = m.group(1)
            x = float(m.group(2)) + x_offset
            y = float(m.group(3)) + y_offset
            clip = m.group(4)
            txt = m.group(5)
            return f'<text class="{cls_}" x="{x:.1f}" y="{y:.2f}" {clip}>{txt}</text>'
        
        t_mod = re.sub(r'<text class="([^"]+)" x="([\d\.]+)" y="([\d\.]+)" ([^>]+)>(.*?)</text>', adj_text, t)
        svg.append(t_mod)

    # Output cursor
    if cursors:
        def adj_cur(m):
            x = float(m.group(1)) + x_offset
            y = float(m.group(2)) + y_offset
            w = m.group(3)
            h = m.group(4)
            return f'<rect class="cursor" x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}"/>'
        cur_mod = re.sub(r'<rect class="cursor" x="([\d\.]+)" y="([\d\.]+)" width="([\d\.]+)" height="([\d\.]+)"\s*/>', adj_cur, cursors[0])
        svg.append(cur_mod)

    # Right side: Terminal neofetch info card
    y = info_start_y
    for item in data:
        kind = item[0]
        if kind == "gap":
            y += 4.5
            continue
        elif kind == "header":
            raw_title = item[1]
            title = html.escape(raw_title)
            dashes = "-" * max(4, total_chars - len(raw_title) - 1)
            svg.append(f'<text class="info-text" x="{info_x}" y="{y:.1f}"><tspan class="user">{title}</tspan> <tspan class="dash">{dashes}</tspan></text>')
        elif kind == "section":
            raw_title = item[1]
            title = f"- {html.escape(raw_title)} "
            dashes = "-" * max(4, total_chars - (len(raw_title) + 3))
            svg.append(f'<text class="info-text" x="{info_x}" y="{y:.1f}"><tspan class="sec">{title}</tspan><tspan class="dash">{dashes}</tspan></text>')
        elif kind == "kv":
            k = item[1]
            v = html.escape(item[2])
            v_cls = item[3] if len(item) > 3 and item[3] else "val"
            
            if "." in k:
                parts = k.split(".", 1)
                k_markup = f'<tspan class="key">{html.escape(parts[0])}</tspan>.<tspan class="key">{html.escape(parts[1])}</tspan>'
            else:
                k_markup = f'<tspan class="key">{html.escape(k)}</tspan>'
            
            prefix = ". "
            used = len(prefix) + len(k) + 1
            num_dots = max(2, val_col - used)
            dots = " " + "." * (num_dots - 2) + " "
            
            line_str = (f'<text class="info-text" x="{info_x}" y="{y:.1f}">'
                        f'<tspan class="prefix">{prefix}</tspan>'
                        f'{k_markup}:'
                        f'<tspan class="dot">{dots}</tspan>'
                        f'<tspan class="{v_cls}">{v}</tspan>'
                        f'</text>')
            svg.append(line_str)
        y += line_h

    svg.append('</svg>')
    out_content = "\n".join(svg)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out_content)
    print(f"Built {out_path} ({card_w}x{card_h}, info_y_final={y:.1f})")

if __name__ == "__main__":
    build_unified_card()
