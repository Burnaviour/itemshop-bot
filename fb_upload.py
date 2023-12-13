import os
import datetime as dt
import requests
import logging
from dotenv import load_dotenv
from emoji import emojize
import aiohttp
import asyncio
logging.basicConfig(filename='fb_logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



def get_current_date():
    return dt.datetime.now().strftime("%d/%m/%Y")

def get_current_day():
    return dt.datetime.now().strftime("%A")

def get_message():
    alram = emojize(':alarm_clock:')
    shop = emojize(':shopping_cart:')
    heart = emojize(':red_heart:')
    day = get_current_day()
    date = get_current_date()
    return f"Fortnite Item Shop {shop}\n{alram} {day}, {date}\n {heart} Use code 'BRNYT' to support me! #EpicPartner \n\n #fortnite #fortniteitemshop #fortniteitemshoplive #fortniteitemshopdaily #fortniteitemshopupdate #fortniteitemshopnow #fortniteitemshopnew #fortniteitemshopnews #fortniteitemsh\n"

async def post_to_facebook(image_path):
    API_TOKEN = os.getenv("API_TOKEN")
    PAGE_ID = os.getenv("PAGE_ID")
    if API_TOKEN and PAGE_ID and os.path.isfile(image_path) and os.path.getsize(image_path) < 4 * 1024 * 1024:
        logger.info("Posting to Facebook... PAGE_ID: %s", PAGE_ID)
        url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
        message = get_message()
        data = aiohttp.FormData()
        data.add_field('source',
                       open(image_path, 'rb'),
                       filename='final_image.png',
                       content_type='image/jpeg')
        data.add_field('access_token', API_TOKEN)
        data.add_field('message', message)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                logger.info(await response.text())
                logger.info("Uploaded image to Facebook.")
    else:
        logger.error("Invalid image file or missing API_TOKEN or PAGE_ID.")

def main():
    load_dotenv()
    image_path = "final_image.png"
    asyncio.run(post_to_facebook(image_path))

if __name__ == "__main__":
    main()
