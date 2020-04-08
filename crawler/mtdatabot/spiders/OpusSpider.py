#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 4/7/20

import scrapy

from mtdatabot.items import MTDataItem, MTCorpusItem

class OpusSpider(scrapy.Spider):
    name = 'opus'
    start_urls = ['http://opus.nlpl.eu/']


    def parse(self, response):
        dataset_pages = response.xpath('(//td[2])[1]//a/@href').getall()
        for url in dataset_pages:
            yield response.follow(url, callback=self.parse_dataset_listing)

    def parse_dataset_listing(self, response):
        self.logger.info(f"Parsing dataset listing : {response.url}")
        suffix = '.txt.zip'
        if response.url.endswith('JW300.php'):  # this one doesnt have moses txt
            suffix = '.xml.gz'

        # URL of form "<prefix>?download?f=dataset/version/moses/src-tgt.zip"
        if getattr(self, 'flat', None):
            # flat all datasets into individual items
            anchors = response.xpath(f"//a[contains(@href, '{suffix}')]")
            self.logger.info(f"Found {len(anchors)} pairs")
            for anch in anchors:
                url = response.urljoin(anch.xpath('./@href').get())
                file_path = url.split('?f=')[-1]
                parts = [p for p in file_path.split('/') if p != 'moses']
                name = '_'.join(parts[:-1]).replace('-', '_')
                lang_pair = parts[-1].replace(suffix, '').split('-')
                if len(lang_pair) != 2:
                    self.logger.warning(f"Couldnt parse {url} properly; skipped")
                    continue

                item = MTDataItem()
                item['url'] = url
                item['name'] = name
                item['id'] = file_path
                item['langs'] = lang_pair
                item['title'] = anch.xpath('./@title').get().strip().replace(' - Moses format', '')
                item['info'] = anch.xpath('./text()').get().strip()
                yield item
        else: # Just one entry -- takes less space on disk
            urls = response.xpath(f"//a[contains(@href, '{suffix}')]/@href").getall()
            # extract corpus info from first URL, and generalize URL pattern
            if not urls:
                self.logger.warning(f"Found 0 URLS in {response.url}")
            else:
                self.logger.info(f"Found {len(urls)} pairs")
                url = urls[0]
                full_url = response.urljoin('/'.join(url.split('/')[:-1]) + f'/%s-%s{suffix}')
                corp_name = '_'.join(url.split('?f=')[-1].split('/')[:-2]).replace('-', '_')
                langs = []
                for url in urls:
                    lang_pair = url.split('/')[-1].replace(suffix, '').split('-')
                    if len(lang_pair) != 2:
                        self.logger.warning(f"Could not parse {url} properly; skipped")
                        continue
                    langs.append(lang_pair)

                item = MTCorpusItem()
                item['url'] = full_url
                item['name'] = corp_name
                item['langs'] = langs
                yield item