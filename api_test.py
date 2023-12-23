import os
from dotenv import load_dotenv
import requests
import logging
import math
import io
from PIL import Image, ImageDraw, ImageFont,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import datetime
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# session = requests.Session()
# retry = Retry(total=3, backoff_factor=0.1, status_forcelist=(500, 502, 503, 504))
# adapter = HTTPAdapter(max_retries=retry,pool_connections=100, pool_maxsize=100)
# session.mount('http://', adapter)
# session.mount('https://', adapter)

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
            if i['displayAssets'] and len( i['displayAssets']) >0:
                media_url = i['displayAssets'][0]['full_background'] or False
                
                # response = requests.get(media_url, stream=True,timeout=10)
                content.append(media_url)
                # print(content)
            logger.info("Link added %s", display_name)
        except requests.exceptions.RequestException as e:
            logging.error("An error occurred: %s", e)

    pictures = math.sqrt(len(content))
    pictures = math.ceil(pictures) if type(pictures) == float else pictures

    size_calc_width = picture_resolutions * pictures + (x_offset*2) + ((pictures-1)*picture_spacing)
    size_calc_height = picture_resolutions * pictures + 400 + ((pictures-1)*picture_spacing) + text_off_set
    print(size_calc_width, size_calc_height)

    img = Image.new('RGB',(int(size_calc_width),int(size_calc_height)),color=(144,238,144))

    for picture_url in content:
        count += 1
        try:
            response = requests.get(picture_url, timeout=10)  # Use a 10-second timeout
            response.raise_for_status()  # Raise an exception if the request was not successful
        except (requests.RequestException, IOError) as e:
            logging.error("Failed to download image: %s", e)
            continue
        try:
            img_temp = Image.open(io.BytesIO(response.content))
        except OSError as e:
            logging.error("Failed to open image: %s", e)            
            continue
        img_temp = img_temp.resize((1080, 1080))  
        img.paste(img_temp, (x_offset, y_offset))
        x_offset += 1080 + picture_spacing
        images_in_row += 1
        if images_in_row == pictures:
            images_in_row = 0
            x_offset = 200
            y_offset += 1080 + picture_spacing
        logging.info("Image %d pasted",count)

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
    
    try:
        img.save("final_image1.png", format="PNG")
        _extracted_from_generate_item_shop_image_78()
        return True
    except Exception as e:
        logging.error("Failed to save image: %s",e)
        return False


# TODO Rename this here and in `generate_item_shop_image`
def _extracted_from_generate_item_shop_image_78():
    image = Image.open('final_image1.png')
    width, height = image.size
    new_width = 2048
    new_height = int(new_width * height / width)
    image = image.resize((new_width, new_height))
    image.save('final_image.png')
