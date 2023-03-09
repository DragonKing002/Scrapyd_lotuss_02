import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from datetime import date
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import boto3
from botocore.exceptions import ClientError
import json

##from config_key import ACCESS_KEY_ID,SECRET_ACCESS_KEY
ACCESS_KEY_ID = 'AKIAQL6UMMH2NVSOC5M4'
SECRET_ACCESS_KEY = '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'


class Outlook():
    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    def send_mail(self,filename,mail_from,mail_to,mail_subject,mail_body):
        mimemsg = MIMEMultipart()
        mimemsg['From']=mail_from
        mimemsg['To']=mail_to
        mimemsg['Subject']=mail_subject
        msgAlternative = MIMEMultipart('alternative')
        with open(filename,'rb') as file:
        # Attach the file with filename to the email
            mimemsg.attach(MIMEApplication(file.read(), Name=filename))
        msgText = MIMEText(mail_body)
        mimemsg.attach(msgText)
        connection = smtplib.SMTP(host='smtp.office365.com', port=587)
        connection.starttls()
        connection.login(self.username,self.password)
        connection.send_message(mimemsg)
        connection.quit()

class Sharepoint():
    def __init__(self,username,password,sharepoint_url):
        self.username = username
        self.password = password
        self.user_credentials = UserCredential(username, password)
        self.sharepoint_url = sharepoint_url
    # create client context object
        self.ctx = ClientContext(self.sharepoint_url).with_credentials(self.user_credentials)
        
    def create_sharepoint_directory(self,dir_name: str):
        """
        Creates a folder in the sharepoint directory.
        """
        if dir_name:

            result = self.ctx.web.folders.add(f'Shared Documents/{dir_name}').execute_query()

            if result:
                # documents is titled as Shared Documents for relative URL in SP
                relative_url = f'Shared Documents/{dir_name}'
                return relative_url
        
    
    def upload_to_sharepoint(self,dir_name: str, file_name: str):
                
        sp_relative_url = self.create_sharepoint_directory(dir_name)
        target_folder = self.ctx.web.get_folder_by_server_relative_url(sp_relative_url)

        with open(file_name, 'rb') as content_file:
            file_content = content_file.read()
            target_folder.upload_file(file_name, file_content).execute_query()
        
    def download_sharepoint(self,dir_name,file_name):
        sp_relative_url = self.create_sharepoint_directory(dir_name)
        folder = self.ctx.web.get_folder_by_server_relative_url(sp_relative_url)
        file = folder.files.get_by_url(file_name)
        with open(file_name, "wb") as f:
            file.download(f).execute_query()

class Secrect():
    def __init__(self):
        pass
    def get_secret(self):

        secret_name = "Config_Mail"
        region_name = "ap-southeast-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        # print(ACCESS_KEY_ID, SECRET_ACCESS_KEY)
        # print("OKKKKK")
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY,
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        # Decrypts secret using the associated KMS key.
        secret_dict = json.loads(get_secret_value_response['SecretString'])
        # print(secret_dict)
        
        # Your code goes here.
        # retrun dict [username,password]
        return secret_dict
    
if "__main__" == __name__:

    config =  Secrect().get_secret()
    username = config['username']
    password = config['password']

    import pandas as pd

    filename = 'requirements.txt'
    mails_to = pd.read_excel('./spiders/config_mer_lotuss_checking_o2o/Email-Cofig.xlsx', index_col=False)['To']
    mails_to = ','.join(mails_to.dropna().tolist())

    mail_subject = 'รายงานการดึงข้อมูลจากเว็บโลตัสสำหรับงาน O2O'
    mail_body = '''

                สำหรับข้อมูลด้านในจะเป็นการดึงข้อมูล Products จากเว็บโลตัสตาม Order ที่ลูกค้าได้กำหนดไว้ให้
                จึงเรียนมาเพื่อทราบ

                
                '''
    
    o = Outlook(username,password)
    o.send_mail(filename=filename,mail_from=username,\
                mail_to=mails_to,mail_subject=mail_subject,mail_body=mail_body)
    
##    sharepoint_url = "https://cpallgroup.sharepoint.com/sites/MST-MarketPriceCheckingforO2O"
##    config =  Secrect().get_secret()
##    username = config['username']
##    password = config['password']
##    s = Sharepoint(username, password, sharepoint_url)
##    s.download_sharepoint('Email-Config','Email-Cofig.xlsx')
    pass
    

    # sharepoint_url = "https://cpallgroup.sharepoint.com/sites/MST-MarketPriceCheckingforO2O"
    # config =  Secrect().get_secret()
    # username = config['username']
    # password = config['password']

    # print(username, password)
    # username = "rpa-notification@cpall.co.th"
    # password = "JIN*Aoztc2nR"
    # s = Sharepoint(username, password, sharepoint_url)
    # create = s.('Report/Shopee')
    # s.upload_to_sharepoint('Report/BigC/test','tops.csv')
    # s.download_sharepoint('Report/BigC/test','tops.csv')
##    s.create_sharepoint_directory('ddd')
