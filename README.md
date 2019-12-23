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

## Usage

### Run

``` python

python amazontracker/main.py -e mymailaddress@gmail.com -p mypassword

```



### Search torrents

Return url's results torrent for specified search

``` python

torrents_url = scraper.search({name : "walking dead s08"})

"""

https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227730-the+walking+dead+s08+complete+vostfr+proper+720p+hdtv+x264-expm5
https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227752-the+walking+dead+s08+complete+vostfr+proper+hdtv+xvid-expm5
https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227763-the+walking+dead+s08+vostfr+web-dl+x264-ark01
https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227764-the+walking+dead+s08+vostfr+720p+amzn+web-dl+dd5+1+h264-ark01
https://www2.yggtorrent.ch/torrent/filmvid▒o/s▒rie-tv/227765-the+walking+dead+s08+vostfr+1080p+amzn+web-dl+ddp5+1+h264-ark01

...

"""

```

### How it work

This program use an config file (default : ./config.yml)

This file contains list of mangas to download, destination path, etc.

#### Example of config file

``` yaml
products:
  - code:
      B07R4NHLD7

  - code:
      B07T4Q53ZL
    price:
      130

email:
  destinations:
    - destination@gmail.com
    - anotherdestination@hotmail.com

  subject:
    "AmazonTracker : $title"

  body:
    $title - $price - $url

sleep:
  10
```


### Track an product

Add an entry in products

You can find the code in product page url

https://www.amazon.fr/Red-Dead-Redemption-2-PC/dp/B07ZWB2Q24/ref=sr_1_1?__mk_fr_FR=ÅMÅŽÕÑ&keywords=red+dead+redemption&qid=1577105770&sr=8-1

you can also add an attribut price, you will notified when the product was available under this price


## TODO

-   More tests, find non bugged search (especially for sort tests)

## Test

Declare environment variables (requiered for login, download tests)

-   YGGTORRENT_IDENTIFIANT
-   YGGTORRENT_PASSWORD

``` bash

pip install tox

tox

```
