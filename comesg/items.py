# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ComesgItem(Item):
    # define the fields for your item here like:
    name = Field()
    address = Field()
    contact = Field()
    hours = Field()
    website = Field()
    photo = Field()
    desc = Field()
    video = Field()
