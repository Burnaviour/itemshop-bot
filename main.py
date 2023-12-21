import api_test
import fb_upload
import schedule
import time
def main():
    if result := api_test.generate_item_shop_image():
        fb_upload.main()

# Schedule the main function to run every day at 5 am Pakistani time
schedule.every().day.at("10:01").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
