#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 4/7/20

import scrapy

from mtdatabot.items import MTDataItem, MTCorpusItem

class OpusSpider(scrapy.Spider):
    name = 'tilde'
    start_urls = ['https://tilde-model.s3-eu-west-1.amazonaws.com/Tilde_MODEL_Corpus.html']

    def parse(self, response):
        suffix = '.tmx.zip'
        anchors = response.xpath(f"//a[contains(@href, '{suffix}')]")
        self.logger.info(f"Found {len(anchors)} pairs")
        for anch in anchors:
            url = response.urljoin(anch.xpath('./@href').get())
            file_path = url.split('/')[-1]
            parts = file_path.replace(suffix, '').split('.')
            lang_pair = parts[-1].split('-')
            name = parts[0]
            if len(parts) != 2 or len(lang_pair) != 2:
                self.logger.warning(f"Couldnt parse {url} properly; skipped")
                continue

            item = MTDataItem()
            item['url'] = url
            item['name'] = name
            item['id'] = file_path
            item['langs'] = lang_pair
            item['title'] = anch.xpath('./@title').get().strip().replace(', TMX format', '')
            item['info'] = anch.xpath('./text()').get().strip()
            yield item