from lolpedia.items import champ_data
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
import scrapy

# //*[@id="mw-content-text"]/div/div[2]/div[5]/table/thead/tr[3]/th/table/tbody/tr/td[1]/a


class ChampSpider(Spider):
    name = 'champ'
    start_urls = ['https://lol.gamepedia.com/LEC/2021_Season/Spring_Season/Champion_Statistics']
    allowed_domains = ['lol.gamepedia.com']
    custom_settings = {
        'FEED_URI':"champ.csv",
        'FEED_FORMAT':'csv',
        'FEED_EXPORT_FIELDS' : ['champ_name', 'role', 'games', 'win', 'loses', 
                                'kill', 'death', 'assist', 'cs', 'csm','TotalGold', 'gold_per_m',
                                'goldshare', 'killp', 'kshare']
    }
    
    def parse(self,response):
        roles = response.xpath('//*[@id="mw-content-text"]/div/div[2]/div[5]/table/tbody/tr[3]/th/table/tbody/tr/td')
        for rol in roles:
            href = rol.xpath('a/@href').get()
            pos = rol.xpath('a/text()').get()
            yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_brand, meta={'Role':pos})
                    
    def parse_brand(self, response):
        response.request.meta.get('redirect_urls')
        rol = response.meta.get('Role')
        sele = Selector(response)
        table = sele.xpath('//div[@id="mw-content-text"]/div[1]/div/table/tbody/tr')
        a = response.xpath('//*[@id="mw-content-text"]/div/div[2]/div[5]/table/tbody').extract()
        for row in table:
            if row.xpath("./td[1]/span/span[2]/text()").extract_first() != None:
                item =  ItemLoader(champ_data(),row)
                item.add_xpath('champ_name','./td[1]/span/span[2]/text()')
                item.add_xpath('games','./td[2]/a/text()')
                item.add_xpath('win','./td[4]/text()')
                item.add_xpath('loses','./td[5]/text()')
                item.add_xpath('kill','./td[7]/text()')
                item.add_xpath('death','./td[8]/text()')
                item.add_xpath('assist','./td[9]/text()')
                item.add_xpath('cs','./td[11]/text()')
                item.add_xpath('csm','./td[12]/text()')
                item.add_xpath('gold_per_m','./td[14]/text()')
                item.add_value('role',rol)
                
                gold = float(row.xpath('./td[13]/span/text()').extract_first())*1000
                killp = float(row.xpath('./td[15]/text()').extract_first().replace('%', ''))/100
                kshare = float(row.xpath('./td[16]/text()').extract_first().replace('%', ''))/100
                goldshare = float(row.xpath('./td[17]/text()').extract_first().replace('%', ''))/100  
                
                item.add_value('killp',str(killp))
                item.add_value('kshare',str(kshare))
                item.add_value('goldshare',str(goldshare))
                item.add_value('TotalGold',str(gold))
                yield item.load_item()            