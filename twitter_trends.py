# -*- coding: utf-8 -*-
"""
@author: giancarlo.pagliaroli
"""
#pip install -U selenium
#sudo apt-get install chromium-chromedriver
import os
import time as time
import mail_sender
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

baseurl = "https://trends24.in/united-states/"
accept_button_login = """/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]/p"""
df_cols = ['time','keyword', 'ranking', 'tweets']
rows = []
#trends = pd.read_csv('trends.txt', sep=',')
scelta = 'y'
#####OPTIONS DRIVER CHROME#############################################
def avvio_driver_Chrome_headless():
    global mydriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    #Windows
    #mydriver = webdriver.Chrome("C:\python\chromedriver.exe", chrome_options=chrome_options)
    #raspberry
    #
    mydriver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)
    
def avvio_driver_Chrome_noheadless():
    
    global mydriver
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    mydriver = webdriver.Chrome("C:\python\chromedriver.exe", chrome_options=opts)
    #mydriver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)



def twitter_trends():
    
     if scelta == 'y' or scelta == 'Y':
         
         avvio_driver_Chrome_headless()
     else:
         
         avvio_driver_Chrome_noheadless()
     
     trends = pd.read_csv('trends.txt', sep=',')
     mydriver.get(baseurl)
     #mydriver.maximize_window()
     print("Cerca...")
     WebDriverWait(mydriver,100).until(EC.element_to_be_clickable((By.XPATH,accept_button_login)))
     mydriver.find_element_by_xpath(accept_button_login).click()
     
     
     for keyword in trends['keywords']:
         for rank in range(1, 11, 1):
             
             key = mydriver.find_element_by_xpath("""//*[@id="trend-list"]/div[1]/ol/li["""+ str(rank) +"""]/a""").text
             
             try:
                 tweets = mydriver.find_element_by_xpath("""//*[@id="trend-list"]/div[1]/ol/li["""+ str(rank) +"""]/span""").text
             except:
                 tweets = ""
                
                                    
             if keyword in key.lower():
                 body = "key: "+str(key)+ "    ranking: " + str(rank) + "    tweets: "+str(tweets)+ "    time: " + str(datetime.today().strftime("%Y%m%d_%H%M")) 
                 print(body)
                 rows.append({"time" : datetime.today().strftime("%Y%m%d_%H%M"), "keyword" : key, "ranking": rank, "tweets" : tweets })
                 df = pd.DataFrame(rows, columns = df_cols)
                 df.to_csv("""output_twitter.csv""", index = False)
                 #parameters: send_to, subject, body
                 subject = key + " - ranking " + str(rank)
                 print("Invio mail...")
                 mail_sender.send_mail('<Insert your destinaton mail>',subject, body)
     mydriver.quit()
     print("Fine Cerca")            
         
         
while True:
    
    twitter_trends()
    time.sleep(3600)