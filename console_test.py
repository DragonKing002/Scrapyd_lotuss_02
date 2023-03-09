from scrapyd_api import ScrapydAPI
import requests
import os
# os.system('cmd /c "scrapyd"')
# os.system('cmd /c "scrapyd-deploy default"')
# scrapyd
# scrapyd-deploy default

ip_adress = 'http://122.248.201.223:6800/'
scrapyd = ScrapydAPI(ip_adress)
r = requests.get(ip_adress + 'daemonstatus.json')
status = r.json()
print(status)
list_project = scrapyd.list_projects()
print(list_project)
spider_list = scrapyd.list_spiders('Market_Price_Checking_for_O2O')
print(spider_list)
r = requests.get(ip_adress + 'listjobs.json')
list_jobs = r.json()
print(list_jobs)
runspider = scrapyd.schedule('Market_Price_Checking_for_O2O', 'lotuss')
print(runspider)

