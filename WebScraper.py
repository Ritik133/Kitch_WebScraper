#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bs4
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup 

import csv
import concurrent.futures


# In[2]:


#function to count the number of pages associated with the search
def pages(url):
    global count
    params = {'api_key':'42e2a129e57389d742a5f8564fb814bf', 'url': url}
    page=requests.get('http://api.scraperapi.com/',params=urlencode(params))
    soup =BeautifulSoup(page.content,'html.parser')
    results = soup.find_all('a',class_='d-block text-center clickable')
    count=0
    for r in results:
        try:
            if int(r.text) not in list:
                #print(int(r.text))
                list.append(int(r.text))
                count+=1
        except:
            continue
    if count == 0:
        return
    else:
        pages("https://www.talabat.com/uae/restaurants/1308/jumeirah-lakes-towers-jlt?&page=%d"%(list[-1]))


# In[3]:


list=[] #to count the number of pages
#pass the baseurl of the area to the pages function
pages("https://www.talabat.com/uae/restaurants/1308/jumeirah-lakes-towers-jlt")


# In[4]:


#store the base url in url_list
url_list=["https://www.talabat.com/uae/restaurants/1308/jumeirah-lakes-towers-jlt"]
for i in list:
    url_list.append("https://www.talabat.com/uae/restaurants/1308/jumeirah-lakes-towers-jlt?&page=%d"%(i))


# In[5]:


#column headers for the table
header=["brand_name",
            "cuisine_tags",
            "restaurant_rating",
            "delivery_time",
            "service_fee",
            "minimum_order_amount",
            "new_restaurant"]
with open('restaurant_data.csv', mode='w') as rest_data:
        data_writer = csv.writer(rest_data)
        data_writer.writerow(header)


# In[6]:


data=[] #list to store details of all Restaurants


# In[7]:


def insert_data(url):
    
    params = {'api_key':'42e2a129e57389d742a5f8564fb814bf', 'url': url}
    page=requests.get('http://api.scraperapi.com/',params=urlencode(params))
    soup =BeautifulSoup(page.content,'html.parser')
    #print(soup.prettify())
    results = soup.find_all('div',class_='list-itemstyles__VendorListItemContainer-ia2hbn-0 eLZatB')
    
    for res in results:
        obj=[] #list to store details at per-restaurant level
        
        #extract restaurant name
        brand_name=res.find('div',class_="restaurant-title pb-1") 
        obj.append(brand_name.text) 
        
        #extract cuisines and add to cuisine_tags array      
        cuisine_tags=res.find('div',class_="cuisines-section pb-1 truncate") #get cuisine details
        str=cuisine_tags.text.replace(',',"").split()
        cuisine_tags_arr=[] # array of restaraunt cuisine
        for i in str:
            if i != "and" and i != "&":
                cuisine_tags_arr.append(i)
        obj.append(cuisine_tags_arr)
        
        #extract restaurant information
        restaurant_info=res.find('div',class_="ratings-and-new-section pb-1 d-flex")
        #check if restaurant is NEW  
        new_info=restaurant_info.find('div',class_="new-restaurant-label f-10 text-center mr-2 f-500")
        if new_info is None:
            new_flag=False
        else:
            #print(new_info.text)
            new_flag=True
        #extract rating_info
        rating_info=res.find('div',class_="rating-displaystyles__RatingDisplayContainer-sc-19r5mol-0 jabHoj")
        if rating_info is not None:
            obj.append(rating_info.text)
            #print(rating_info.text)
        else:
            obj.append("NA")
    
        #extract restaurant delivery information i.e., delivery_time,service_fee,minimum_order_amount
        delivery_info=res.find('div',class_="info-section pb-1 f-14 delivery-info d-flex")
        delivery_time=delivery_info.find('span',class_="mr-2")
        service_fee=delivery_time.find_next_sibling("span","mr-2")
        minimum_order_amount=delivery_info.find('span',class_="d-sm-block")
        obj.append(int(delivery_time.text.split(" ")[1]))
        
        #check if service fee is free then add fee as 0 otherwise add the parsed fee
        if service_fee.text != "Free":
            obj.append(int(float(service_fee.text)))
        else:
            obj.append(0)
       
        obj.append(int(float(minimum_order_amount.text.split()[1])))
        obj.append(new_flag)
        data.append(obj)
    
    
    


# In[8]:


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(insert_data, url_list)


# In[9]:


#store the scraped data in csv file
with open('restaurant_data.csv', mode='a') as rest_data:
        data_writer = csv.writer(rest_data)
        for d in data:
            data_writer.writerow(d)


# In[ ]:




