import api_test
import fb_upload
import schedule
import time
import os
import logging
from Loading_Image import loading_bar_in_depth
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
def main2():
    try:
        if result := loading_bar_in_depth.display_loading_bar():
            fb_upload.main("final_loading_bar_img.png", "loading_bar",result[0])
    except Exception as e:
        logging.error("An error occurred: %s",e)
# Schedule the main function to run every day at 5 am Pakistani time
# schedule.every().day.at("05:03").do(main)
# schedule.every().day.at("10:00").do(main2)

# while True:
#     try:
#         schedule.run_pending()
#         time.sleep(1)
#     except KeyboardInterrupt:
#         break
#     except Exception as e:
#         logging.error("An error occurred: %s",e)
main2()
