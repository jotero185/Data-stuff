from lolpedia.items import player_data
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy import Request


class PlayerSpider(Spider):
    name = 'player'
    start_urls = ['https://lol.gamepedia.com/LEC/2021_Season/Spring_Season/Player_Statistics',
                  'https://lol.gamepedia.com/LCK/2021_Season/Spring_Season/Player_Statistics',
                  'https://lol.gamepedia.com/LCS/2021_Season/Spring_Season/Player_Statistics',
                  'https://lol.gamepedia.com/LPL/2021_Season/Spring_Season/Player_Statistics',
                 ]
    allowed_domains = ['lol.gamepedia.com']
    custom_settings = {
        'FEED_URI':"players.csv",
        'FEED_FORMAT':'csv',
        'FEED_EXPORT_FIELDS' : ['league', 'team', 'name_player', 'role', 'win', 'loses', 
                                'kill', 'death', 'assist', 'kda',
                                'cs', 'csm','TotalGold', 'gold_per_m',
                                'goldshare', 'killp', 'kshare']
    }
    
    def parse(self,response):
        roles = response.xpath('//*[@id="mw-content-text"]/div/div[2]/div[5]/table/tbody/tr[3]/th/table/tbody/tr/td')
        for rol in roles:
            href = rol.xpath('a/@href').get()
            pos = rol.xpath('a/text()').get()
            yield Request(url=href, dont_filter=True, callback=self.parse_brand, meta={'Role':pos})
                    
    def parse_brand(self, response):
        response.request.meta.get('redirect_urls')
        rol = response.meta.get('Role')
        sele = Selector(response)
        table = sele.xpath('//*[@id="mw-content-text"]/div[1]/div/table/tbody/tr')
        for row in table[3:]:
            item =  ItemLoader(player_data(),row)
            item.add_xpath('team','./td[1]/a/@title')
            item.add_xpath('name_player','./td[2]/a/text()')
            item.add_xpath('win','./td[4]/text()')
            item.add_xpath('loses','./td[5]/text()')
            item.add_xpath('kill','./td[7]/text()')
            item.add_xpath('death','./td[8]/text()')
            item.add_xpath('assist','./td[9]/text()')
            item.add_xpath('kda','./td[10]/text()')
            item.add_xpath('cs','./td[11]/text()')
            item.add_xpath('csm','./td[12]/text()')
            item.add_xpath('gold_per_m','./td[14]/text()')
            item.add_value('role',rol)

            league = sele.xpath('//*[@id="mw-content-text"]/div[1]/div/table/tbody/tr[1]/th/a/@title').extract_first().split("/")[0]
            gold = float(row.xpath('./td[13]/span/text()').extract_first())*1000
            killp = float(row.xpath('./td[15]/text()').extract_first().replace('%', ''))/100
            kshare = float(row.xpath('./td[16]/text()').extract_first().replace('%', ''))/100
            goldshare = float(row.xpath('./td[17]/text()').extract_first().replace('%', ''))/100  

            item.add_value('league', league)
            item.add_value('killp',str(killp))
            item.add_value('kshare',str(kshare))
            item.add_value('goldshare',str(goldshare))
            item.add_value('TotalGold',str(gold))
            yield item.load_item()            