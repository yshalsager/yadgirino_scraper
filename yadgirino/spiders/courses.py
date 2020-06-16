# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request


class CoursesSpider(Spider):
    name = 'courses'
    allowed_domains = ['yadgirino.com']

    def __init__(self, url, proxy):
        self.base_url = 'https://yadgirino.com'
        self.url = url
        self.start_urls = [url]
        self.proxy = proxy
        self.info = {}
        self.downloads = set()

    def parse(self, response):
        title = response.css('.lead > a::text')
        title = title.get() if title else response.xpath('//*[@id="pageheadertitle"]/text()').get()
        self.info.update({
            'course': title,
            'author': response.xpath('//*[@class="card-title m-0"]/text()').get()
        })
        nav = response.xpath('//*[@id="course-toc"]/li')
        modules = []
        for section in nav:
            section_title = section.xpath('a/span[@class="flex"]/text()').get()
            items_selector = section.xpath('div/ul/li')
            items = {}
            for item in items_selector:
                item_title = item.xpath('a/text()').get()
                item_url = f"{self.base_url}{item.xpath('a/@href').get()}"
                items.update({item_title: item_url})

                yield Request(
                    url=item_url,
                    callback=self.get_course_content,
                    meta={"proxy": self.proxy}
                )
            modules.append({'title': section_title, 'items': items})
        self.info.update({'modules': modules})

    def get_course_content(self, response):
        self.downloads.add(response.xpath('//source[@type="video/mp4"]/@src').get())
        self.downloads.add('https://host-video.com' + response.xpath('//track[@kind="captions"]/@src').get())
        exercise_file = response.xpath('//a[contains(@href, "zip")]/@href')
        if exercise_file:
            self.downloads.add(exercise_file.get())

    def close(self):
        course = self.info.get('course')
        course = course if course else 'course'
        with open(f'{course}_info.json', 'w') as json_file:
            json.dump(self.info, json_file, indent=4, ensure_ascii=False)

        with open(f'{course}_links.json', 'w') as out:
            json.dump(sorted(list(self.downloads)), out, indent=4, ensure_ascii=False)
