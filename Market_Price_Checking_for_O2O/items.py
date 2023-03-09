# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MarketPriceCheckingForO2OItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name_Web_Site = scrapy.Field()
    Cate = scrapy.Field() #ได้จากชื่อชีทที่เตรียมข้อมูล
    Subcate = scrapy.Field()
    Item_Name = scrapy.Field()
    Unit = scrapy.Field() #ต่อชิ้นต่อแพ็ค
    Pack_Type = scrapy.Field()
    Normal_Price = scrapy.Field()
    Promotion_Price = scrapy.Field()
    Promotion_Type = scrapy.Field()
    Promotion_Period = scrapy.Field()
    Discount = scrapy.Field()
    Imag_Product_Url = scrapy.Field()
    Sold = scrapy.Field() #ขายแล้ว
    Inventory = scrapy.Field() #สินค้าคงเหลือ
    Date = scrapy.Field() #วันที่เก็บข้อมูล
    Img_Promotion_Url =  scrapy.Field()
    Remark = scrapy.Field()