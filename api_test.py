import os
from dotenv import load_dotenv
import requests
import logging
import math
import io
from PIL import Image, ImageDraw, ImageFont
import datetime

logging.basicConfig(filename='api_test.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def generate_item_shop_image():
    load_dotenv()

    TOKEN = os.getenv('TOKEN')
    URL = "https://fortniteapi.io/v2/shop?lang=en"

    # Configure logging


    obj = requests.get(URL, headers={"Authorization": TOKEN}, timeout=10)
    data = obj.json()['shop']
    picture_resolutions = 1080
    picture_spacing = 50
    x_offset = 200
    text_off_set = 1080
    y_offset = 200 + text_off_set
    images_in_row = 0
    count = 0

    content = []

    for i in data:
        logging.info("started %s", i['mainId'])
        try:
            display_name = i['displayName']
            if i['displayAssets']:
                media_url = i['displayAssets'][0]['full_background'] or False
                count += 1
                response = requests.get(media_url, stream=True)
                logging.info("%d Downloaded and added image for %s", count, display_name)

                content.append(response)
        except requests.exceptions.RequestException as e:
            logging.error("An error occurred: %s", e)

    pictures = math.sqrt(len(content))
    pictures = math.ceil(pictures) if type(pictures) == float else pictures

    size_calc_width = picture_resolutions * pictures + (x_offset*2) + ((pictures-1)*picture_spacing)
    size_calc_height = picture_resolutions * pictures + 400 + ((pictures-1)*picture_spacing) + text_off_set
    print(size_calc_width, size_calc_height)

    img = Image.new('RGB',(int(size_calc_width),int(size_calc_height)),color=(144,238,144))

    for picture in content:
        img_temp = Image.open(io.BytesIO(picture.content))
        img_temp = img_temp.resize((1080, 1080))  
        img.paste(img_temp, (x_offset, y_offset))
        x_offset += 1080 + picture_spacing
        images_in_row += 1
        if images_in_row == pictures:
            images_in_row = 0
            x_offset = 200
            y_offset += 1080 + picture_spacing
        logging.info("done")

    # img.save('new_image.png')

    draw = ImageDraw.Draw(img)
    font_path = os.path.join("static/fonts", "fortnite.otf")
    
    font = ImageFont.truetype(font_path, size=800)
    font2 = ImageFont.truetype(font_path, size=200)
    text = "Daily Item Shop"

    width = font.getlength(text)

    fontcenter = (size_calc_width - width) / 2

    draw.text((fontcenter+16,250+16), text, fill="black", font=font)
    draw.text((fontcenter,250), text, fill="white", font=font)

    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y")
    draw.text((100,250), date, fill="white", font=font2)
    img.save("final_image1.png", format="PNG")
    if os.path.exists('final_image1.png'):
        _extracted_from_generate_item_shop_image_78()
        return True


# TODO Rename this here and in `generate_item_shop_image`
def _extracted_from_generate_item_shop_image_78():
    image = Image.open('final_image1.png')
    width, height = image.size
    new_width = 2048
    new_height = int(new_width * height / width)
    image = image.resize((new_width, new_height))
    image.save('final_image.png')

