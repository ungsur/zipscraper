# -*- coding: utf-8 -*-
#Regular expressions library is used for pattern matching
import re
import urllib
from bs4 import BeautifulSoup

#user agent is so that the website thinks it's a computer, not a program getting the page
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 

#from the first link, turn the contents of the first page into a soup object
url1 = 'http://www.codigopostalde.com.ar/en/'
request1 =  urllib.request.Request(url1,None,headers)
response1 =  urllib.request.urlopen(request1)
data = response1.read()

soup = BeautifulSoup(data, "lxml")
print(soup.prettify())

'''
we see that the links are after the /h3 section, so we look for 
the unordered lists after it and grab all of the links and put it in a 
dictionary of states with the statename as the key and the link as the value

'''
states_dict = {}
for link in soup.find('h3').find_next('ul').find_all("a"):
    print(link.text, link.get("href"))
    states_dict[link.text] = str(link.get("href"))
    
'''
From the list of states/links, we make a BS object from each state page to 
make a dictionary with city name as the key and city url, zipcode, and lat/long
as the values
'''
city_dict = {}
for k,v in states_dict.items():
    url_state = v
    statename = k
    temp_request =  urllib.request.Request(url_state,None,headers)
    temp_response =  urllib.request.urlopen(temp_request)
    temp_data = temp_response.read()
    temp_soup = BeautifulSoup(temp_data, "lxml")
    for link in temp_soup.find('h3').find_next('ul').find_all("a"):
        city_dict[link.text] = {'url':str(link.get("href")),'zipcode':'','lat':0.0,'long':0.0}

'''
We go over city dictionary again and fill in the zip code and lat/long values.
Some cities don't have any lat/long data, so we have to use try/exception to
skip over any errors. The counter is just to see how far the progam is going.
There are 15706 city pages.
'''
counter = 0 
for k in city_dict.keys():
    #this part fills in the zipcode
    zipurl = city_dict[k]['url']
    ziprequest=urllib.request.Request(zipurl,None,headers)
    zipresponse = urllib.request.urlopen(ziprequest)
    zipdata = zipresponse.read()
    zipsoup = BeautifulSoup(zipdata, "lxml")
    print(zipurl)
    
    '''
    the part between the ' '  is the regular expressions search. From the 
    whole zipstring, we go to the h1 section, then look for the 2nd instance
    of 'strong' after that:
        zipstring = <strong>Postal Code 4644</strong>
    '''
    zipstring = str(zipsoup.find('h1').find_next('strong').find_next('strong'))
    
    #To get zipcode from zipstring, we match only the numbers in the string
    zipcode = re.findall('[0-9]+.+[0-9]', zipstring)
    
    #this part fills in the lat/long
    script = zipsoup.find_all('script')
    counter = counter+1
    print(counter)
    tempstring = str(script[1])
    templist = re.findall('\(.[0-9]+.+[0-9]\)',tempstring)
    try:
        latitude = float(re.split(",",templist[0])[0].strip("()"))
        longitude = float(re.split(",",templist[0])[1].strip("()"))
    except:
        pass
    
    city_dict[k]['zipcode']=zipcode
    city_dict[k]['lat']=latitude
    city_dict[k]['long']=longitude
    