import time
import requests
import re
from datetime import datetime
import json
import logging

logger = logging.getLogger("water reminder")
file_handler = logging.FileHandler('reminder.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
file_handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
"""
logging options:
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')
"""


def reminder():
    bot_token = "<bot token>"
    chat_id = "<user chat ID>"
    debug_id = "<admin chat ID>"
    message = "please drink water <3"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    logger.debug("Sending message")
    response = requests.get(url).json()
    formatted_string = json.dumps(response, indent=4)
    time_stamp = re.compile(r'"date": (\d+),')
    status = re.compile(r'"error_code": (\d+),')
    match_time = re.search(time_stamp, formatted_string)
    match_status = re.search(status, formatted_string)
    if match_status:
        print("error code: " + match_status.group(1))
        logger.error("Failed to send")
        logger.error("error code: " + match_status.group(1))
        message = f"Failed to send with error code: {match_status.group(1)}"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={debug_id}&text={message}"
        requests.get(url).json()
        logger.critical("Admin notified")
    if match_time:
        logger.info("Successfully sent")


logger.debug("Initializing reminder")
reminder()
start_time = time.time()

while True:
    current_time = datetime.now().time().hour
    if 9 <= current_time < 23:  # only sends notification between 9:00 - 23:00
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 3600:  # 60 minutes in seconds
            start_time = current_time
            reminder()
