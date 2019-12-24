# This program will check the price of a product on Amazon.de and send and email if a conditional is true.

import requests
from bs4 import BeautifulSoup
import logging
import os
import threading
import smtplib, ssl
import time
import unicodedata
import signal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if __package__ is None or __package__ == "":
    from helpers import get_arguments, get_config
else:
    from .helpers import get_arguments, get_config

DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
AMAZON_TLD = "fr"

AMAZON_BASE_PRODUCT_URL = f"https://www.amazon.{AMAZON_TLD}/dp/"
logger = logging.getLogger(__name__)

DEFAULT_PORT = 587
DEFAULT_SMTP_SERVER = "smtp.gmail.com"

DEFAULT_SLEEP = 3600
DEFAULT_PRODUCTS_SLEEP = 20

headers = {"User-Agent": "Mozilla/5.0"}


class AmazonTracker:
    def __init__(self):
        self.products = []

        self.config_file = DEFAULT_CONFIG_FILE

        self.mailed_products = []

        self.sleep = DEFAULT_SLEEP

        self.email_address = ""
        self.password = ""

    def init(self, arguments):
        self.init_arguments(arguments)

        self.init_config()

        logger.debug("config_file : %s", self.config_file)
        logger.debug("sleep : %f", self.sleep)
        logger.debug("email : %s", self.email_address)
        logger.debug("password : %s", self.password)

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

        if arguments.email is not None:
            self.email_address = arguments.email

        if arguments.password is not None:
            self.password = arguments.password

        if self.sleep is not None:
            self.sleep = arguments.sleep

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

        if "sleep" in config and config["sleep"] is not None:
            sleep = float(config["sleep"])

            if sleep != DEFAULT_SLEEP:
                self.sleep = sleep

    def check_prices(self):
        self.init_config()

        print("Check prices...")

        for product in self.products:
            print(f" - {product['code']}")

            if product["code"] not in self.mailed_products:
                self.check_price(product)

            time.sleep(DEFAULT_PRODUCTS_SLEEP)

    def check_price(self, product):
        logger.debug("product['code'] : %s", product["code"])

        url = f"{AMAZON_BASE_PRODUCT_URL}{product['code']}"

        logger.debug("url : %s", url)

        page = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

        title_tag = page.find(id="productTitle")

        title = title_tag.text.strip()

        price_tag = page.find(id="priceblock_ourprice")

        if price_tag is not None:
            price = price_tag.text.strip()

            converted_price = float(price[0 : price.rfind(" ") - 1].replace(",", "."))

            logger.debug("title : %s", title)
            logger.debug("converted_price : %f", converted_price)

            if "price" in product:
                logger.debug("checked price : %f", product["price"])
                if converted_price <= product["price"]:
                    logger.debug(
                        "price lower (%s) : %f -> %f",
                        product["code"],
                        product["price"],
                        converted_price,
                    )
                    self.send_mail(
                        product["code"], title=title, price=str(price), url=url
                    )
            else:
                logger.debug("produce %s available", product["co"])
                print("Product")
                self.send_mail(product["code"], title=title, url=url)

    def run(self):
        set_interval(self.check_prices, self.sleep, True)

    def send_mail(self, code="", title="", price="", url=""):
        port = 587
        smtp_server = "smtp.gmail.com"
        subject = format_string(self.email["subject"], title, price, url)
        body = format_string(self.email["body"], title, price, url)

        logger.debug("subject : %s", subject)
        logger.debug("body : %s", body)

        message = MIMEMultipart()
        message["From"] = self.email_address
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP(DEFAULT_SMTP_SERVER, DEFAULT_PORT) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.email_address, self.password)

            for destination in self.email["destinations"]:
                message["To"] = destination
                server.sendmail(
                    self.email_address, destination, strip_accents(message.as_string())
                )

            logger.debug("append %s to mailed_products", code)
            self.mailed_products.append(code)


def format_string(base_string="", title="", price="", url=""):
    return (
        base_string.replace("$title", title)
        .replace("$price", price)
        .replace("$url", url)
    )


def set_interval(callback, time, once=False):
    event = threading.Event()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if once:
        callback()  # call once

    while not event.wait(time):
        callback()


def strip_accents(text):

    try:
        text = unicode(text, "utf-8")
    except NameError:  # unicode is a default on python 3
        pass

    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")

    return str(text)


class TrackedProduct:
    def __init__(self):
        self.code = ""
        self.name = ""
        self.price = 0.0

    def __str__(self):
        pass
