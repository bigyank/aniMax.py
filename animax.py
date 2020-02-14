# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerProcess
import os
import json
import logging


import itertools
import threading
import time
import sys


class AnimaxSpider(Spider):
    name = 'animax'
    search = ""

    def parse(self, response):
        return [
            FormRequest(
                url=response.url,
                formdata={"s": self.search},  # s is the name of the searchfeild
                callback=self.after_search,
            )
        ]

    def after_search(self, response):
        anime = response.xpath('//div[@class="condd"]')
        for singleAnime in anime:
            yield {
                singleAnime.xpath(".//a/text()").get(): singleAnime.xpath(".//a/@href").get()
            }


def first_process(searchAnime):
    AnimaxSpider.search = searchAnime

    process = CrawlerProcess(
        {"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1,)",
         'FEED_FORMAT': 'json',
         'FEED_URI': 'temp/main.json'}
    )

    # first process
    process.crawl(AnimaxSpider, start_urls=["https://animefrenzy.net"])
    process.start()


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rSearching for anime ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\n')


logging.getLogger('scrapy').propagate = False


print(r'''
  _           _
  /_\   _ __  (_)  /\/\    __ _ __  __
 //_\\ | '_ \ | | /    \  / _` |\ \/ /
/  _  \| | | || |/ /\/\ \| (_| | >  <
\_/ \_/|_| |_||_|\/    \/ \__,_|/_/\_\

                                      ''')


done = False

t = threading.Thread(target=animate)
searchAnime = input("Please enter anime name\n")
t.start()
first_process(searchAnime)
time.sleep(1)
os.system('cls||clear')
# long process here
done = True


# second_process()
