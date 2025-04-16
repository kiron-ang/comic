# image4.py
# Three huge blue dollar signs centered in a wide rectangle

width, height = 400, 120
blue = "#0056a9"

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
svg.append(f'<rect width="{width}" height="{height}" fill="white" />')

# Add three huge blue dollar signs, centered
# font-size chosen to fit the height; adjust as needed for best fit
font_size = 100
svg.append(
    f'<text x="50%" y="50%" fill="{blue}" font-size="{font_size}" font-family="Courier, monospace" '
    'dominant-baseline="middle" text-anchor="middle">$$$</text>'
)

svg.append('</svg>')

with open("4.svg", "w") as f:
    f.write("\n".join(svg))

print("SVG file generated: 4.svg")
