import cron_job
import time
import logging
# this script should call the function add_details from cron_job.py and if it fails for some reason it retires again with exponential backoff up to 5 times before giving up and logging the error

if __name__ == "__main__":
    for i in range(5):
        print("Attempt: ", i)
        try:
            cron_job.add_details()
            break
        except Exception as e:
            logging.error("Error in cron job: " + str(e))
            time.sleep(4**i)
            continue
    else:
        logging.error("Failed to run cron job after 5 attempts")

