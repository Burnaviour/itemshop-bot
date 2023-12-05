import os
import shutil
from dotenv import load_dotenv
import requests
import logging
import io
from PIL import Image, ImageDraw, ImageFont


load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = "https://fortniteapi.io/v2/shop?lang=en"

# Configure logging
logging.basicConfig(filename='api_test.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

obj = requests.get(URL, headers={"Authorization": TOKEN})
data = obj.json()['shop']

img = Image.new('RGB', (1500, 500))

x_offset = 0
y_offset = 0
images_in_row = 0
print(len(data))
for i in data:
    logging.info("started %s", i['mainId'])
    try:
        display_name = i['displayName']
        media_url = i['displayAssets'][0]['url']
        response = requests.get(media_url, stream=True)

        # Open the image with Pillow
        img_temp = Image.open(io.BytesIO(response.content))

        # Resize the image if needed
        img_temp = img_temp.resize((250, 250))

        # Paste the image onto the blank image
        img.paste(img_temp, (x_offset, y_offset))

        # Add display name on the image
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 20)
        draw.text((x_offset, y_offset + 250), display_name,
                  font=font, fill=(255, 255, 255))

        x_offset += 250
        images_in_row += 1

        # If the row is full, move to the next row
        if images_in_row == 4:
            images_in_row = 0
            x_offset = 0
            y_offset += 250

        logging.info("Downloaded and added image for %s", display_name)
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred: %s", e)

# Save the final image
img.save('new_image.png')
