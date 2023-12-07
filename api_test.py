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

obj = requests.get(URL, headers={"Authorization": TOKEN}, timeout=10)
data = obj.json()['shop']
font_path = os.path.join(os.getcwd(), "static/fonts", "fortnite.otf")
x_offset = 100
y_offset = 200
images_in_row = 0
count = 0
# num_images_in_row = 4
# num_images = len(data)
# img_width = 500
# num_rows = (num_images + num_images_in_row - 1) // num_images_in_row
# image_size = (img_width * num_images_in_row, img_width * num_rows)

# Use the 'image_size' variable to resize the blank image






#img = Image.new('RGB',(2250,3300))

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
        
pictures = len(content)//4

size_calc_width = 1080 * 4 + 350
size_calc_height = 1080 * pictures + 400 + ((pictures-1)*50)
print(size_calc_width, size_calc_height)
img = Image.new('RGB',(int(size_calc_width),int(size_calc_height)),color=(255,48,65))

for picture in content:
    img_temp = Image.open(io.BytesIO(picture.content))
    img_temp = img_temp.resize((1080, 1080))
    img.paste(img_temp, (x_offset, y_offset))
    x_offset += 1080 + 50
    images_in_row += 1
    if images_in_row == 4:
        images_in_row = 0
        x_offset = 100
        y_offset += 1080 + 50
    logging.info("doen")


img.save('new_image.png')









        

#         # Open the image with Pillow
#         img_temp = Image.open(io.BytesIO(response.content))
#         # img_temp.save(f'{display_name}.png')

#         # Resize the image if needed
#         img_temp = img_temp.resize((1080, 1080))

#         # Paste the image onto the blank image
#         #img.paste(img_temp, (x_offset, y_offset))

#         x_offset += 500
#         images_in_row += 1

#         # If the row is full, move to the next row
#         if images_in_row == 4:
#             images_in_row = 0
#             x_offset = 0
#             y_offset += 500

#         count += 1
#         logging.info("%d Downloaded and added image for %s", count, display_name)
   

# # Save the final image
# img.save('new_image.png')