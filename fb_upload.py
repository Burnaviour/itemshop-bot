import os
import datetime as dt
import requests
import logging
from dotenv import load_dotenv
from emoji import emojize

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("API_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")  # You need the Page ID to post to a specific page
logger.info(API_TOKEN)
date = dt.datetime.now().strftime("%d/%m/%Y")
day = dt.datetime.now().strftime("%A")   
alram=emojize(':alarm_clock:')
shop=emojize(':shopping_cart:')
heart = emojize(':heartpulse:')
message = f"Fortnite Item Shop {shop}\n{alram} {day}, {date}\n{heart} Use code 'BRNYT' to support me! #EpicPartner \n\n #fortnite #fortniteitemshop #fortniteitemshoplive #fortniteitemshopdaily #fortniteitemshopupdate #fortniteitemshopnow #fortniteitemshopnew #fortniteitemshopnews #fortniteitemsh\n"
image_path = "final_image.jpeg"
if API_TOKEN and PAGE_ID and os.path.isfile(image_path) and os.path.getsize(image_path) < 4 * 1024 * 1024:
    logger.info("Posting to Facebook... PAGE_ID: %s", PAGE_ID)
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
    params = {"access_token": API_TOKEN, "message": message}
    with open(image_path, "rb") as image_file:
        files = {"source": image_file}
        try:
            logger.info("Uploading image... %s", image_file)
            response = requests.post(url, params=params, files=files)
            logger.info(response.json())
        except requests.exceptions.RequestException as e:
            logger.error("Error: %s", e)
else:
    logger.error("Invalid image file or missing API_TOKEN or PAGE_ID.")
