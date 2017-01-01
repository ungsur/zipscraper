# -*- coding: utf-8 -*-
#Regular expressions library is used for pattern matching
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


