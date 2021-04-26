# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy.item import Field

class champ_data(Item):
    champ_name = Field()
    games = Field()
    win = Field()
    loses = Field()
    kill = Field()
    death = Field()
    assist = Field()
    role = Field()
    cs = Field()
    csm = Field()
    TotalGold = Field()
    gold_per_m = Field()
    killp = Field()
    kshare = Field()
    goldshare = Field()

class player_data(Item):
    team = Field()
    name_player = Field()
    games = Field()
    win = Field()
    loses = Field()
    kill = Field()
    death = Field()
    assist = Field()
    kda = Field()
    role = Field()
    cs = Field()
    csm = Field()
    TotalGold = Field()
    gold_per_m = Field()
    killp = Field()
    kshare = Field()
    goldshare = Field()
    league = Field()