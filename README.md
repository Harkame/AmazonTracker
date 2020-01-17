# AmazonTracker

AmazonTracker is a script that track amazon product and notify you if the price is below an specified price, if the product is available or discounting

You can be notified by Email :email: or with firebase push notification :iphone:

## README AND SCRIPT IN PROGRESS

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fb0ce7eed7e04839b8023b520f6d6c13)](https://www.codacy.com/manual/Harkame/AmazonTracker?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Harkame/AmazonTracker&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/c8c73facbfdde6a7d943/maintainability)](https://codeclimate.com/github/Harkame/AmazonTracker/maintainability)
[![Build Status](https://travis-ci.org/Harkame/AmazonTracker.svg?branch=master)](https://travis-ci.org/Harkame/AmazonTracker)

## Installation

clone this repository and

``` bash

git clone https://github.com/Harkame/AmazonTracker.git

cd AmazonTracker

pip install -r requirements.txt

```

### Dependencies

-   [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [lxml](https://github.com/lxml/lxml.git)
-   [requests](https://github.com/psf/requests.git)
-   [firebase-admin-python](https://github.com/firebase/firebase-admin-python)

## Usage

### Run

``` python

python amazontracker/main.py

```

### Options

``` bash

usage: main.py [-h] [-c CONFIG_FILE] [-e EMAIL] [-p PASSWORD] [-n NOTIFICATION] [-v]

Script to track product on Amazon

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Set config file
                        Example : python japscandownloader/main.py -c /home/myconfigfile.yml
  -e EMAIL, --email EMAIL
                        Gmail address
                        Required with password option to send email
                        Example : python amazontracker/main.py -l mymailadress@gmail.com
  -p PASSWORD, --password PASSWORD
                        Gmail password
                        Required with email option to send email
                        Example : python amazontracker/main.py -p mypassword
  -n NOTIFICATION, --notification NOTIFICATION
                        SDK Admin Firebase private key
                        Example : python amazontracker/main.py -n /path/to/myprivatekey.json
  -v, --verbose         Active verbose mode, support different level
                        Example : python japscandownloader/main.py -v
```

### How it works

This program use an config file (default : ./config.yml)

This file contains list of products to track, alert settings, etc.

#### Example of config file

``` yaml

products:
  - code: #check price
      B07T4Q53ZL
    price:
      151

  - code: #check if discouned
      B07T4Q53ZL
    discounted:
      true

  - code: #check price with specific selector
      B07T3NQBXV
    price:
      140
    selector:
        value:
          .swatchElement span span span span span
        count:
          1

  - code: #check available
      B07T3NQBXV

email:
  destinations:
    - myemailaddress@gmail.com
    - myanotheremailaddress@hotmail.com

  subject:
    "AmazonTracker : $title"

  body:
    "<html>
    <a href='$url'><H3>$title</H3></a>
    <H3>$price</H3>
    </html>"

notification:
  topic:
    amazon_tracker

  registration_token:
    - device1
    - device2

  title:
    "AmazonTracker"

  body:
    "$price"

sleep:
  10
```

### Track an product

Add an entry in products

You can find the code in product page url

<https://www.amazon.fr/Red-Dead-Redemption-2-PC/dp/B07ZWB2Q24/ref=sr_1_1?__mk_fr_FR=ÅMÅŽÕÑ&keywords=red+dead+redemption&qid=1577105770&sr=8-1>

Here the product code is « B07ZWB2Q24 »

#### Tracking by price

``` yaml

products:
  - code: #check price
      B07T4Q53ZL
    price:
      151

```

Alert if the product « B07T4Q53ZL » price is below 151

#### Tracking by availability

``` yaml

products:
  - code: #check available
      B07T3NQBXV

```

Alert if the product « B07T3NQBXV » is available

#### Tracking by price with custom selector

Some product like movie have multiple price for Blu-ray or DVD for example

![Screenshot](https://github.com/Harkame/AmazonTracker/blob/master/amazon_selector.JPG "Amazon multiple product")

In this case, you can specify attribut « selector »

Value « .swatchElement span span span span span » select price from Blu-ray and DVD

Count represent the element to select, in this case 1 = Blu-ray and 2 = DVD


``` yaml

products:
  - code: #check price with specific selector
      B07T3NQBXV
    price:
      140
    selector:
        value:
          .swatchElement span span span span span
        count:
          1

```

Alert if the product « B07T3NQBXV » Blu-ray price is below 140

#### Tracking by discount

``` yaml

products:
  - code: #check if discounted
      B07T4Q53ZL
    discounted:
      true

```

Alert if the product « B07T4Q53ZL » is discounted

### Alert

There is 2 type of alert

#### Email :email:

To enable e-mail notification you need to run amazontracker with parameter email and password

``` bash

python amazontracker/main.py -e myemailaddress@gmail.com -p mypassword

```

You must specify an gmail account, with less secure apps enabled ([Documentation](https://support.google.com/a/answer/6260879))

##### Email config

``` yaml

email:
  destinations:
    - myemailaddress@gmail.com
    - myanotheremail@hotmail.com

  subject:
    "AmazonTracker : $title"

  body:
    "<html>
    <a href='$url'><H3>$title</H3></a>
    <H3>$price</H3>
    </html>"

```

destinations : List to Email address to send email
subject : Email subject
body : Email bodt

#### Push notification :iphone:

You must create an application linked with your own firebase account

[There is my example app](https://github.com/Harkame/AmazonTrackerApp)

[FCM Tuto](https://www.youtube.com/watch?v=QXPgMUSfYFI)

``` yaml

notification:
  topic:
    amazon_tracker

  registration_token:
    - device1
    - device2

  title:
    "AmazonTracker"

  body:
    "$price"

```

To enable firebase push notification you need to run amazontracker with notification, this is your SDK Admin private key [Documentation](https://firebase.google.com/docs/admin/setup)

``` bash

python amazontracker/main.py -n credential.json

```

topic :

Notify all devices that subscribes this topic

registration_token :

Notify all devices represented by those tokens

title and body

The title and the body of the notifications.
These are customisable

For Email (subject, body) and notification (title, body), this program recognised keyword and replace it

-   $price : Product price
-   $title : Product title
-   $url   : Product url

## TODO

-   Unit tests
-   Travis
