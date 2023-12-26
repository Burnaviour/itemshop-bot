from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


# width, height,
import os

def create_loading_bar(progress, text="", text2=""):
    # image = Image.new("RGB", (width + 20, height + 27), "white")
    # custom_width, custom_height = width + 20, height + 27
    width = 500
    height = 100
    r_width = 520
    r_height = 127
    image_path = os.path.join("Loading_Image", "navy2.jpg")
    loaded_image = Image.open(image_path)
    resized_image = loaded_image.resize((r_width, r_height))

    # draw = ImageDraw.Draw(image)
    draw = ImageDraw.Draw(resized_image)

    draw.rectangle([(30, 30), (width - 10, height - 10)], outline="#0096FF", width=3)  # Border

    fill_width = int((width - 30) * progress)

    draw.rectangle([(40, 35), (10 + fill_width, height - 16)], fill="#00FFFF")  # Inner

    font_size = 34
    font_path = os.path.join("Fortnite/fortnite", "fortnite.otf")
    font = ImageFont.truetype(font_path, font_size)

    text_width, text_height = 200, 400
    # text_position = ((width - text_width) // 2, (height - text_height) // 2)
    text_position = (180, 0)  # Old (225,0)
    text_position2 = (180, 90)  # old (100,90)

    draw.text(text_position, text, fill="white", font=font)
    draw.text(text_position2, text2, fill="white", font=font)

    season_end_date = datetime(2024, 3, 8)
    chapter_5_launch_date = datetime(2023, 12, 3)
    total_days = season_end_date.date() - chapter_5_launch_date.date()
    current_date = datetime.now()
    days_diff = current_date.date() - chapter_5_launch_date.date()
    progress = days_diff.days / total_days.days
    progress_percentage = progress * 100
    int_perc = int(progress_percentage)

    text_position3 = (250, 50)

    draw.text(text_position3, f"{int_perc} %", fill="white", font=font)

    return resized_image


def display_loading_bar():
    season_end_date = datetime(2024, 3, 8)
    chapter_5_launch_date = datetime(2023, 12, 3)
    total_days = season_end_date.date() - chapter_5_launch_date.date()
    current_date = datetime.now()
    days_diff = current_date.date() - chapter_5_launch_date.date()
    progress = days_diff.days / total_days.days
    loading_bar = create_loading_bar(progress, text="Fortnite Ch5 S1", text2="Use Code BRNYT")
    loading_bar.save("Season Progress.png")


if __name__ == "__main__":
    display_loading_bar()
