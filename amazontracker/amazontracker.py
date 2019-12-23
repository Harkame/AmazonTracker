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
import time

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

DEFAULT_SLEEPING_TIME = 3600
DEFAULT_PRODUCTS_SLEEPING_TIME = 5

headers = {'User-Agent': 'Mozilla/5.0'}

class AmazonTracker:
    def __init__(self):
        self.products = []

        self.config_file = DEFAULT_CONFIG_FILE

        self.mailed_products = []

        self.sleeping_time = DEFAULT_SLEEPING_TIME

    def init(self, arguments):
        self.init_arguments(arguments)

        self.init_config()

        logger.debug("config_file : %s", self.config_file)
        logger.debug("sleeping_time : %f", self.sleeping_time)

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

        if arguments.identifiant  is not None:
            self.identifiant = arguments.identifiant

        if arguments.password  is not None:
            self.password = arguments.password

        if self.sleeping_time is not None:
            self.sleeping_time = arguments.sleeping_time

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

        if "sleeping_time" in config and config["sleeping_time"] is not None:
            sleeping_time = float(config["sleeping_time"])

            if sleeping_time != DEFAULT_SLEEPING_TIME:
                self.sleeping_time = sleeping_time

    def check_prices(self):
        self.init_config()

        for product in self.products:
            #time.sleep(DEFAULT_PRODUCTS_SLEEPING_TIME)
            if product["code"] not in self.mailed_products:
                self.check_price(product)

    def check_price(self, product):
        logger.debug("product['code'] : %s", product['code'])

        url = f"{AMAZON_BASE_PRODUCT_URL}{product['code']}"
        print(url)

        page = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

        title_tag = page.find(id="productTitle")

        title = title_tag.text.strip()

        price_tag = page.find(id="priceblock_ourprice")

        if price_tag is not None:
            price = price_tag.text.strip()

            converted_price = float(price[0:price.rfind(" ") - 1].replace(",", "."))

            logger.debug("title : %s", title)
            logger.debug("converted_price : %f", converted_price)

            if "price" in product:
                logger.debug("checked price : %f", product["price"])
                if converted_price <= product["price"]:
                    logger.debug("price lower (%s) : %f -> %f", product['code'], product["price"], converted_price)
                    self.send_mail(product["code"], title=title, price=price)
            else:
                logger.debug("produce %s available", product["co"])
                self.send_mail(product["code"], title=title)


    def run(self):
        set_interval(self.check_prices, self.sleeping_time)

    def send_mail(self, code=None, title=None, price=None):
        context = ssl.create_default_context()

        subject = format_string(self.email["subject"], title, price)
        body = format_string(self.email["body"], title, price)

        logger.debug("subject : %s", subject)
        logger.debug("body : %s", body)

        message = f"""\
        {subject}

        {body}"""

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
