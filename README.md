# Kitch_WebScraper


# Objective:
Extract and store data pertaining to restaurants available from the Talabat website.


This project primarily makes use of the Beautiful Soup module in python to parse html webpages.
Web Srcaping can be a tedious process and to optimize the performance in terms of time, we use multithreading to write to the csv file concurrently.

***

The csv file contains the following data for every restaraunt found on the website: 

1.brand_name (string)- Name of the restaurant. 
2.cuisine_tags(array) - List of cuisine served by the restaurant.    
3.restaurant_rating (string)- Talabat User Restaurant Rating ( NA - for some new restaurants). 
4.delivery time (int)- Time taken to deliver. 
5.service fee (int)- Service fee charged by the restaurant.    
6.minimum order amount(int) - Minimum Order Amount for delivery. 
7.new_restaurant (bool) - TRUE/FALSE depending on whether the restaurant is new on the website. 


*** 

The given code works well with the Jumeirah Lakes Towers - JLT area.
To be able to scrape data pertaining to other areas, all we have to do is replace the website base url at the appropriate lines, specifically:

```python 
#pass the baseurl of the area to the pages function
pages("website_base_url") 

#store the base url in url_list
url_list=["website_base_url"]

 ```
