import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def draw_svg(c, svg_path, x_panel, y_panel, panel_width, panel_height, scale_factor=0.95):
    drawing = svg2rlg(svg_path)
    scale_x = panel_width / drawing.width
    scale_y = panel_height / drawing.height
    scale = min(scale_x, scale_y) * scale_factor
    drawing.scale(scale, scale)

    svg_x = x_panel + (panel_width - drawing.width * scale) / 2
    svg_y = y_panel + (panel_height - drawing.height * scale) / 2 - 10

    renderPDF.draw(drawing, c, svg_x, svg_y)

def draw_text(c, sentence, font, size, x_center, y_bot, y_top, color, max_width_ratio=0.85):
    lh = size * 1.2
    padding = 10
    panel_width = (x_center * 2) if x_center <= 300 else (612 - x_center) * 2
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
    lines = lines[:max_lines]

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
    blue = HexColor("#0056a9")
    red = HexColor("#d90d0d")
    font = "Courier"
    font_size = 12

    # Panel layout heights
    top_h = height * (1/3)
    bottom_h = height * (1/5)
    middle_h = height - top_h - bottom_h

    # Y-positions
    y_top = height
    y_middle = bottom_h
    y_bottom = 0

    # White background first
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Red panel divider lines
    c.setStrokeColor(red)
    c.setLineWidth(2)
    c.line(0, bottom_h, width, bottom_h)
    c.line(0, bottom_h + middle_h, width, bottom_h + middle_h)
    c.line(width / 2, bottom_h + middle_h, width / 2, height)
    c.line(width / 2, 0, width / 2, bottom_h)

    panel_w = width / 2

    # === Load sentences from readme.txt ===
    with open("readme.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    sentences = re.split(r'(?<=\.)\s+', content)
    while len(sentences) < 5:
        sentences.append("")

    c.setFont(font, font_size)
    c.setFillColor(blue)

    # Panel 1: Top-Left
    draw_svg(c, "1.svg", 0, y_middle + middle_h - 5, panel_w, top_h, scale_factor=0.95)
    draw_text(c, sentences[0], font, font_size, width * 0.25, y_middle + middle_h, y_top, blue)

    # Panel 2: Top-Right
    draw_svg(c, "2.svg", width / 2, y_middle + middle_h - 20, panel_w, top_h)
    draw_text(c, sentences[1], font, font_size, width * 0.75, y_middle + middle_h, y_top, blue)

    # Panel 3: Middle
    draw_svg(c, "3.svg", 0, y_middle, width, middle_h, scale_factor=0.9)
    draw_text(c, sentences[2], font, font_size, width / 2, y_middle, y_middle + middle_h, blue)

    # Panel 4: Bottom-Left — draw text first, then image lower in panel
    draw_text(c, sentences[3], font, font_size, width * 0.25, y_bottom + bottom_h * 0.3, y_bottom + bottom_h, blue)
    draw_svg(c, "4.svg", 0, y_bottom, panel_w, bottom_h * 0.7, scale_factor=0.7)

    # Panel 5: Bottom-Right — draw text first, then sad face SVG below
    draw_text(c, sentences[4], font, font_size, width * 0.75, y_bottom + bottom_h * 0.3, y_bottom + bottom_h, blue)
    draw_svg(c, "5.svg", width / 2, y_bottom, panel_w, bottom_h * 0.6, scale_factor=0.7)

    c.showPage()
    c.save()
    print("Success:", filename)

if __name__ == "__main__":
    create_pdf("comic.pdf")
