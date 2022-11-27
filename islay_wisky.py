from selenium import webdriver
from fake_useragent import UserAgent
import os
import requests
from bs4 import BeautifulSoup as soup
import time
#import lxml
#%%
#設定Driver.exe的path & Base_url
#from selenium.webdriver.common.action_chains import ActionChains


URL = 'https://www.whiskyshop.com/single-malt-scotch-whisky/islay'
PATH = r'C:\SeleniumDrivers'
os.environ['PATH'] = PATH
 
#開啟 Chrome_driver 讀取url
driver = webdriver.Chrome()
driver.get(URL)
#%% test
names = driver.find_elements_by_css_selector('div[class="product details product-item-details"]')

out = []
for i in names:
    name = i.find_element_by_class_name("product-item-link").get_attribute("innerHTML").replace('&amp;','&')
    out.append(name)
print(out)



#%%

#%%
#將定位元素帶入for迴圈依序將 name & price 加到 LIST
from selenium.webdriver.remote.webelement import WebElement

def get_elements(elem_list1:WebElement, elem_list2:WebElement):
    output = []
    for i ,j in zip(elem_list1,elem_list2):
        name = i.find_elements_by_class_name("product-item-link")[0].get_attribute("innerHTML").replace('&amp;','&')
        driver.implicitly_wait(5)
        try:
            price = j.find_element_by_css_selector('span[class="price"]').get_attribute("innerText").replace('from ','')
        except:
            price = "Sold Out"
            driver.implicitly_wait(5)
        
        output.append({
            'product_name': name,
            'price': price
            })

    return output

#%%
def all_page_items(driver):
    #self.driver = driver
    all_elements = []
    while True:
        names = driver.find_elements_by_css_selector('div[class="product details product-item-details"]')
        prices = driver.find_elements_by_css_selector('div[data-role="priceBox"]')
        driver.implicitly_wait(10)
        
        all_elements.append(get_elements(names, prices))
        
        driver.implicitly_wait(10)
        
        nextpage = driver.find_elements_by_css_selector('#maincontent > div.columns > div.column.main > div:nth-child(5) > div.pages > ul > li.item.pages-item-next > a')
        driver.implicitly_wait(10)
        if len(nextpage) == 0:
            print('isEmpty')
            break
        else:
            print('----------nextpage------------')
            driver.execute_script("arguments[0].click()",nextpage[0]);
            driver.implicitly_wait(10)
            
    return all_elements

#%%

run = all_page_items(driver)

#%%
count = 1
for i in run:
    print(f'No{count}',i['product_name'],i['price'])
    count +=1

#%%
import json
with open('Islay_whisky.json','w') as f:
    json.dump(li, f,ensure_ascii=False)
    
#%%

with open('Islay_whisky.json','r') as f:
          data = json.load(f)
for i in data:
    print(i['price'])
#%%
#%%
#自動跳轉下一頁code
'''nextpage = driver.find_elements_by_css_selector('#maincontent > div.columns > div.column.main > div:nth-child(5) > div.pages > ul > li.item.pages-item-next > a')
driver.implicitly_wait(5)

driver.execute_script("arguments[0].click()",nextpage[0]);


#nextpage.click()
#ActionChains(driver).move_to_element(nextpage).click().perform()'''