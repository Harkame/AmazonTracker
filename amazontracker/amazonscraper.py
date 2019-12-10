# This program will check the price of a product on Amazon.de and send and email if a conditional is true.

import requests
from bs4 import BeautifulSoup
import smtplib
import time


# Product link
URL = "https://www.amazon.de/Samsung-C24F396FHU-Curved-Monitor-schwarz/dp/B01DMDKZTC/ref=sr_1_3?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=monitor&qid=1565082683&s=gateway&sr=8-3"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
}

# Function that will get the information from the URL - in this case we will get:
# productTitle and priceblock_ourprice (product price)
def check_price():
    page = requests.get(URL, headers=headers)
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


# Calling the function
check_price()


# It is also possible to add a loop to check the price from time to time
# while (True):
#    check_price()
#    time.sleep(45)


class TrackedProduct:
    def __init__(self):
        self.code = ""
        self.name = ""
        self.price = 0.0

    def __str__(self):
        pass
