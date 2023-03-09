FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update
RUN apt-get -y install sudo 

RUN pip install boto3 
RUN pip install secure-smtplib 
RUN pip install Office365-REST-Python-Client
RUN pip install pandas
RUN pip install scrapy
RUN pip install chromedriver_autoinstaller
RUN pip install scrapyd
RUN pip install scrapy-user-agents
RUN pip install scrapy-useragents
RUN pip install scrapy_proxies
RUN pip install scrapy-rotating-proxies
RUN pip install openpyxl

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - 


# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

COPY scrapyd.conf /app/

EXPOSE 6800

CMD ["scrapyd", "--pidfile="] 

# docker run -d -p 6800:6800 my-scrapyd-image  
# docker build -t my-scrapyd-image .
#/var/lib/scrapyd/items