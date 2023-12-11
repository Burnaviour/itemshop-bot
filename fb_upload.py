import os
import datetime as dt
import requests
from dotenv import load_dotenv
from emoji import emojize

load_dotenv()


API_TOKEN = os.getenv("API_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")  # You need the Page ID to post to a specific page
print(API_TOKEN)
date = dt.datetime.now().strftime("%d/%m/%Y")
day = dt.datetime.now().strftime("%A")   
alram=emojize(':alarm_clock:')
shop=emojize(':shopping_cart:')

message = f"Fortnite Item Shop {shop}\n{alram} {day}, {date}\nUse code 'BRNYT' to support me! #EpicPartner \n\n #fortnite #fortniteitemshop #fortniteitemshoplive #fortniteitemshopdaily #fortniteitemshopupdate #fortniteitemshopnow #fortniteitemshopnew #fortniteitemshopnews #fortniteitemsh\n"
image_path = "final_image.jpeg"
if API_TOKEN and PAGE_ID and os.path.isfile(image_path) and os.path.getsize(image_path) < 4 * 1024 * 1024:
    print("Posting to Facebook...",PAGE_ID)
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
    params = {"access_token": API_TOKEN, "message": message}
    with open(image_path, "rb") as image_file:
        files = {"source": image_file}
        try:
            print("Uploading image...", image_file)
            response = requests.post(url, params=params, files=files)
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
else:
    print("Invalid image file or missing API_TOKEN or PAGE_ID.")