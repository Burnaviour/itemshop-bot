import api_test
import fb_upload
import schedule
import time
import os
import logging
# Configure logger
logging.basicConfig(filename='api_test.log',
                        format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def main():
    try:
        if result := api_test.generate_item_shop_image():
            os.remove("final_image1.png") 
            fb_upload.main("final_image.png", "itemshop")
    except Exception as e:
        logging.error("An error occurred: %s",e)

# Schedule the main function to run every day at 5 am Pakistani time
schedule.every().day.at("10:04").do(main)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        break
    except Exception as e:
        logging.error("An error occurred: %s",e)
# main()