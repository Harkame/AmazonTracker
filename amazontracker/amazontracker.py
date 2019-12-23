# This program will check the price of a product on Amazon.de and send and email if a conditional is true.

import requests
from bs4 import BeautifulSoup
import smtplib
import time
import logging
import os
import threading
import re
import smtplib, ssl

if __package__ is None or __package__ == "":
    from helpers import get_arguments, get_config
else:
    from .helpers import get_arguments, get_config

DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
AMAZON_TLD = "fr"

AMAZON_BASE_PRODUCT_URL = f"https://www.amazon.{AMAZON_TLD}/dp/"
logger = logging.getLogger(__name__)

PORT = 587
SMTP_SERVER = "smtp.gmail.com"

headers = {'User-Agent': 'Mozilla/5.0'}

class AmazonTracker:
    def __init__(self):
        self.products = []

        self.config_file = DEFAULT_CONFIG_FILE

        self.mailed_products = []

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

        if "products" in config and config["products"] is not None:
            self.products = config["products"]
        else:
            self.products = []

        if "email" in config and config["email"] is not None:
            self.email = config["email"]
        else:
            self.email = {}

    def check_prices(self):
        self.init_config()

        for product in self.products:
            if product["code"] not in self.mailed_products:
                self.check_price(product)

    def check_price(self, product):
        print(product["code"])
        url = f"{AMAZON_BASE_PRODUCT_URL}{product['code']}"
        print(url)

        page = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

        print(page)

        title_tag = page.find(id="productTitle")

        title = title_tag.text.strip()

        price_tag = page.find(id="priceblock_ourprice")

        if price_tag is not None:
            price = price_tag.text.strip()

            converted_price = float(price[0:price.rfind(" ") - 1].replace(",", "."))

            print(title)
            print(price)
            print(converted_price)

            if "price" in product:
                print(f"converted_price : {converted_price}/ product['price'] : {product['price']}")
                if converted_price <= product["price"]:
                    self.send_mail(product["code"], title=title, price=price)
            else: #product is available
                self.send_mail(product["code"], title=title)


    def run(self):

        self.send_mail("frfrefre", "cyberpunk", str(43.5))

        return
        set_interval(self.check_prices, 10)

    def send_mail(self, code=None, title=None, price=None):
        context = ssl.create_default_context()

        message = f"""\
        {format_string(self.email["subject"], title, price)}

        {format_string(self.email["body"], title, price)}"""

        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.identifiant, self.password)

            for destination in self.email["destinations"]:
                server.sendmail(self.identifiant, destination, message)

            if code is not None:
                self.mailed_products.append(code)

def format_string(base_string="", title="", price="", url=""):
    return base_string.replace("$title", title).replace("$price", price).replace("$url", url)


def set_interval(callback, time):
    event = threading.Event()
    while not event.wait(time):
        callback()


class TrackedProduct:
    def __init__(self):
        self.code = ""
        self.name = ""
        self.price = 0.0

    def __str__(self):
        pass
