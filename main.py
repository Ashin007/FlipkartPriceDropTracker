import pickle
import requests
import os

import datetime

from bs4 import BeautifulSoup as bS
import urllib.request

first_product_dict = \
    {
        "product_link": "https://www.flipkart.com/dr-morepen-glucoone-bg-03-50-glucometer-strips/p/itm091d9067dcc0e"
                        "?pid=GLTEFTX3TWGCHJWY&lid=LSTGLTEFTX3TWGCHJWYVDM9XO",
        "product_class_name": "_30jeq3 _16Jk6d"}
second_product_dict = {
    "product_link": "https://www.flipkart.com/dr-morepen-glucoone-bg-03-50-glucometer-strips/p/itm091d9067dcc0e?pid"
                    "=GLTEFTX3TWGCHJWY&lid=LSTGLTEFTX3TWGCHJWYIGDR3Y",
    "product_class_name": "_30jeq3 _16Jk6d"}


def get_price_from_flip_kart(link, class_name):
    page = urllib.request.urlopen(link)

    soup = bS(page, features="html.parser")
    value = soup.find('div', class_=class_name).string
    flip_kart_price = int(value[1::])
    return flip_kart_price


def put_least_price_to_file(data):
    price_file = open('least_price.txt', 'wb')
    pickle.dump(data, price_file)
    price_file.close()


def get_least_price_from_file():
    price_file = open('least_price.txt', 'rb')
    return pickle.load(price_file)


def price_log_file(price):
    date_and_time = str(datetime.datetime.now())
    price_file_log = open("price_log.txt", "a")
    price_file_log.write("Product price : " + str(price) + " Date: " + date_and_time[:19] + "\n")
    price_file_log.close()


def sms_alert(response):
    resp = requests.post('https://textbelt.com/text', {
        'phone': os.environ.get("ph_number"),
        'message': response,
        'key': 'textbelt',
    })
    print(resp.json())


put_least_price_to_file(1000)
# keep_alive()
while True:
    try:
        first_product_price = get_price_from_flip_kart(first_product_dict.get("product_link"),
                                                       first_product_dict.get("product_class_name"))
        print(first_product_price)

        second_product_price = get_price_from_flip_kart(second_product_dict.get("product_link"),
                                                        second_product_dict.get("product_class_name"))
        print(second_product_price)

        least_price = get_least_price_from_file()

        if first_product_price < second_product_price:
            if least_price != first_product_price:
                if least_price > first_product_price:
                    info = 'flipkart product price drop alert, Current price is: ' + str(
                        first_product_price) + " Link to the product is: " + first_product_dict.get("product_link")
                    print(info)
                    sms_alert(info)
                else:
                    info = 'flipkart product price higher alert, Current price is: ' + str(
                        first_product_price) + " Link to the product is: " + first_product_dict.get("product_link")
                    print(info)
                    sms_alert(info)

                least_price = first_product_price
                put_least_price_to_file(least_price)
                price_log_file(least_price)

        else:
            if least_price != second_product_price:
                if least_price > second_product_price:
                    info = 'flipkart product price drop alert, Current price is: ' + str(
                        second_product_price) + " Link to the product is: " + second_product_dict.get("product_link")
                    print(info)
                    sms_alert(info)
                else:
                    info = 'flipkart product price higher alert, Current price is: ' + str(
                        second_product_price) + " Link to the product is: " + second_product_dict.get("product_link")
                    print(info)
                    sms_alert(info)

                least_price = second_product_price
                put_least_price_to_file(least_price)
                price_log_file(least_price)
    except:
        print("Error occurred while fetching price from flipkart")
