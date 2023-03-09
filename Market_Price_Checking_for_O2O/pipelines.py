# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import date

def send_mail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.application import MIMEApplication
    filename = "Market_Price_Checking_for_O2O\\%(name)s_{}.csv".format(date.today())
    username = "isornham@gosoft.co.th"
    password = "Jeepza_1004*"


    mail_from = "isornham@gosoft.co.th"
    mail_to = "isornham@gosoft.co.th"
    mail_subject = "Test Subject"
    mail_body = "This is a test message"

    mimemsg = MIMEMultipart()
    mimemsg['From']=mail_from
    mimemsg['To']=mail_to
    mimemsg['Subject']=mail_subject
    msgAlternative = MIMEMultipart('alternative')
    with open(filename,'rb') as file:
    # Attach the file with filename to the email
        mimemsg.attach(MIMEApplication(file.read(), Name=filename))
    msgText = MIMEText('This is a test message')
    mimemsg.attach(msgText)
    connection = smtplib.SMTP(host='smtp.office365.com', port=587)
    connection.starttls()
    connection.login(username,password)
    connection.send_message(mimemsg)
    connection.quit()

class MarketPriceCheckingForO2OPipeline:
    
    head_url = 'https://www.bigc.co.th'
    
    def process_item(self, item, spider):
        if item['Imag_Product_Url']:
            item['Imag_Product_Url'] = self.head_url+item['Imag_Product_Url']
        
        if item['Item_Name']:
            text = item['Item_Name']
            if text.find("แพ็ค") != -1:
                item['Pack_Type'] = text[text.find("แพ็ค"):]
        return item

class LotussPipeline:
    head_url = 'https://www.lotuss.co.th'
    def process_item(self, item, spider):
        if item['Imag_Product_Url']:
            #item['Imag_Product_Url'] = self.head_url+item['Imag_Product_Url']
            item['Imag_Product_Url'] = item['Imag_Product_Url']
        
        if item['Item_Name']:
            text = item['Item_Name']
            if text.find("แพ็ค") != -1:
                item['Pack_Type'] = text[text.find("แพ็ค"):]
            else:
                item['Pack_Type'] = ''
                
##            if text.find("มล") != -1 and text.find("แพ็ค") == -1:
##                item['Pack_Type'] = " ".join([text[:text.find("มล")].split(' ')[-1], 'มล.'])
##            else:
##                item['Pack_Type'] = ''
        return item

class LazadaPipeline:
    def process_item(self, item, spider):
        if item['Imag_Product_Url']:
            item['Imag_Product_Url'] = item['Imag_Product_Url']

##        if 'data:image' in item['Img_Promotion_Url']:
##            item['Img_Promotion_Url'] = ''
            
        if item['Item_Name']:
            text = item['Item_Name']
            if text.find("แพ็ค") != -1:
                item['Pack_Type'] = text[text.find("แพ็ค"):]
            else:
                item['Pack_Type'] = ''
        return item


class TopsPipeline:
    
    head_url = 'https://www.bigc.co.th'
    
    def process_item(self, item, spider):

        if item['Promotion_Period']:
            item['Promotion_Period'] = item['Promotion_Period'].replace("<span>","").replace("</span>","")

        if item['Promotion_Type']:
            item['Promotion_Type'] = item['Promotion_Type'].replace("<span>","").replace("</span>","")
        if item['Unit']:
            item['Unit'] = item['Unit'].replace(" / ","")

        if item['Item_Name']:
            # item['Item_Name'] = item['Item_Name']
            Item_Name = item['Item_Name']
            item['Subcate'] = Item_Name.split()[0]
            if Item_Name.find("แพค") != -1:
                item['Pack_Type'] = Item_Name[Item_Name.find("แพค"):]

        if item['Img_Promotion_Url']:
            item['Img_Promotion_Url'] = item['Img_Promotion_Url'][0]
            

        if item['Promotion_Price']:
            price_promo = item['Promotion_Price']
            price = item['Normal_Price']
            Discount = round((float(price)-float(price_promo))/float(price)*100,0) 
            item['Discount'] = "{}%".format(int(Discount))
        return item



class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['Item_Name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['Item_Name'])
            return item
        
