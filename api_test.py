import os
import shutil
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = "https://fortniteapi.io/v2/shop?lang=en"

obj = requests.get(URL, headers={"Authorization": TOKEN})
data = obj.json()['shop']
i = 0
while i < 3:
    try:
        display_name = data[i]['displayName']
        media_url = data[i]['displayAssets'][0]['url']

        response = requests.get(media_url, stream=True)

        with open(f"{display_name}.jpg", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    except Exception as e:
        print("An error occurred:", e)
    i += 1
