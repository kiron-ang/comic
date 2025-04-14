import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def draw_svg(c, svg_path, x_panel, y_panel, panel_width, panel_height):
    drawing = svg2rlg(svg_path)

    # Calculate scale to fit inside the panel
    scale_x = panel_width / drawing.width
    scale_y = panel_height / drawing.height
    scale = min(scale_x, scale_y) * 0.95  # slightly shrink to add margin
    drawing.scale(scale, scale)

    svg_x = x_panel + (panel_width - drawing.width * scale) / 2
    svg_y = y_panel + (panel_height - drawing.height * scale) / 2 - 15  # slight vertical adjustment

    renderPDF.draw(drawing, c, svg_x, svg_y)

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # White background
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Grid
    third = height / 3
    c.setStrokeColor(HexColor("#d90d0d"))
    c.setLineWidth(2)
    c.line(0, third, width, third)
    c.line(0, 2 * third, width, 2 * third)
    c.line(width / 2, 2 * third, width / 2, height)
    c.line(width / 2, 0, width / 2, third)

    # Insert SVGs
    panel_width = width / 2
    panel_height = third

    draw_svg(c, "1.svg", 0, 2 * third, panel_width, panel_height)      # Top-Left
    draw_svg(c, "2.svg", width / 2, 2 * third, panel_width, panel_height)  # Top-Right

    # Read and split text
    with open("readme.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    sentences = re.split(r'(?<=\.)\s+', content)

    # Text settings
    c.setFillColor(HexColor("#0056a9"))
    font = "Courier"
    size = 12
    c.setFont(font, size)
    lh = size * 1.2
    padding = 12

    layout = [
        (width / 2, third, 2 * third),      # Sentence 3
        (width * 0.25, 0, third),           # Sentence 4
        (width * 0.75, 0, third)            # Sentence 5
    ]

    # Write the last 3 sentences
    for index, orig_sentence in enumerate(sentences[2:5]):
        x_center, y_bot, y_top = layout[index]
        section_h = y_top - y_bot
        start_y = y_top - padding - size

        match = re.search(r'\(?\bhttps?://\S+\b\)?', orig_sentence)
        if match:
            url = match.group(0).strip("()")
            sent = orig_sentence.replace(match.group(0), "").strip(" .") + "."
        else:
            url = None
            sent = orig_sentence

        tw = width * 0.45
        lines = simpleSplit(sent, font, size, tw)

        max_width = min(tw, max(c.stringWidth(line, font, size) for line in lines))
        left_x = x_center - max_width / 2
        right_x = x_center + max_width / 2
        top_y = start_y + size
        bottom_y = start_y - lh * (len(lines) - 1) - 2

        current_y = start_y
        for line in lines:
            c.drawCentredString(x_center, current_y, line)
            current_y -= lh

        if url:
            c.linkURL(url, (left_x, bottom_y, right_x, top_y), relative=0)

    c.showPage()
    c.save()
    print("Success:", filename)

if __name__ == "__main__":
    create_pdf("comic.pdf")
