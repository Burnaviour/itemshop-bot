import logging

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os


def create_loading_bar_image(progress):
    # Loading_Image/navy2.jpg
    image_path = os.path.join("Loading_Image", "navy2.jpg")
    font_path = os.path.join("Loading_Image", "fortnite.otf")
    loaded_image = Image.open(image_path)  # Background Image Width 4096, Height 2726
    resize_width, resize_height = 1280, 960
    resized_image = loaded_image.resize((resize_width, resize_height), Image.NEAREST)
    width, height = resized_image.size

    # Drawing the outer rectangle of the loading bar.
    draw = ImageDraw.Draw(resized_image)
    # Rectangle dimensions
    rectangle_width = resize_width * 0.8  # 1000
    rectangle_height = resize_height * 0.2  # date

    # Calculate the coordinates of the top-left corner
    x0 = (width - rectangle_width) // 2
    y0 = (height - rectangle_height) // 2

    # Calculate the coordinates of the bottom-right corner
    x1 = x0 + rectangle_width
    y1 = y0 + rectangle_height

    draw.rectangle([x0, y0, x1, y1], outline="#0096FF", width=4)

    # Drawing inner rectangle to show filled bar.
    fill_width = int((rectangle_width - 20) * progress) + x0 + 10
    draw.rectangle([x0 + 10, y0 + 10, fill_width, y1 - 10], fill="#00FFFF")  # Inner

    # Rectangle round behind the percentage
    draw.rounded_rectangle([550, 450, 700, 520], radius=50, fill="#ffffff")

    # Season progress percentage calculations
    season_end_date = datetime(2024, 5, 24)
    chapter_5_launch_date = datetime(2024, 3, 8)
    total_days = season_end_date.date() - chapter_5_launch_date.date()
    current_date = datetime.now()
    days_diff = current_date.date() - chapter_5_launch_date.date()
    progress = days_diff.days / total_days.days
    progress_percentage = progress * 100
    int_perc = int(progress_percentage)

    text_position = [550 + 38, 450 + 15, 700 - 50, 520 - 100]
    font_size = 50
    title_font_size = 100

    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(font_path, title_font_size)

    draw.text(text_position, f"{int_perc} %", fill="black", font=font)

    title_position = [500, 180]
    draw.text(title_position, f"FORTNITE", fill="white", font=title_font)

    title2_position = [400, 280]
    draw.text(title2_position, f"Myths & Mortals", fill="white", font=title_font)

    below_title = [490, 600]
    draw.text(below_title, f"SEASON 2", fill="white", font=title_font)

    c5_logo_path = os.path.join("Loading_Image", "IMG_4654.png")
    battle_bus_path = os.path.join("Loading_Image", "white_bus.PNG")
    battle_bus_logo = Image.open(battle_bus_path)
    battle_bus_logo = battle_bus_logo.resize((200, 200), Image.NEAREST)
    chapter_logo = Image.open(c5_logo_path)
    chapter_logo = chapter_logo.resize((200, 200), Image.NEAREST)

    resized_image.paste(battle_bus_logo, [1080, 20], battle_bus_logo)
    resized_image.paste(chapter_logo, [20, 20], chapter_logo)

    number_5 = [100, 100]
    draw.text(number_5, f"5", fill="white", font=title_font)

    cc_back_path = os.path.join("Loading_Image", "FNCS_BG.JPG")
    cc_back_logo = Image.open(cc_back_path).convert('RGBA')
    cc_back_logo = cc_back_logo.resize((400, 200), Image.NEAREST)

    support_font_size = 65
    support_code_font = ImageFont.truetype(font_path, support_font_size)
    support_code_pos = [900, 890]
    draw.text(support_code_pos, f"USE CODE:BRNYT", font=support_code_font)

    return resized_image

def display_loading_bar():
    season_end_date = datetime(2024, 5, 24)
    chapter_5_launch_date = datetime(2024, 3, 8)
    total_days = season_end_date.date() - chapter_5_launch_date.date()
    current_date = datetime.now()
    days_diff = current_date.date() - chapter_5_launch_date.date()
    
    progress = days_diff.days / total_days.days
    progress_percentage = int(progress * 100)
    loading_bar = create_loading_bar_image(progress)
    try:
        loading_bar.save("final_loading_bar_img.png", format="PNG")
        return progress_percentage, True
    except Exception as e:
        logging.error("Failed to save image: %s", e)
        return False


if __name__ == "__main__":
    display_loading_bar()
