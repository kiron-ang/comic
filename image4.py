# image4.py
# Wide rectangle with blue/red sides and a crack in between (ideal for panel 4)

width, height = 400, 120
gap = 6
half = width // 2
blue = "#0056a9"
red = "#d90d0d"

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
svg.append(f'<rect width="{width}" height="{height}" fill="white" />')

# Left blue rectangle (shifted left of center)
left_width = half - gap // 2
svg.append(f'<rect x="0" y="0" width="{left_width}" height="{height}" fill="{blue}" />')

# Right red rectangle (shifted right of center)
right_x = half + gap // 2
right_width = width - right_x
svg.append(f'<rect x="{right_x}" y="0" width="{right_width}" height="{height}" fill="{red}" />')

# Crack path centered in the gap
center = width / 2
zigzag = [
    (center, 0),
    (center - 4, 15),
    (center + 4, 30),
    (center - 4, 45),
    (center + 4, 60),
    (center - 4, 75),
    (center + 4, 90),
    (center - 4, 105),
    (center, height)
]
points = " ".join([f"{x},{y}" for x, y in zigzag])
svg.append(f'<polyline points="{points}" fill="none" stroke="white" stroke-width="5" />')

svg.append('</svg>')

with open("4.svg", "w") as f:
    f.write("\n".join(svg))

print("SVG file generated: 4.svg")
