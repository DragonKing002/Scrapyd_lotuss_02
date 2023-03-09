# Scrapy settings for Market_Price_Checking_for_O2O project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from shutil import which
import chromedriver_autoinstaller
import random 
chromedriver_autoinstaller.install()
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS=['--headless']

BOT_NAME = 'Market_Price_Checking_for_O2O'

SPIDER_MODULES = ['Market_Price_Checking_for_O2O.spiders']
NEWSPIDER_MODULE = 'Market_Price_Checking_for_O2O.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Market_Price_Checking_for_O2O (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 10
RANDOMIZE_DOWNLOAD_DELAY = True # 
DOWNLOAD_DELAY = random.uniform(0.5,1.5) * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY_MIN = 2
RANDOMIZE_DOWNLOAD_DELAY_MAX = 20
AUTOTHROTTLE_ENABLED = True
COOKIES_ENABLED = False
HTTPCACHE_ENABLED = False

# # Retry many times since proxies often fail
RETRY_TIMES = 3
# # Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408, 429, 423]
LOG_LEVEL = 'ERROR'
# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
DOWNLOADER_MIDDLEWARES = {
     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
     'Market_Price_Checking_for_O2O.middlewares.TooManyRequestsRetryMiddleware': 543,
##     'scrapy_selenium.SeleniumMiddleware': 800
}

# ITEM_PIPELINES = {
#     'Market_Price_Checking_for_O2O.pipelines.MarketPriceCheckingForO2OPipeline': 100,
# }
# FEEDS = {
#     'data/%(name)s/%(name)s_%(time)s.csv': {
#         'format': 'csv',
#         }
# }
# FEED_EXPORT_ENCODING = 'utf-8'
