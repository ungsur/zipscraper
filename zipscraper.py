# -*- coding: utf-8 -*-
#Regular expressions library is used for pattern matching
import re
import urllib

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 
url = "http://www.codigopostalde.com.ar/buenos-aires/20-de-junio/calle-casacuberta/00000002-00000100/"
#url = ''
request=urllib.request.Request(url,None,headers)
response = urllib.request.urlopen(request)
data = response.read()

from bs4 import BeautifulSoup
soup = BeautifulSoup(data, "lxml")

#this returns all of the parts of the page as soup elements
data=soup.find_all()

#this returns a list of the parts of the page which start the the part <script>
script = soup.find_all('script')

#turn the 3rd element on the page to one long string
tempstring = str(script[3])

#grab the part of the strings that starts with a ( has some numbers inbetween and ends with a )
#['(-34.7736969, -58.7326622)', '(-34.7736969, -58.7326622)', '(-34.7736969, -58.7326622)']
templist = re.findall('\(.[0-9]+.+[0-9]\)',tempstring)

#grab the first pair of coordinates and cut out the parentheses parts with .strip
latitude = float(re.split(",",templist[0])[0].strip("()"))
longitude = float(re.split(",",templist[0])[1].strip("()"))


url1 = 'http://www.codigopostalde.com.ar/en/'
request1 =  urllib.request.Request(url1,None,headers)
response1 =  urllib.request.urlopen(request1)
data = response1.read()

soup = BeautifulSoup(data, "lxml")
print(soup.prettify())
urllist = soup.find('h3').find_next('ul')


states_dict = {}
for link in soup.find('h3').find_next('ul').find_all("a"):
    print(link.text, link.get("href"))
    states_dict[link.text] = str(link.get("href"))
    
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


counter = 0 
for k in city_dict.keys():
    zipurl = city_dict[k]['url']
    ziprequest=urllib.request.Request(zipurl,None,headers)
    zipresponse = urllib.request.urlopen(ziprequest)
    zipdata = zipresponse.read()
    zipsoup = BeautifulSoup(zipdata, "lxml")
    print(zipurl)
    zipstring = str(zipsoup.find('h1').find_next('strong').find_next('strong'))
    zipcode = re.findall('[0-9]+.+[0-9]', zipstring)
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
    