import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Fill the page with a white background (#ffffff)
    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Draw four horizontal lines in color #d90d0d to split the page into 5 equal sections
    line_color = HexColor("#d90d0d")
    c.setStrokeColor(line_color)
    c.setLineWidth(2)
    for i in range(1, 5):
        y = (height * i) / 5
        c.line(0, y, width, y)

    # Read sentences from readme.txt (all sentences on one line)
    with open("readme.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
    # Split sentences using a regex that looks for whitespace following a period.
    sentences = re.split(r'(?<=\.)\s+', content)
    sentences.reverse()  # Reverse the order of sentences

    # Set text color and font properties
    c.setFillColor(HexColor("#0056a9"))
    font_name = "Courier"
    font_size = 12
    c.setFont(font_name, font_size)

    # Define the maximum width for the text (e.g., 90% of the page width) and the line height
    max_text_width = width * 0.9
    line_height = font_size * 1.2

    # Calculate the height of each section
    section_height = height / 5

    # Process each sentence in its section
    for index, orig_sentence in enumerate(sentences):
        # Attempt to extract a URL using a regex.
        # This regex will match strings that begin with http/https and end at a whitespace or closing parenthesis.
        match = re.search(r'\(?\bhttps?://\S+\b\)?', orig_sentence)
        url = None
        if match:
            # Strip leading/trailing parentheses if they exist.
            url = match.group(0).strip("()")
            # Remove the URL portion from the sentence so it doesn’t show up in the text.
            sentence = orig_sentence.replace(match.group(0), "").strip(" .") + "."
        else:
            sentence = orig_sentence

        # Wrap the sentence into lines that do not exceed max_text_width.
        wrapped_lines = simpleSplit(sentence, font_name, font_size, max_text_width)

        # Calculate the starting vertical position near the top of the section.
        section_bottom = section_height * index
        padding_from_top = 12  # Adjust this value to change the distance from the top edge of the section.
        start_y = section_bottom + section_height - padding_from_top - font_size

        # For hyperlink annotation, determine the bounding rectangle of the text block.
        max_line_width = max(c.stringWidth(line, font_name, font_size) for line in wrapped_lines)
        left_x = width / 2 - max_line_width / 2
        right_x = width / 2 + max_line_width / 2
        top_y = start_y + font_size  # approximate ascent.
        bottom_y = start_y - line_height * (len(wrapped_lines) - 1) - 2  # a small padding.

        # Draw each wrapped line centered horizontally.
        current_y = start_y
        for line in wrapped_lines:
            c.drawCentredString(width / 2, current_y, line)
            current_y -= line_height

        # If a URL was found, add a hyperlink annotation over the entire text block.
        if url:
            c.linkURL(url, (left_x, bottom_y, right_x, top_y), relative=0)

    c.showPage()
    c.save()

if __name__ == "__main__":
    create_pdf("comic.pdf")

