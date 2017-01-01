# -*- coding: utf-8 -*-
import re
import urllib

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 
url = "http://www.codigopostalde.com.ar/buenos-aires/20-de-junio/calle-casacuberta/00000002-00000100/"

request=urllib.request.Request(url,None,headers)
response = urllib.request.urlopen(request)
data = response.read()

from bs4 import BeautifulSoup
soup = BeautifulSoup(data, "lxml")
data=soup.find_all()


script = soup.find_all('script')
tempstring = str(script[3])
templist = re.findall('\(.[0-9]+.+[0-9]\)',tempstring)

latitude = float(re.split(",",templist[0])[0].strip("()"))
longitude = float(re.split(",",templist[0])[1].strip("()"))


