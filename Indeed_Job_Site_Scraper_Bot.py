#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
import selenium 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time


# In[2]:


driver = webdriver.Chrome("your chrome web driver location here\\chromedriver.exe")
url = "https://in.indeed.com/"
driver.get(url)


# In[4]:


job_title = input("what is the job that you are looking for..? ")
loc = input("please tell us the location where you are finding the job.. ")
path =input("enter the path where you would like to store the scraped csv file.? **NOTE if your file path looks like C:\\Users\\asus\\Desktop\\Desktop\\Project Indeed Job Site Scraping then put it like C:\\Users\\asus\\Desktop\\Desktop\\Project Indeed Job Site Scraping")
what_box = driver.find_element(by = "xpath", value ="//input[@id ='text-input-what']")
where_box = driver.find_element(by ="xpath" , value ="//input[@id ='text-input-where']")
find_jobs_button =  driver.find_element(by = "xpath", value ="//button[@class = 'yosegi-InlineWhatWhere-primaryButton']")
what_box.send_keys(job_title)
where_box.send_keys(loc)
find_jobs_button.click()


# In[5]:


df = pd.DataFrame({'Company Name':[''],'Location':[''],'Expected Salary':[''],'Job Title':[''],'Description About the Job':[''],'Link':[''],'Date Posted/Active':['']})
while True:
    soup = BeautifulSoup(driver.page_source ,'lxml')
    start = soup.find('ul',class_='jobsearch-ResultsList css-0')
    for litag in start.find_all('li'):
        try:
            title = litag.find('h2',class_='jobTitle css-1h4a4n5 eu4oa1w0').text
            company = litag.find('span',class_='companyName').text
            link = litag.find('a',class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
            link_full = 'https://in.indeed.com'+link
            description = litag.find('ul',{'style':'list-style-type:circle;margin-top: 0px;margin-bottom: 0px;padding-left:20px;'}).text

            try:
                location = litag.find('div',class_='companyLocation').text

            except:
                location = 'N/A'
            try:
                salary  = litag.find('div',class_='metadata salary-snippet-container').text
            except:
                salary ='N/A'
            date = litag.find('span',class_='date').text


            length = len(df)
            df.loc[length]={'Company Name':company,'Location':location,'Expected Salary':salary,'Job Title':title,'Description About the Job':description,'Link':link_full,'Date Posted/Active':date}
        except:
            pass
    try:
        button_to_next_page = soup.find('a',{'aria-label':'Next Page'}).get('href')
        driver.get('https://in.indeed.com'+button_to_next_page)
    except:
        print("All Data Scraped Successfully.....")
        break

df.to_csv("your directory where you want to save this scraped file\\{}.csv".format(job_title))


# #### * Now we have scraped all the postings data from the Indeed Job Site 
# #### * Now we would like to email it to the targeted addresses/address
# 

# In[16]:


import smtplib ,ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email.mime.multipart import MIMEMultipart
from email import encoders


# In[14]:


sender = input("Enter the sender's email/gmail address ")
reciever = input("Enter the reciever's email/gmail address ")


# In[21]:


msg = MIMEMultipart()
msg['Subject'] = 'New postings on Indeed'
msg['From']  = sender
msg['To'] = ','.join(reciever)

part = MIMEBase('application', 'octet-stream')
part.set_payload(open("the location where you saved the scraped file\\{}.csv".format(job_title),'rb').read())
encoders.encode_base64(part)
part.add_header('Content-Disposition','attachment; filename ="the location where you saved the scraped file\\{}.csv"'.format(job_title))
msg.attach(part)

s=smtplib.SMTP_SSL(host ='smtp.gmail.com',port = 465)
s.login(user = 'senders gmail id here',password  = 'senders password here')
s.sendmail(sender,reciever,msg.as_string())
s.quit()


# In[20]:


import sys
print(sys.executable)


# In[ ]:




