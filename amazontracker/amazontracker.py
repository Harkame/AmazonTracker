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

from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

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

DEFAULT_CREDENTIAL = "credential.json"

headers = {"User-Agent": "Mozilla/5.0"}


class AmazonTracker:
    def __init__(self):
        self.products = []

        self.config_file = DEFAULT_CONFIG_FILE

        self.mailed_products = []

        self.sleep = DEFAULT_SLEEP

        self.email_address = ""
        self.password = ""

        self.enable_notification = False
        self.enable_email = False
        self.credential = DEFAULT_CREDENTIAL

    def init(self, arguments):
        self.init_arguments(arguments)

        self.init_config()

        logger.debug("config_file : %s", self.config_file)
        logger.debug("sleep : %f", self.sleep)
        logger.debug("email : %s", self.email_address)
        logger.debug("password : %s", self.password)
        logger.debug("enable_notification : %s", self.enable_notification)
        logger.debug("credential : %s", self.credential)

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

        if arguments.email is not None and arguments.password is not None:
            self.email_address = arguments.email
            self.password = arguments.password
            self.enable_email = True
            print("inside")

        if self.sleep is not None:
            self.sleep = arguments.sleep

        if "notification" in arguments:
            self.enable_notification = True
            self.credential = arguments.notification
            cred = credentials.Certificate(self.credential)
            firebase_admin.initialize_app(cred)

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

        if "selector" in product:
            count = (
                product["selector"]["count"] if "count" in product["selector"] else 0
            )
            price_tag = page.select(product["selector"]["value"])[count]
        else:
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

                    if self.enable_email:
                        self.send_email(
                            product["code"], title=title, price=str(price), url=url
                        )

                    if self.enable_notification:
                        self.send_notification("amazon_tracker", title, str(price), url)
            else:
                logger.debug("produce %s available", product["co"])

                if self.enable_email:
                    self.send_email(product["code"], title=title, url=url)

                if self.enable_notification:
                    self.send_notification("amazon_tracker", title, body, url)

    def run(self):
        set_interval(self.check_prices, self.sleep, True)

    def send_email(self, code="", title="", price="", url=""):
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

    def send_notification(self, topic="", title="", body="", url=""):
        logger.debug("send_notification")

        topic = "amazon_tracker"

        # See documentation on defining a message payload.
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body,),
            data={"url": url},
            topic=topic,
        )

        response = messaging.send(message)

    def send_single(self):
        cred = credentials.Certificate("credential.json")
        firebase_admin.initialize_app(cred)

        registration_token = "exW-CX5H0us:APA91bFSAjAvvmF5RSLuO9qLXrFRrpBoDEjNG02zZpe__Rdu-gH1RvFQvR0lD2iz13bZpASKyuTHwxKDLlFNC63kopKxP_LiUr5BnJhWqV9U8a81oNiPsptCV1v_Rru3SmqCk-Ju2adw"

        # See documentation on defining a message payload.
        message = messaging.Message(
            data={"score": "850", "time": "2:45",}, token=registration_token,
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print("Successfully sent message:", response)


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
