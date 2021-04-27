import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer



# url = 'https://foodgawker.com/page/2/'

url = 'https://foodgawker.com/page/5/'
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

request=urllib.request.Request(url,None, header) #The assembled request
response = urllib.request.urlopen(request)


# soup = BeautifulSoup(response, 'html.parser')
# images = soup.find_all('img')
#
# for item in images:
#     print(item['src'])

#works
for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
    if link.has_attr('href'):
        print(link['href'])




#
# for a in soup.find_all('a', href=True):
#     print(a['href'])