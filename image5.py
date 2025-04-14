# image5.py
# Generates a sad face with X eyes for panel 5

width, height = 200, 200
blue = "#0056a9"

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
svg.append(f'<rect width="{width}" height="{height}" fill="white" />')

# Face circle
svg.append(f'<circle cx="{width/2}" cy="{height/2}" r="80" stroke="{blue}" stroke-width="5" fill="none" />')

# Left eye (X)
lx, ly = width/2 - 35, height/2 - 30
svg.append(f'<line x1="{lx-8}" y1="{ly-8}" x2="{lx+8}" y2="{ly+8}" stroke="{blue}" stroke-width="4" />')
svg.append(f'<line x1="{lx-8}" y1="{ly+8}" x2="{lx+8}" y2="{ly-8}" stroke="{blue}" stroke-width="4" />')

# Right eye (X)
rx, ry = width/2 + 35, height/2 - 30
svg.append(f'<line x1="{rx-8}" y1="{ry-8}" x2="{rx+8}" y2="{ry+8}" stroke="{blue}" stroke-width="4" />')
svg.append(f'<line x1="{rx-8}" y1="{ry+8}" x2="{rx+8}" y2="{ry-8}" stroke="{blue}" stroke-width="4" />')

# Sad mouth (downward arc)
svg.append(f'''
  <path d="M {width/2 - 30} {height/2 + 40}
           Q {width/2} {height/2 + 20},
             {width/2 + 30} {height/2 + 40}"
        stroke="{blue}" stroke-width="4" fill="none" />
''')

svg.append('</svg>')

with open("5.svg", "w") as f:
    f.write("\n".join(svg))

print("SVG file generated: 5.svg")
