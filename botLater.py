#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install selenium
import numpy as np
import pandas as pd
from selenium import webdriver
import random
from time import time, sleep
import math
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# In[2]:


#extracting the company names
file = 'firmlist_20190125_pr.csv'
xl = pd.read_csv(file)
company_names = xl['conm']
company_names
#Initializing the dataFrame
column = ['Company','Author', 'Date', 'Time', 'Title', 'Content']
DATA = pd.DataFrame(columns=column)
DATA = DATA.fillna(0)


# In[50]:


#intializing everything properly
#for profile settings
profile = webdriver.FirefoxProfile()
path_to_firefoxdriver = '*********************'
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("**************************')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/rtf")
browser = webdriver.Firefox( executable_path = path_to_firefoxdriver, firefox_profile=profile)
url = 'http://guides.lib.uw.edu/factiva'
browser.get(url)



sleep(5)
browser.find_element_by_id('weblogin_netid').send_keys("*************")
browser.find_element_by_id ('weblogin_password').send_keys("************")
browser.find_element_by_id("submit_button").click()

#Sleep for some seconds
sleep(25)


# In[81]:


temp = np.array(company_names[5029:])
#PRIMELINE ENERGY HLDGS INC is not there due to academic restriction
#SANCHEZ MIDSTREAM PARTNRS LP
#KAYNE ANDERSON ENERGY DEV CO
temp


# In[83]:


for j in np.arange(0, len(temp)):
    company = temp[j]
    browser.find_element_by_id('sfs').click()
    browser.find_element_by_id('atx').clear()
    browser.find_element_by_id('atx').send_keys(company)

    #for the dates
    browser.find_element_by_xpath('//*[@id="dr"]/option[contains(text(), "Enter date range...")]').click()
    browser.find_element_by_id('frm').clear()
    browser.find_element_by_id('frd').clear()
    browser.find_element_by_id('fry').clear()
    browser.find_element_by_id('tom').clear()
    browser.find_element_by_id('tod').clear()
    browser.find_element_by_id('toy').clear()
    browser.find_element_by_id('frm').send_keys('11')

    browser.find_element_by_id('frd').send_keys('01')

    browser.find_element_by_id('fry').send_keys('2005')

    browser.find_element_by_id('tom').send_keys('12')

    browser.find_element_by_id('tod').send_keys('31')

    browser.find_element_by_id('toy').send_keys('2018')
    sleep(5)


    #Selecting the source
    browser.find_element_by_id('scTab').click()
    #//*[@id="scCat"]
    browser.find_element_by_xpath('//*[@id="scCat"]/option[contains(text(), "By Type")]').click()
    sleep(5)
    #//*[@id="scMnu"]/ul/li[23]/span
    browser.find_element_by_xpath('//*[@id="scMnu"]/ul/li[23]/span').click()
    sleep(5)
    browser.find_element_by_css_selector('#scMnu > ul:nth-child(1) > li:nth-child(23) > div:nth-child(5) > ul:nth-child(1) > li:nth-child(2) > span:nth-child(1)').click()
    sleep(5)
    browser.find_element_by_css_selector('#scMnu > ul:nth-child(1) > li:nth-child(23) > div:nth-child(5) > ul:nth-child(1) > li:nth-child(2) > div:nth-child(5) > ul:nth-child(1) > li:nth-child(42) > a:nth-child(1)').click()
    browser.find_element_by_css_selector('#scMnu > ul:nth-child(1) > li:nth-child(23) > div:nth-child(5) > ul:nth-child(1) > li:nth-child(2) > div:nth-child(5) > ul:nth-child(1) > li:nth-child(160) > a:nth-child(1)').click()
    sleep(1)
    browser.find_element_by_id("btnSBSearch").click()
    #Sleep for some seconds
    sleep(25)

    #to get articles in formatible view
    browser.find_element_by_id('framesLink').click()
    sleep(3)
    count = 0
    #WE HAVE ENTERED THE RESULT SECTION, THIS IS WHERE THE FOR LOOPS COME INTO PLAY
    limit = int(browser.find_element_by_class_name("resultsBar").get_attribute('data-hits'))
    elementsLeftToBeSearched = limit
    currentRun = 1
    loops = -1
    while(elementsLeftToBeSearched > 0):
        sleep(5)
        if(elementsLeftToBeSearched/ ( 100) != 0):
            loops = 100
        else:
            loops = elementsLeftToBeSearched % (100)
        for  i  in np.arange(0, loops):
            #first element tr.headline:nth-child(1) > td:nth-child(3) > a:nth-child(2)
            number = i + 1
            count += 1
            #SOURCE
            sleep(1)
            #div.article:nth-child(1) > div:nth-child(8) > a:nth-child(1)
            #div.article:nth-child(1) > div:nth-child(6) > a:nth-child(1)
            ####
            #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
            #tr.headline:nth-child(29) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
            #tr.headline:nth-child(8) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
            #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
            #sourcePath
            sourcePath = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)'
            source = browser.find_element_by_css_selector(sourcePath)
            timePath = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > div:nth-child(3)'
            timings = browser.find_element_by_css_selector(timePath).text
            timings = timings.split(', ')
            pathName = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > a:nth-child(2)'
            browser.find_element_by_css_selector(pathName).click()
            #this is where we collect the data
            #HEADLINE
            sleep(9)
            #element = WebDriverWait(browser, 80).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div/div[1]/span')))
            headline = browser.find_element_by_css_selector("span.enHeadline")
            #TOTAL WORDS
            totalWords = browser.find_element_by_css_selector("div.article:nth-child(1) > div:nth-child(6)")
            #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3)
            if(len(timings) == 4):
                #DATE
                date = timings[1]
                #TIME
                time = 'NaN'
            else:
                #DATE
                date = timings[2]
                #TIME
                time = timings[1]
            #ARTICLE
            #article = browser.find_element_by_css_selector(".articleParagraph")
            article = browser.find_element_by_css_selector(".article")
            #column = ['Company','Author', 'Date', 'Title', 'Content']
            DATA = DATA.append({'Company': company, 'Author': source.text, 'Date': date, 'Time': time, 'Title': headline.text ,'Content': article.text }, ignore_index=True)
            #sleep(3)
        elementsLeftToBeSearched = elementsLeftToBeSearched - loops
        currentRun += 1
        #this is where the current page ends, so we have to go back up and click next
        if(elementsLeftToBeSearched > 0):
            seconds = 5 + (random.random() * 5)
            sleep(seconds)
            browser.find_element_by_class_name('nextItem').click()
    #save the data that has been collected till now in a csv file
    #clicking the search button, to look for another company
    browser.find_element_by_css_selector('#navmbm0').click()
    sleep(10)
    DATA.to_excel("work1.xlsx", header=True, encoding = 'utf-8') 


# In[ ]:





# In[95]:


DATA.to_excel("work1.xlsx", header=True, encoding = 'utf-8')


# In[94]:


#WHEN THE BOT CRASHES
#when failure occurs, the option to start back from here:, just for that company
failure = True
index = count
failureRun = 2
#elementsLeftToBeSearched = 48
#loops =48
for  i  in np.arange(index, loops):
    #first element tr.headline:nth-child(1) > td:nth-child(3) > a:nth-child(2)
    number = i+1
    
    #SOURCE
    sleep(1)
    #div.article:nth-child(1) > div:nth-child(8) > a:nth-child(1)
    #div.article:nth-child(1) > div:nth-child(6) > a:nth-child(1)
    ####
    #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
    #tr.headline:nth-child(29) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
    #tr.headline:nth-child(8) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
    #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
    #sourcePath
    sourcePath = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)'
    source = browser.find_element_by_css_selector(sourcePath)
    timePath = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > div:nth-child(3)'
    timings = browser.find_element_by_css_selector(timePath).text
    timings = timings.split(', ')
    pathName = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > a:nth-child(2)'
    browser.find_element_by_css_selector(pathName).click()
    #this is where we collect the data
    #HEADLINE
    sleep(9)
    #element = WebDriverWait(browser, 80).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div/div[1]/span')))
    headline = browser.find_element_by_css_selector("span.enHeadline")
    count += 1
    #TOTAL WORDS
    totalWords = browser.find_element_by_css_selector("div.article:nth-child(1) > div:nth-child(6)")
    #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3)
    if(len(timings) == 4):
        #DATE
        date = timings[1]
        #TIME
        time = 'NaN'
    else:
        #DATE
        date = timings[2]
        #TIME
        time = timings[1]
    #ARTICLE
    #article = browser.find_element_by_css_selector(".articleParagraph")
    article = browser.find_element_by_css_selector(".article")
    #column = ['Company','Author', 'Date', 'Title', 'Content']
    DATA = DATA.append({'Company': company, 'Author': source.text, 'Date': date, 'Time': time, 'Title': headline.text ,'Content': article.text }, ignore_index=True)
    #sleep(3)
elementsLeftToBeSearched = elementsLeftToBeSearched - loops
currentRun += 1
if(elementsLeftToBeSearched  > 0):
    browser.find_element_by_class_name('nextItem').click()

sleep(10)
#WE HAVE ENTERED THE RESULT SECTION, THIS IS WHERE THE FOR LOOPS COME INTO PLAY
limit = int(browser.find_element_by_class_name("resultsBar").get_attribute('data-hits'))

#elementsLeftToBeSearched = 5253
#currentRun = 7
loops = -1
while(elementsLeftToBeSearched > 0):
    sleep(10)
    count = 0
    if(elementsLeftToBeSearched / (100) != 0):
        loops = 100
    else:
        loops = elementsLeftToBeSearched % (100)
    for  i  in np.arange(0, loops):
        #first element tr.headline:nth-child(1) > td:nth-child(3) > a:nth-child(2)
        number = i + 1
        
        #SOURCE
        sleep(1)
        #div.article:nth-child(1) > div:nth-child(8) > a:nth-child(1)
        #div.article:nth-child(1) > div:nth-child(6) > a:nth-child(1)
        ####
        #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
        #tr.headline:nth-child(29) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
        #tr.headline:nth-child(8) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
        #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)
        #sourcePath
        sourcePath = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > div:nth-child(3) > a:nth-child(1)'
        source = browser.find_element_by_css_selector(sourcePath)
        timePath = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > div:nth-child(3)'
        timings = browser.find_element_by_css_selector(timePath).text
        timings = timings.split(', ')
        pathName = 'tr.headline:nth-child(' + str(number) + ') > td:nth-child(3) > a:nth-child(2)'
        browser.find_element_by_css_selector(pathName).click()
        #this is where we collect the data
        #HEADLINE
        sleep(10)
        #element = WebDriverWait(browser, 80).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div/div[1]/span')))
        #/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div/div[1]/span
        headline = browser.find_element_by_css_selector("span.enHeadline")
        count += 1
        #TOTAL WORDS
        totalWords = browser.find_element_by_css_selector("div.article:nth-child(1) > div:nth-child(6)")
        #tr.headline:nth-child(1) > td:nth-child(3) > div:nth-child(3)
        if(len(timings) == 4):
            #DATE
            date = timings[1]
            #TIME
            time = 'NaN'
        else:
            #DATE
            date = timings[2]
            #TIME
            time = timings[1]
        #ARTICLE
        #article = browser.find_element_by_css_selector(".articleParagraph")
        article = browser.find_element_by_css_selector(".article")
        #column = ['Company','Author', 'Date', 'Title', 'Content']
        DATA = DATA.append({'Company': company, 'Author': source.text, 'Date': date, 'Time': time, 'Title': headline.text ,'Content': article.text }, ignore_index=True)
        #sleep(3)
    elementsLeftToBeSearched = elementsLeftToBeSearched - loops
    currentRun += 1
    #this is where the current page ends, so we have to go back up and click next
    if(elementsLeftToBeSearched > 0):
        seconds = 5 + (random.random() * 5)
        sleep(seconds)
        browser.find_element_by_class_name('nextItem').click()
    #save the data that has been collected till now in a csv file
    #clicking the search button, to look for another company
browser.find_element_by_css_selector('#navmbm0').click()
sleep(10)
DATA.to_excel("work1.xlsx", header=True, encoding = 'utf-8')


# In[96]:


DATA


# In[ ]:




