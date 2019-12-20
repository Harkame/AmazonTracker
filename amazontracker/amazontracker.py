# This program will check the price of a product on Amazon.de and send and email if a conditional is true.

import requests
from bs4 import BeautifulSoup
import smtplib
import time
import logging
import os

if __package__ is None or __package__ == "":
    from helpers import get_arguments, get_config
else:
    from .helpers import get_arguments, get_config

DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
AMAZON_TLD = "fr"

AMAZON_BASE_PRODUCT_URL = f"https://www.amazon.{AMAZON_TLD}/dp/"
logger = logging.getLogger(__name__)

# Product link
URL = "https://www.amazon.de/Samsung-C24F396FHU-Curved-Monitor-schwarz/dp/B01DMDKZTC/ref=sr_1_3?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=monitor&qid=1565082683&s=gateway&sr=8-3"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
}

# Function that will get the information from the URL - in this case we will get:
# productTitle and priceblock_ourprice (product price)
def check_price(product):
    page = requests.get(f"{AMAZON_BASE_PRODUCT_URL}product", headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[0:3])

    if converted_price < 100:
        send_mail()

    print(title.strip())
    print(converted_price, "€")

    if converted_price <= 100:
        send_mail()


# Function that will send an email if the price is 'true'
def send_mail(mail_address, password, subject, bod, destinations):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("", "")

    subject = "Price fell down!"
    body = "Check the Amazon link  https://www.amazon.de/Samsung-C24F396FHU-Curved-Monitor-schwarz/dp/B01DMDKZTC/ref=sr_1_3?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=monitor&qid=1565082683&s=gateway&sr=8-3"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail("thomcord@gmail.com", "thomcord@me.com", msg)

    print("Email has been sent")

    server.quit()


# It is also possible to add a loop to check the price from time to time
# while (True):
#    check_price()
#    time.sleep(45)


class AmazonTracker:
    def __init__(self):
        self.products = []

        self.config_file = DEFAULT_CONFIG_FILE

    def init(self, arguments):
        self.init_arguments(arguments)

        self.init_config()

        logger.debug("config_file : %s", self.config_file)

    def init_arguments(self, arguments):
        arguments = get_arguments(arguments)

        if arguments.verbose:
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s :: %(levelname)s :: %(module)s :: %(lineno)s :: %(funcName)s :: %(message)s"
            )
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            if arguments.verbose == 0:
                logger.setLevel(logging.NOTSET)
            elif arguments.verbose == 1:
                logger.setLevel(logging.DEBUG)
            elif arguments.verbose == 2:
                logger.setLevel(logging.INFO)
            elif arguments.verbose == 3:
                logger.setLevel(logging.WARNING)
            elif arguments.verbose == 4:
                logger.setLevel(logging.ERROR)
            elif arguments.verbose == 5:
                logger.setLevel(logging.CRITICAL)

            logger.addHandler(stream_handler)

        if arguments.identifiant:
            self.identifiant = arguments.identifiant

        if arguments.password:
            self.password = arguments.password

    def init_config(self):
        config = get_config(self.config_file)

        if "products" in config:
            self.products.extend(config["products"])

    def check_price(self):
        for product in selfs.product:
            # TODO
            pass


class TrackedProduct:
    def __init__(self):
        self.code = ""
        self.name = ""
        self.price = 0.0

    def __str__(self):
        pass
