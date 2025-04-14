import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Draw white background
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Draw grid lines
    third = height / 3
    line_color = HexColor("#d90d0d")
    c.setStrokeColor(line_color)
    c.setLineWidth(2)
    c.line(0, third, width, third)
    c.line(0, 2 * third, width, 2 * third)
    c.line(width / 2, 2 * third, width / 2, height)
    c.line(width / 2, 0, width / 2, third)

    # Insert SVG into first panel (top-left panel)
    drawing = svg2rlg("1.svg")

    # Calculate scale to fit into the top-left panel
    panel_width = width / 2
    panel_height = third

    scale_x = panel_width / drawing.width
    scale_y = panel_height / drawing.height
    scale = min(scale_x, scale_y) * 0.95  # scale down to 95%

    drawing.scale(scale, scale)

    svg_x = (panel_width - drawing.width * scale) / 2
    svg_y = 2 * third + (panel_height - drawing.height * scale) / 2

    renderPDF.draw(drawing, c, svg_x, svg_y - 10)

    # Read sentences from file and split on sentences ending with a period.
    with open("readme.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    sentences = re.split(r'(?<=\.)\s+', content)

    # Setup text appearance
    c.setFillColor(HexColor("#0056a9"))
    font = "Courier"
    size = 12
    c.setFont(font, size)
    lh = size * 1.2  # Line height
    padding = 12

    # Layout: (x_center, y_bottom, y_top) for each of the 5 sections.
    layout = [
        (width * 0.25, 2 * third, height),     # Sentence 1
        (width * 0.75, 2 * third, height),     # Sentence 2
        (width / 2, third, 2 * third),         # Sentence 3
        (width * 0.25, 0, third),              # Sentence 4
        (width * 0.75, 0, third)               # Sentence 5
    ]

    # Process up to the first 5 sentences.
    for index, orig_sentence in enumerate(sentences[:5]):
        x_center, y_bot, y_top = layout[index]
        section_h = y_top - y_bot
        start_y = y_top - padding - size

        # Detect and remove URL from the sentence, if present.
        match = re.search(r'\(?\bhttps?://\S+\b\)?', orig_sentence)
        if match:
            url = match.group(0).strip("()")
            sent = orig_sentence.replace(match.group(0), "").strip(" .") + "."
        else:
            url = None
            sent = orig_sentence

        # Set text width limit depending on the section.
        tw = width * 0.9 if index == 2 else width * 0.45
        lines = simpleSplit(sent, font, size, tw)

        # Calculate bounding box for hyperlink if needed.
        max_width = min(tw, max(c.stringWidth(line, font, size) for line in lines))
        left_x = x_center - max_width / 2
        right_x = x_center + max_width / 2
        top_y = start_y + size
        bottom_y = start_y - lh * (len(lines) - 1) - 2

        # Draw each line of the text.
        current_y = start_y
        for line in lines:
            c.drawCentredString(x_center, current_y, line)
            current_y -= lh

        # Add a hyperlink if a URL was found.
        if url:
            c.linkURL(url, (left_x, bottom_y, right_x, top_y), relative=0)

    c.showPage()
    c.save()
    print("Success:", filename)

if __name__ == "__main__":
    create_pdf("comic.pdf")
