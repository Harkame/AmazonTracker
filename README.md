# AmazonTracker

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

python amazontracker/main.py -e mymailaddress@gmail.com -p mypassword

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
    - louisr.daviaud@gmail.com

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

https://www.amazon.fr/Red-Dead-Redemption-2-PC/dp/B07ZWB2Q24/ref=sr_1_1?__mk_fr_FR=ÅMÅŽÕÑ&keywords=red+dead+redemption&qid=1577105770&sr=8-1

There is 4 type of tracking :

#### By price

``` yaml

products:
  - code: #check price
      B07T4Q53ZL
    price:
      151

```

Alert if the product « B07T4Q53ZL » price is below 151

#### Is available

``` yaml

products:
  - code: #check available
      B07T3NQBXV

```

Alert if the product « B07T3NQBXV » is available

#### Custom selector

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

Alert if the product « B07T3NQBXV » price is below 140

![Screenshot](https://github.com/Harkame/AmazonTracker/blob/master/amazon_selector.JPG "Amazon multiple product")

selector :

In this case « .swatchElement span span span span span » select price from Blu-ray and DVD
count represent the element to select, in this case 1 = Blu-ray and 2 = DVD

#### Is discounted

``` yaml
products:
  - code: #check if discounted
      B07T4Q53ZL
    discounted:
      true

```

####

### Alert

There is 2 type of alert

#### EMail

To enable e-mail notification you need to run amazontracker with parameter email and password

```

python amazontracker/main.py -e myemailaddress@gmail.com -p mypassword

```

You specify an gmail account, you must enable access https://support.google.com/a/answer/6260879


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



#### Push notification

You must create an application linked with your own firebase account

[There is an example app](https://github.com/Harkame/AmazonTrackerApp)

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

``` bash

python amazontracker/main.py -n credential.json

topic :

Topic to send message

registration_token :

List of token generated by your app

title, subject :

Those can be customised, keyword $title, $price and $url gonna be replaced by product's title, product's price and product's url

```

https://github.com/Harkame/AmazonTrackerApp

topic :

registration_token :

title :

body :
