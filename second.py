from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerProcess
import os
import json
from subprocess import call
import logging


class AnimaxSpiderEp(Spider):
    name = 'animaxEp'

    def parse(self, response):
        ep_collection = response.xpath('//div[@class="infoepbox"]')
        ep_link_collection = ep_collection.xpath('.//a/@href').getall()
        for single_link in ep_link_collection:
            yield{
                'anime_ep_link': single_link
            }


def second_process(anime_url):
    process = CrawlerProcess(
        {"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1,)",
         'FEED_FORMAT': 'json',
         'FEED_URI': 'temp/episodes.json'}
    )
    process.crawl(AnimaxSpiderEp, start_urls=[anime_url])
    process.start()


def choose_anime():
    with open('temp/main.json', 'r') as json_file:
        anime_list = json.load(json_file)

    for anime in anime_list:
        for key in anime.keys():
            print(anime_list.index(anime), key)  # keys contains name of the anime

    select_anime = int(input("Please select a index\n"))

    for value in anime_list[select_anime].values():
        choosen_anime = value
    return choosen_anime


def clean_up():
    tempFile = "temp/main.json"
    if os.path.isfile(tempFile):
        os.remove(tempFile)
    else:  # Show an error ##
        print("Error: %s file not found" % tempFile)


# process starts here
# calling here beacuse reactor can not be restarted
logging.getLogger('scrapy').propagate = False
anime_name = choose_anime()
second_process(anime_name)
clean_up()
