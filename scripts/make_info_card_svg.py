#!/usr/bin/env python3
"""
make_info_card_svg.py

Generates info-card.svg — a terminal-style neofetch/system-fetch card for
Siddharth Kumar Maharana, styled after Andrew6rant's terminal profile card,
using details from Siddharth's resume and matching the exact 389px height
of avi-ascii.svg.
"""

def build_card(out_path="info-card.svg"):
    width = 510
    height = 389
    font_size = 9.8
    line_h = 13.8
    start_y = 22.0
    start_x = 16.0
    val_col = 25  # character index where value starts
    total_chars = 68

    data = [
        # (type, key, value, optional_class)
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
    import html

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" font-family="Consolas, \'SF Mono\', \'Roboto Mono\', Menlo, monospace" font-size="{font_size}px">')
    svg.append('''<style>
  .bg { fill: #0d1117; }
  .border { stroke: #30363d; fill: none; }
  .user { fill: #79c0ff; font-weight: bold; }
  .sec { fill: #c9d1d9; font-weight: bold; }
  .dash { fill: #30363d; }
  .dot { fill: #484f58; }
  .prefix { fill: #484f58; }
  .key { fill: #ffa657; }
  .key-sub { fill: #ff7b72; }
  .val { fill: #a5d6ff; }
  .highlight { fill: #e6edf3; }
  .green { fill: #3fb950; font-weight: bold; }
  text, tspan { white-space: pre; }
</style>''')
    svg.append(f'<rect width="{width}" height="{height}" rx="10" class="bg"/>')
    svg.append(f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="10" class="border"/>')

    y = start_y
    for item in data:
        kind = item[0]
        if kind == "gap":
            y += 4.5
            continue
        elif kind == "header":
            raw_title = item[1]
            title = html.escape(raw_title)
            dashes = "-" * max(4, total_chars - len(raw_title) - 1)
            svg.append(f'<text x="{start_x}" y="{y:.1f}"><tspan class="user">{title}</tspan> <tspan class="dash">{dashes}</tspan></text>')
        elif kind == "section":
            raw_title = item[1]
            title = f"- {html.escape(raw_title)} "
            dashes = "-" * max(4, total_chars - (len(raw_title) + 3))
            svg.append(f'<text x="{start_x}" y="{y:.1f}"><tspan class="sec">{title}</tspan><tspan class="dash">{dashes}</tspan></text>')
        elif kind == "kv":
            k = item[1]
            v = html.escape(item[2])
            v_cls = item[3] if len(item) > 3 and item[3] else "val"
            
            # Format key (handle dotted keys like Languages.Code)
            if "." in k:
                parts = k.split(".", 1)
                k_markup = f'<tspan class="key">{html.escape(parts[0])}</tspan>.<tspan class="key">{html.escape(parts[1])}</tspan>'
            else:
                k_markup = f'<tspan class="key">{html.escape(k)}</tspan>'
            
            prefix = ". "
            used = len(prefix) + len(k) + 1  # 1 for ":"
            num_dots = max(2, val_col - used)
            dots = " " + "." * (num_dots - 2) + " "
            
            line_str = (f'<text x="{start_x}" y="{y:.1f}">'
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
    print(f"Built {out_path} ({width}x{height}, y_final={y:.1f})")

if __name__ == "__main__":
    build_card()
