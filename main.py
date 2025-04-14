import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Fill background
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Line color and spacing
    line_color = HexColor("#d90d0d")
    c.setStrokeColor(line_color)
    c.setLineWidth(2)
    third_height = height / 3

    # Horizontal lines
    c.line(0, third_height, width, third_height)
    c.line(0, 2 * third_height, width, 2 * third_height)

    # Vertical lines (for top and bottom thirds)
    c.line(width / 2, 2 * third_height, width / 2, height)  # top third
    c.line(width / 2, 0, width / 2, third_height)           # bottom third

    # Read sentences
    with open("readme.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    sentences = re.split(r'(?<=\.)\s+', content)

    # Set text appearance
    c.setFillColor(HexColor("#0056a9"))
    font_name = "Courier"
    font_size = 12
    c.setFont(font_name, font_size)
    line_height = font_size * 1.2

    # Layout map: (x_center, y_bottom, y_top)
    layout_map = [
        (width * 0.25, 2 * third_height, height),     # Sentence 1
        (width * 0.75, 2 * third_height, height),     # Sentence 2
        (width / 2, third_height, 2 * third_height),  # Sentence 3
        (width * 0.25, 0, third_height),              # Sentence 4
        (width * 0.75, 0, third_height)               # Sentence 5
    ]

    # Draw sentences
    for index, orig_sentence in enumerate(sentences):
        if index >= 5:
            break

        x_center, y_bottom, y_top = layout_map[index]
        section_height = y_top - y_bottom
        padding_from_top = 12
        start_y = y_top - padding_from_top - font_size

        # Detect and strip URL
        match = re.search(r'\(?\bhttps?://\S+\b\)?', orig_sentence)
        url = None
        if match:
            url = match.group(0).strip("()")
            sentence = orig_sentence.replace(match.group(0), "").strip(" .") + "."
        else:
            sentence = orig_sentence

        # Determine max width based on section
        if index == 2:  # Middle section (sentence 3)
            text_width_limit = width * 0.9
        else:
            text_width_limit = width * 0.45

        wrapped_lines = simpleSplit(sentence, font_name, font_size, text_width_limit)

        # Warn if the text may overflow vertically
        required_height = line_height * len(wrapped_lines)
        available_height = section_height - 24  # 12pt top & bottom padding
        if required_height > available_height:
            print(f"⚠️ Warning: Sentence {5 - index} may overflow its box.")

        # Bounding box for optional hyperlink
        max_line_width = min(text_width_limit, max(c.stringWidth(line, font_name, font_size) for line in wrapped_lines))
        left_x = x_center - max_line_width / 2
        right_x = x_center + max_line_width / 2
        top_y = start_y + font_size
        bottom_y = start_y - line_height * (len(wrapped_lines) - 1) - 2

        # Draw text
        current_y = start_y
        for line in wrapped_lines:
            c.drawCentredString(x_center, current_y, line)
            current_y -= line_height

        # Add hyperlink if present
        if url:
            c.linkURL(url, (left_x, bottom_y, right_x, top_y), relative=0)

    c.showPage()
    c.save()

if __name__ == "__main__":
    create_pdf("comic.pdf")
