import logging

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os


def create_loading_bar_image(progress):
    # Loading_Image/navy2.jpg
    image_path = os.path.join("Loading_Image", "navy2.jpg")
    font_path = os.path.join("Loading_Image", "fortnite.otf")
    loaded_image = Image.open(image_path)  # Background Image Widht 4096, Height 2726
    resize_width, resize_height = 1280, 960
    resized_image = loaded_image.resize((resize_width, resize_height), Image.NEAREST)
    width, height = resized_image.size
    #print(f"Width:{width}, Height:{height}")

    # Drawing the outer rectangle of the loading bar.

    draw = ImageDraw.Draw(resized_image)
    # Rectangle dimensions
    rectangle_width = resize_width * 0.8  # 1000
    rectangle_height = resize_height * 0.2  # 200

    # Calculate the coordinates of the top-left corner
    x0 = (width - rectangle_width) // 2
    y0 = (height - rectangle_height) // 2

    # Calculate the coordinates of the bottom-right corner
    x1 = x0 + rectangle_width
    y1 = y0 + rectangle_height

    draw.rectangle([x0, y0, x1, y1], outline="#0096FF", width=4)

    # Drawing inner rectangle to show filled bar.
    fill_width = int((width - 128) * progress)
    draw.rectangle([x0 + 10, y0 + 10, fill_width - 10, y1 - 10], fill="#00FFFF")  # Inner

    #print(f"x0:{x0}, y0:{y0}, x1:{x1}, y1:{y1}")

    # Rectangle round behind the percentage
    draw.rounded_rectangle([550, 450, 700, 520], radius=50, fill="#ffffff")

    # Season progress precentage calculations

    season_end_date = datetime(2024, 3, 8)
    chapter_5_launch_date = datetime(2023, 12, 3)
    total_days = season_end_date.date() - chapter_5_launch_date.date()
    current_date = datetime.now()
    days_diff = current_date.date() - chapter_5_launch_date.date()
    progress = days_diff.days / total_days.days
    progress_percentage = progress * 100
    int_perc = int(progress_percentage)

    text_position = [550 + 38, 450 + 15, 700 - 50, 520 - 100]
    # text_position = [650, 450, 750, 530]

    font_size = 50
    title_font_size = 100

    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(font_path, title_font_size)

    draw.text(text_position, f"{int_perc} %", fill="black", font=font)

    title_position = [500, 220]

    draw.text(title_position, f"FORTNITE", fill="white", font=title_font)

    title2_position = [400, 300]

    draw.text(title2_position, f"UNDERGROUND", fill="white", font=title_font)

    # title3_position = [325, 300]
    #
    # draw.text(title3_position, f"SEASON PROGRESS", fill="white", font=title_font)

    below_title = [490, 580]
    draw.text(below_title, f"SEASON 1", fill="white", font=title_font)

    c5_logo_path = os.path.join("Loading_Image", "IMG_4654.png")
    battle_bus_path = os.path.join("Loading_Image", "white_bus.PNG")
    battle_bus_logo = Image.open(battle_bus_path)
    battle_bus_logo = battle_bus_logo.resize((200, 200), Image.NEAREST)
    chapter_logo = Image.open(c5_logo_path)
    chapter_logo = chapter_logo.resize((200, 200), Image.NEAREST)

    resized_image.paste(battle_bus_logo, [1100, 0], battle_bus_logo)
    resized_image.paste(chapter_logo, [0, 0], chapter_logo)
    # FFB700 Yellow
    number_5 = [80, 65]
    draw.text(number_5, f"5", fill="white", font=title_font)

    cc_back_path = os.path.join("Loading_Image", "FNCS_BG.JPG")
    cc_back_logo = Image.open(cc_back_path).convert('RGBA')
    cc_back_logo = cc_back_logo.resize((400, 200), Image.NEAREST)
    resized_image.paste(cc_back_logo, [900, 760], cc_back_logo)

    support_code_pos = [1040, 790]
    support_code_pos2 = [1025, 840]
    support_code_pos3 = [1015, 890]
    support_font_size = 65
    support_code_font = ImageFont.truetype(font_path, support_font_size)
    draw.text(support_code_pos, f"USE", font=support_code_font)
    draw.text(support_code_pos2, f"CODE", font=support_code_font)
    draw.text(support_code_pos3, f"BRNYT", font=support_code_font)
    return resized_image


def display_loading_bar():
    season_end_date = datetime(2024, 3, 8)
    chapter_5_launch_date = datetime(2023, 12, 3)
    total_days = season_end_date.date() - chapter_5_launch_date.date()
    current_date = datetime.now()
    days_diff = current_date.date() - chapter_5_launch_date.date()
    progress = days_diff.days / total_days.days
    progress_percentage = int(progress * 100)
    loading_bar = create_loading_bar_image(progress)
    try:
        loading_bar.save("Loading_Bar_Img.png", format="PNG")
        return progress_percentage, True
    except Exception as e:
        logging.error("Failed to save image: %s",e)
        return False


if __name__ == "__main__":
    display_loading_bar()
