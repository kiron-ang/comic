import random

# SVG canvas dimensions
width, height = 800, 600

# Number of circles to generate and radius of each circle
num_circles = 100
circle_radius = 15

# Probability that a circle is "infected" (red)
infection_probability = 0.3  # Adjust this value (0 to 1) as needed

# Initialize SVG content as a list of strings for easier concatenation
svg_elements = []
svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')

# Draw a background rectangle with white fill (no border)
svg_elements.append(f'<rect width="{width}" height="{height}" fill="white" />')

# Loop to generate each circle with random positions and color selection
for i in range(num_circles):
    # Ensure the circle stays within canvas bounds
    x = random.uniform(circle_radius, width - circle_radius)
    y = random.uniform(circle_radius, height - circle_radius)

    # Randomly assign color based on infection_probability:
    # Red if the random value is lower than the probability, blue otherwise.
    color = "#d90d0d" if random.random() < infection_probability else "#0056a9"

    # Append the circle element to the SVG elements list
    svg_elements.append(f'  <circle cx="{x:.2f}" cy="{y:.2f}" r="{circle_radius}" fill="{color}" />')

# Add the text label "WEST TEXAS" in the bottom left corner.
# The coordinates here (x=10, y=height - 10) place the text with a small margin.
svg_elements.append(f'<text x="0" y="{height}" font-size="30" fill="#0056a9" font-family="Courier, monospace">WEST TEXAS</text>')

# Close the SVG tag
svg_elements.append('</svg>')

# Combine all SVG parts into one string
svg_content = "\n".join(svg_elements)

# Write the SVG content to a file named "1.svg"
with open("1.svg", "w") as file:
    file.write(svg_content)

print("SVG file generated: 1.svg")
