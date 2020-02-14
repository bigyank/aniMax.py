from scrapy import Spider
from scrapy.crawler import CrawlerProcess
import json
import logging


class AnimaxSpiderEpVid(Spider):
    name = 'animaxEpVid'

    def parse(self, response):
        yield {
            "ep": response.xpath('//a[@class="an"]/@href')[1].get()
        }


def third_process(ep_href):
    process = CrawlerProcess(
        {"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1,)",
         'FEED_FORMAT': 'json',
         'FEED_URI': 'temp/episodes_video.json'}
    )
    process.crawl(AnimaxSpiderEpVid, start_urls=[ep_href])
    process.start()


def choose_ep():
    with open('temp/episodes.json', 'r') as json_file:
        episodes_list = json.load(json_file)

    episodes_list.reverse()
    print(len(episodes_list))
    ask_episode = int(input("Please enter ep n0."))

    for value in episodes_list[ask_episode - 1].values():
        choosen_ep = value
    return choosen_ep


logging.getLogger('scrapy').propagate = False
choosen_ep = choose_ep()
third_process(choosen_ep)
