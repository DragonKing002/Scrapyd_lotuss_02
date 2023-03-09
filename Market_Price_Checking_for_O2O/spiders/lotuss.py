
import sys
import os
import pandas as pd
import scrapy
import json
import time
from scrapy import signals
from Market_Price_Checking_for_O2O.other import Outlook,Sharepoint,Secrect
from Market_Price_Checking_for_O2O.items import MarketPriceCheckingForO2OItem

from datetime import date, datetime
#scrapy crawl lotuss
        
class LotussSpider(scrapy.Spider):
    name = 'lotuss'
    filename = "data\lotuss\%(name)s_{}.csv".format(date.today())
    #filename = "data\lotuss\%(name).csv"
    custom_settings = {
        'FEEDS': { filename : { 'format': 'csv','overwrite':False}},
        'FEED_EXPORT_ENCODING':'utf-8',
        'ITEM_PIPELINES':{
                            'Market_Price_Checking_for_O2O.pipelines.LotussPipeline': 300,
                        },  
                        }
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):

        spider = super(LotussSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self, spider):

        sharepoint_url = "https://cpallgroup.sharepoint.com/sites/MST-MarketPriceCheckingforO2O"
        config =  Secrect().get_secret()
        username = config['username']
        password = config['password']

        s = Sharepoint(username, password, sharepoint_url)
        s.download_sharepoint('Email-Config','Email-Cofig.xlsx')
        s.download_sharepoint('Master Files','Order_files.xlsx')

        dir_path = 'config_mer_lotuss_checking_o2o'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Remove all files
        folder_path = './config_mer_lotuss_checking_o2o'
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
    
        src = 'Email-Cofig.xlsx'
        dst = './config_mer_lotuss_checking_o2o/' + src
        os.rename(src, dst)

        src = 'Order_files.xlsx'
        dst = './config_mer_lotuss_checking_o2o/' + src
        os.rename(src, dst)

    def spider_closed(self, spider):

        name = 'lotuss'
        filename = "data\lotuss\lotuss_{}.csv".format(date.today())

        df = pd.read_csv(filename, encoding='utf-8')
        df.to_excel("data\\lotuss\\lotuss_{}.xlsx".format(date.today()), index = False, 
                    columns=['Date', 'Name_Web_Site', 'Cate', 'Subcate', 'Item_Name', 
                             'Unit', 'Pack_Type', 'Normal_Price',
                             'Promotion_Price', 'Promotion_Type',
                             'Promotion_Period', 'Discount', 'Remark',
                             'Sold', 'Inventory', 'Imag_Product_Url',
                             'Img_Promotion_Url'])

        os.remove(filename)

        try: #ลบไฟล์กันเหนียว
            os.remove('lotuss_{}.xlsx'.format(date.today()))
        except:
            pass
        src = "data\lotuss\lotuss_{}.xlsx".format(date.today())
        dst = 'lotuss_{}.xlsx'.format(date.today())
        os.rename(src, dst)
        
        sharepoint_url = "https://cpallgroup.sharepoint.com/sites/MST-MarketPriceCheckingforO2O"
        config =  Secrect().get_secret()
        username = config['username']
        password = config['password']

        mails_to = pd.read_excel('./config_mer_lotuss_checking_o2o/Email-Cofig.xlsx', index_col=False)['To']
        mails_to = ','.join(mails_to.dropna().tolist())
        mail_subject = 'รายงานการดึงข้อมูลจากเว็บโลตัสสำหรับงาน O2O'
        mail_body = '''

สำหรับข้อมูลด้านในจะเป็นการดึงข้อมูล Products จากเว็บโลตัสตาม Order ที่ลูกค้าได้กำหนดไว้ให้
จึงเรียนมาเพื่อทราบ

                    
                    '''
        # แจ้งเตือนทางเมลล์
        o = Outlook(username,password)
        o.send_mail(filename=dst,mail_from=username,\
                    mail_to=mails_to,mail_subject=mail_subject,mail_body=mail_body)

        # Upload ไปที่ Sharepoint
        s = Sharepoint(username, password, sharepoint_url)
        s.upload_to_sharepoint('Report/Lotuss/Products', dst)

        os.remove(dst)
        
        spider.logger.info('Spider closed: %s', spider.name)

    def start_requests(self):

        # ดึงข้อมูลสินค้าโปรโมทชั่นก่อน
        for index in range(1, 40): # Default 40
            
            payload = json.dumps({
                    "offset": 15*index,
                    "limit": 15,
                    "filter": {
                        "categoryId": [
                            "97571"
                        ]
                    },
                    "websiteCode": "thailand_hy"
                })
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'th',
                "key": "Vp9n5jFIPcNFHZBLsLBJ5iEMbFscZplK",
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
            }
            urls = "https://api-customer.lotuss.com/lotuss-mobile-bff/product/v2/products?websiteCode=thailand_hy"
            yield scrapy.Request(url=urls, callback=self.parse_promotions, headers=headers,method="POST",body=payload)
            
        # url = "https://api-customer.lotuss.com/lotuss-mobile-bff/product/v2/products?websiteCode=thailand_hy"
        self.counter = 0
        file_order = './config_mer_lotuss_checking_o2o/Order_files.xlsx'
        self.item_products = pd.read_excel(file_order, sheet_name='Lotus', index_col=False)['กลุ่มสินค้า'].values

        for item_product in self.item_products:

            payload = json.dumps({
                "offset": 0,
                "limit": 20,
                "filter": {},
                "search": item_product,
                "sort":"relevance:DESC",
                "websiteCode":"thailand_hy",
            })
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'th',
                "key": "Vp9n5jFIPcNFHZBLsLBJ5iEMbFscZplK",
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
            }
            urls = "https://api-customer.lotuss.com/lotuss-mobile-bff/product/v2/products?websiteCode=thailand_hy"
            yield scrapy.Request(url=urls, callback=self.parse, headers=headers,method="POST",body=payload)

            #Bypass
            #break
            
    def parse(self, response):

        lotuss_item = MarketPriceCheckingForO2OItem()
        today = date.today()
        datetime = today
                
        data_json = response.json()['data']['products']
        for data in data_json:

            item_name = data['name']
            normal_price = round(data['priceRange']['minimumPrice']['finalPrice']['value'], 0)
            promotion_price = data['priceRange']['minimumPrice']['regularPrice']['value']
            discount = round(data['priceRange']['minimumPrice']['discount']['percentOff'], 0)
            img_product_url = data['mediaGallery'][0]['url']
            
            if len(data['promotions']) > 0:
                img_promotion_url = data['promotions'][0]['image']
                if int(discount) == 0:
                    promotion_type = 'ซื้อ 1 แถม 1'
                elif int(discount) > 0:
                    promotion_type = 'ลดราคาสินค้า'

                remark = 'ไม่มีระยะเวลาโปรโมทชั่น'
            else:
##                print("Don't have promotions")
                img_promotion_url = ''
                promotion_type = ''
                remark = ''

            lotuss_item['Name_Web_Site'] = "Lotus"
            lotuss_item['Cate'] = self.item_products[self.counter]
            lotuss_item['Subcate'] = ''
            lotuss_item['Item_Name'] = item_name
            lotuss_item['Unit'] = ''
            lotuss_item['Normal_Price'] = normal_price
            lotuss_item['Promotion_Price'] = promotion_price
            lotuss_item['Promotion_Period'] = ''
            lotuss_item['Promotion_Type'] = promotion_type
            lotuss_item['Discount'] = discount
            lotuss_item['Remark'] = remark
            lotuss_item['Imag_Product_Url'] = img_product_url
            lotuss_item['Img_Promotion_Url'] = img_promotion_url
            lotuss_item['Date'] = datetime
        
            #print(response.json()['data']['products'])
            yield lotuss_item

        self.counter += 1

    def parse_promotions(self, response):

        lotuss_item = MarketPriceCheckingForO2OItem()
        today = date.today()
        datetime = today
                
        data_json = response.json()['data']['products']
        for data in data_json:

            item_name = data['name']
            normal_price = round(data['priceRange']['minimumPrice']['finalPrice']['value'], 0)
            promotion_price = data['priceRange']['minimumPrice']['regularPrice']['value']
            discount = round(data['priceRange']['minimumPrice']['discount']['percentOff'], 0)
            img_product_url = data['mediaGallery'][0]['url']
            
            if len(data['promotions']) > 0:
                img_promotion_url = data['promotions'][0]['image']
                if int(discount) == 0:
                    promotion_type = 'ซื้อ 1 แถม 1'
                elif int(discount) > 0:
                    promotion_type = 'ลดราคาสินค้า'

                remark = 'ไม่มีระยะเวลาโปรโมทชั่น'
            else:
                img_promotion_url = ''
                promotion_type = ''
                remark = ''

            lotuss_item['Name_Web_Site'] = "Lotus"
            lotuss_item['Cate'] = 'สินค้าโปรโมทชั่น'
            lotuss_item['Subcate'] = ''
            lotuss_item['Item_Name'] = item_name
            lotuss_item['Unit'] = ''
            lotuss_item['Normal_Price'] = normal_price
            lotuss_item['Promotion_Price'] = promotion_price
            lotuss_item['Promotion_Period'] = ''
            lotuss_item['Promotion_Type'] = promotion_type
            lotuss_item['Discount'] = discount
            lotuss_item['Remark'] = remark
            lotuss_item['Imag_Product_Url'] = img_product_url
            lotuss_item['Img_Promotion_Url'] = img_promotion_url
            lotuss_item['Date'] = datetime
        
            #print(response.json()['data']['products'])
            yield lotuss_item
            
