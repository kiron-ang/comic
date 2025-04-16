# image2.py
# Symbolic SVG of a computer monitor with a document and lines of data

# SVG setup
width, height = 800, 500
blue = "#0056a9"
red = "#d90d0d"
font = "Courier, monospace"

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
svg.append(f'<rect width="{width}" height="{height}" fill="white" />')

# --- Monitor base ---
monitor_x = 200
monitor_y = 100
monitor_w = 400
monitor_h = 300
svg.append(f'<rect x="{monitor_x}" y="{monitor_y}" width="{monitor_w}" height="{monitor_h}" rx="20" ry="20" fill="none" stroke="{blue}" stroke-width="6" />')

# --- Stand ---
stand_w = 100
stand_h = 30
stand_x = width / 2 - stand_w / 2
stand_y = monitor_y + monitor_h + 10
svg.append(f'<rect x="{stand_x}" y="{stand_y}" width="{stand_w}" height="{stand_h}" rx="5" fill="{blue}" />')

# --- Document (inside monitor) ---
doc_x = monitor_x + 60
doc_y = monitor_y + 40
doc_w = monitor_w - 120
doc_h = monitor_h - 80
svg.append(f'<rect x="{doc_x}" y="{doc_y}" width="{doc_w}" height="{doc_h}" fill="none" stroke="{blue}" stroke-width="3" />')

# --- Data lines (inside document) ---
line_start_x = doc_x + 20
line_end_x = doc_x + doc_w - 20
line_y = doc_y + 30
line_spacing = 25

for i in range(6):
    svg.append(f'<line x1="{line_start_x}" y1="{line_y}" x2="{line_end_x}" y2="{line_y}" stroke="{blue}" stroke-width="3" />')
    line_y += line_spacing


svg.append(f'<text x="0" y="{height}" font-size="30" fill="#0056a9" font-family="Courier, monospace">This infographic was created by Kiron Ang!</text>')


# End SVG
svg.append('</svg>')

# Write to file
with open("2.svg", "w") as f:
    f.write("\n".join(svg))

print("SVG file generated: 2.svg")
