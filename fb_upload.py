import os
import datetime as dt
import requests
import logging
from dotenv import load_dotenv
from emoji import emojize
import aiohttp
import asyncio

logging.basicConfig(filename='api_test.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_current_date():
    return dt.datetime.now().strftime("%d/%m/%Y")

def get_current_day():
    return dt.datetime.now().strftime("%A")

def get_message(for_message="itemshop",progress=0.0):
    alram = emojize(':alarm_clock:')
    if for_message == "itemshop": 
        shop = emojize(':shopping_cart:')
        heart = emojize(':red_heart:')
        day = get_current_day()
        date = get_current_date()
        return f"Fortnite Item Shop {shop}\n{alram} {day}, {date}\n {heart} Use code 'BRNYT' to support me! #EpicPartner \n\n #fortnite #fortniteitemshop #fortniteitemshoplive #fortniteitemshopdaily #fortniteitemshopupdate #fortniteitemshopnow #fortniteitemshopnew #fortniteitemshopnews #fortniteitemsh\n"
    elif for_message == "loading_bar":
        season_end_date = dt.datetime(2024, 3, 8)
        chapter_5_launch_date = dt.datetime(2023, 12, 3)
        total_days = (season_end_date.date() - dt.datetime.now().date()).days
        end_date_str = f"The season ends on {season_end_date.date().strftime('%d/%m/%Y')}"
        remaining_days_str = f"There are {total_days} days remaining in the season"
        timer = emojize(':timer_clock:')
        season_name= "Chapter 5 Season 1"
        return f"Fortnite {season_name} \n\n {timer}   Progress {progress}% Completed \n\n {end_date_str} \n\n {remaining_days_str} \n\n #fortnite #seasonprogress #chapter5season1\n"
async def post_to_facebook(image_path, for_message="itemshop",progress=0.0):
    
    API_TOKEN = os.environ.get("API_TOKEN")
    PAGE_ID = os.environ.get("PAGE_ID")
    if API_TOKEN and PAGE_ID and os.path.isfile(image_path) and os.path.getsize(image_path) < 4 * 1024 * 1024:
        logger.info("Posting to Facebook... PAGE_ID: %s", PAGE_ID)
        url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
        message = get_message(for_message=for_message,progress=progress)
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
        os.remove(image_path)
               
    else:
        logger.error("Invalid image file or missing API_TOKEN or PAGE_ID.")

def main(image_path, for_message,progress=0):
    image_path = image_path
    asyncio.run(post_to_facebook(image_path,for_message=for_message,progress=progress))

if __name__ == "__main__":
    print(get_message('loading_bar'))
    # main("final_image.png","itemshop")
