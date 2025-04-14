import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def draw_svg(c, svg_path, x_panel, y_panel, panel_width, panel_height):
    drawing = svg2rlg(svg_path)
    scale_x = panel_width / drawing.width
    scale_y = panel_height / drawing.height
    scale = min(scale_x, scale_y) * 0.95
    drawing.scale(scale, scale)

    svg_x = x_panel + (panel_width - drawing.width * scale) / 2
    svg_y = y_panel + (panel_height - drawing.height * scale) / 2 - 15

    renderPDF.draw(drawing, c, svg_x, svg_y)

def draw_text(c, sentence, font, size, x_center, y_bot, y_top, url_color, max_width_ratio=0.85):
    lh = size * 1.2
    padding = 10
    panel_width = (x_center * 2) if x_center <= 300 else (612 - x_center) * 2  # Estimate width by panel position
    text_width = panel_width * max_width_ratio

    max_text_height = y_top - y_bot - 2 * padding
    max_lines = int(max_text_height // lh)

    match = re.search(r'\(?\bhttps?://\S+\b\)?', sentence)
    if match:
        url = match.group(0).strip("()")
        sent = sentence.replace(match.group(0), "").strip(" .") + "."
    else:
        url = None
        sent = sentence

    lines = simpleSplit(sent, font, size, text_width)
    lines = lines[:max_lines]  # prevent overflow

    start_y = y_top - padding - size
    current_y = start_y

    max_line_width = max(c.stringWidth(line, font, size) for line in lines)
    left_x = x_center - max_line_width / 2
    right_x = x_center + max_line_width / 2
    top_y = start_y + size
    bottom_y = start_y - lh * (len(lines) - 1) - 2

    for line in lines:
        c.drawCentredString(x_center, current_y, line)
        current_y -= lh

    if url:
        c.linkURL(url, (left_x, bottom_y, right_x, top_y), relative=0)

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    third = height / 3
    blue = HexColor("#0056a9")
    red = HexColor("#d90d0d")
    font = "Courier"
    font_size = 12

    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    c.setStrokeColor(red)
    c.setLineWidth(2)
    c.line(0, third, width, third)
    c.line(0, 2 * third, width, 2 * third)
    c.line(width / 2, 2 * third, width / 2, height)
    c.line(width / 2, 0, width / 2, third)

    with open("readme.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    sentences = re.split(r'(?<=\.)\s+', content)

    panel_w = width / 2
    panel_h = third

    c.setFont(font, font_size)
    c.setFillColor(blue)

    # Top-Left
    draw_svg(c, "1.svg", 0, 2 * third, panel_w, panel_h)
    draw_text(c, sentences[0], font, font_size, width * 0.25, 2 * third, height, blue)

    # Top-Right
    draw_svg(c, "2.svg", width / 2, 2 * third, panel_w, panel_h)
    draw_text(c, sentences[1], font, font_size, width * 0.75, 2 * third, height, blue)

    # Middle
    draw_text(c, sentences[2], font, font_size, width / 2, third, 2 * third, blue)

    # Bottom-Left
    draw_text(c, sentences[3], font, font_size, width * 0.25, 0, third, blue)

    # Bottom-Right
    draw_text(c, sentences[4], font, font_size, width * 0.75, 0, third, blue)

    c.showPage()
    c.save()
    print("Success:", filename)

if __name__ == "__main__":
    create_pdf("comic.pdf")
