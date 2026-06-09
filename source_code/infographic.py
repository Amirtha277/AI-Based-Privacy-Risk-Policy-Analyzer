from PIL import Image, ImageDraw, ImageFont
from translation import translate_text
import os


def draw_multiline_text(draw, text, x, y, max_width, font, line_spacing=18):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        w = draw.textlength(test_line, font=font)

        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    lines.append(current_line.strip())

    for line in lines:
        draw.text((x, y), line, fill="#222222", font=font)
        y += font.size + line_spacing

    return y


def generate_infographic(score, risks, lang):

    width, height = 700, 500
    img = Image.new("RGB", (width, height), "#f4f6f8")
    draw = ImageDraw.Draw(img)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Auto-translate labels
    title = translate_text("Privacy Risk Summary", lang)
    risk_label = translate_text("Risk Score", lang)

    # ---------------- FONT SETTINGS ----------------

    try:
        if lang == "ta":
            font_path = os.path.join(BASE_DIR, "fonts", "NotoSerifTamil-Regular.ttf")
            title_font = ImageFont.truetype(font_path, 34)
            normal_font = ImageFont.truetype(font_path, 24)
            score_font = ImageFont.truetype(font_path, 20)
        else:
            font_path = "C:/Windows/Fonts/arial.ttf"
            title_font = ImageFont.truetype(font_path, 38)
            normal_font = ImageFont.truetype(font_path, 24)
            score_font = ImageFont.truetype(font_path, 22)

    except:
        title_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        score_font = ImageFont.load_default()

    # ---------------- TITLE ----------------

    draw.text(
        (width // 2, 70),
        title,
        fill="#111111",
        font=title_font,
        anchor="mm"
    )

    # ---------------- SCORE BOX ----------------

    box_x1, box_y1 = 480, 150
    box_x2, box_y2 = 660, 270

    draw.rounded_rectangle(
        (box_x1, box_y1, box_x2, box_y2),
        radius=30,
        fill="#1f4e5f"
    )

    draw.text(
        ((box_x1 + box_x2) // 2, box_y1 + 50),
        risk_label,
        fill="white",
        font=normal_font,
        anchor="mm"
    )

    draw.text(
        ((box_x1 + box_x2) // 2, box_y1 + 105),
        f"{score}/100",
        fill="white",
        font=score_font,
        anchor="mm"
    )

    # ---------------- RISKS SECTION ----------------

    y = 160

    for clause, level in risks[:4]:

        if "High" in level:
            color = "#e63946"
        elif "Medium" in level:
            color = "#f4a261"
        else:
            color = "#2a9d8f"

        draw.ellipse((60, y + 10, 80, y + 30), fill=color)

        y = draw_multiline_text(draw, clause, 110, y, 320, normal_font)
        y += 25

    # Save clean image
    output_path = "static/infographic.png"
    img.save(output_path)