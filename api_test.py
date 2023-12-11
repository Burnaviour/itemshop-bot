import os
import shutil
from dotenv import load_dotenv
import requests
import logging
import math
import io
from PIL import Image, ImageDraw, ImageFont
from colour import Color
import datetime
import facebook


load_dotenv()

# def compress_image(image, max_size=3110000, initial_quality=90, step=10):
#     """
#     Compress an image, keeping its aspect ratio.
#     :param image: The PIL Image object.
#     :param max_size: The maximum size of the output image, in bytes.
#     :param initial_quality: The initial quality of the image.
#     :param step: The quality reduction step size.
#     :return: The path to the compressed image.
#     """
#     quality = initial_quality

#     # Save the image with reduced quality.
#     temp_path = "final_image.jpg"
#     # Iterate until the size is acceptable.
#     while True:
#         image.save(temp_path)
#         # Check the size.
#         size = os.stat(temp_path).st_size
#         if size <= max_size or quality <= step or size <= 3110000:  # Add condition to terminate loop if size is less than or equal to 4 MB.
#             return temp_path
#         # Reduce the quality for the next iteration.
#         quality -= step

TOKEN = os.getenv('TOKEN')
URL = "https://fortniteapi.io/v2/shop?lang=en"

# Configure logging
logging.basicConfig(filename='api_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

obj = requests.get(URL, headers={"Authorization": TOKEN}, timeout=10)
data = obj.json()['shop']
font_path = os.path.join(os.getcwd(), "static/fonts", "fortnite.otf")
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
red = Color("red")
colors = list(red.range_to(Color("green"),10))
print(colors)


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
font = ImageFont.truetype('/home/muzafar/Desktop/dev/static/fonts/fortnite.otf', size=800)
font2 = ImageFont.truetype('/home/muzafar/Desktop/dev/static/fonts/fortnite.otf', size=200)
text = "Daily Item Shop"

width = font.getlength(text)

fontcenter = (size_calc_width - width) / 2

draw.text((fontcenter+16,250+16), text, fill="black", font=font)
draw.text((fontcenter,250), text, fill="white", font=font)

date = datetime.datetime.now()u
draw.text((100,250), date, fill="white", font=font2)
# img.save("output", format='JPEG', optimize=True, quality=50)
# compressed_image_path = compress_image(image=img)
img.save("final_image.jpeg", format="jpeg",quality=5)
# logging.info(compressed_image_path)