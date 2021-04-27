import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import string
import xml.etree.ElementTree
import urllib3
# from BeautifulSoup import BeautifulSoup
import requests
import re
from urllib.error import HTTPError



# or if you're using BeautifulSoup4:
# from bs4 import BeautifulSoup
# url = 'https://foodgawker.com/'
# url = 'https://borrowedbites.com/blackberry-cheesecake/'
# url = 'https://goodbalancedfood.com/en/red-rice-salad/'
# url = 'https://adoringkitchen.com/2021/03/quinoa-salmon-bowl-lemon-vinaigrette.html'
# url = 'https://track.foodgawker.com/3695138/http://myperfectgreens.com/recipe/raspberry-baked-oats/?preview_id=2409&preview_nonce=f7845b31d8&preview=true&_thumbnail_id=2410'
# url = 'https://spicechronicles.com/chocolate-chip-banana-bread/#sthash.byFnDYB9.dpbs'
# url = 'https://inquiringchef.com/soft-cut-out-sugar-cookies/'
# url = 'https://www.familyfreshmeals.com/2021/03/buttermilk-glazed-donut-bundt-cake.html'
# url = "http://www.w3.org/2000/svg'%20viewBox='0%200%20767%20367'%3E%3C/svg%3E"
url = ' https://somethingaboutsandwiches.com/wp-content/uploads/2020/07/footer2.png'
# url = 'https://secure.gravatar.com/avatar/1dc64346865a28682283f9e9ce476fd7?s=125&d=mm&r=g'
# htmldata = urlopen(url)
# soup = BeautifulSoup(htmldata, 'html.parser')
# # images = soup.find_all('img')
# print(soup.get_text())
# image_formats = ("image/png", "image/jpeg", "image/jpg")
# r = requests.head(url)
# print(r.headers)
# print(r.headers["content-type"] in image_formats)

print(url.endswith(('.jpg', '.png')))
# for item in images:
#     print(item['src'])

# header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#        'Accept-Encoding': 'none',
#        'Accept-Language': 'en-US,en;q=0.8',
#        'Connection': 'keep-alive'}
#
# request=urllib.request.Request(url,None, header) #The assembled request
# response = urllib.request.urlopen(request)


# data = response.read() # The data u need
# print(data)

# soup = BeautifulSoup(response, 'html.parser')



# review = []
# for i in soup.find_all('div', {'class':'comment-content'}):
#     per_review = i.find('p')
#     review.append(per_review)
#
# print('review', len(review))
#
# body_text = soup.body.get_text()
# title_text = soup.title.get_text()
# def text_process(text):
#     text = text.lower()
#
#     text = text.replace('-', ' ')
#     text = text.replace('\n', ' ')
#
#
#     ## Remove words with apostrophes
#     for word in text.split():
#         if "'" in word:
#             text = text.replace(word, '')
#         # if word in self.stop_list:
#         #     temp = temp.replace(word, '')
#
#     ##Remove all punctuations
#     text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
#     return text
#
# updated_body_text = text_process(body_text)
# updated_title_text = text_process(title_text)
#
# h2_tag = []
# for i in soup.find_all('h2'):
#     h2_tag.append(i.get_text())
#
# print('h2_tag'  ,h2_tag)

L = ["This is China", "This is Paris", "This is London"]
l_connect = '##'.join(L)
print(l_connect)

# append to a file
# with open('testfile.txt','a') as file1:
#     for i in range(5):
#
#         file1.write(f'\n{str(i) + l_connect}')


# read from a file
with open('datafile.txt','r') as file_read:
    next(file_read)
    while True:
        line = file_read.readline()
        # line = line.strip('\n')
        text = line.split('###')

        if not line:
            break
        print(text)



# filetemp = open('testfile.txt', 'w')
# L = ["This is China \n", "This is Paris \n", "This is London"]
# filetemp.writelines(L)
# filetemp.close()

# print(updated_body_text,'\n\n')
# print(updated_title_text)


# images = soup.find_all('img')

# for item in images:
#     print(item['src'])
# text = soup.get_text()
# print(str(text))
# print(soup.title)
# title = soup.title.get_text()
# print(title)
# body = soup.body.get_text()
# print(body)
dash_times = 0
stop_place = 0
# for c in reversed(url):
print(len(url))

# try:
#     temp_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
#     title = temp_soup.title.get_text()
#     print('2    ', title)
#
#     if title == 'Not Acceptable!':
#         # header = {
#         #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#         #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         #         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#         #         'Accept-Encoding': 'none',
#         #         'Accept-Language': 'en-US,en;q=0.8',
#         #         'Connection': 'keep-alive'}
#         header = {'User-Agent': 'XYZ/3.0'}
#         request = urllib.request.Request(a_link, None, header)  # The assembled request
#         response = urllib.request.urlopen(request)
#         soup_1 = BeautifulSoup(response, 'html.parser')
#         title = soup_1.title.get_text()
#         print('              3    ', title)
# except AttributeError as e:
#     pass



# title = soup_1.title.get_text()
# print('3    ',title)
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
# page_num = soup.find('div', {'class':"post-section"}).get('data-maxpage')
# print(page_num)
#
# #works
# for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
#     print("HHHHHH   ",link)
#     if link.has_attr('href'):
#         print(link['href'])


#In retrieve info
# header = {
#         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#         'Accept-Encoding': 'none',
#         'Accept-Language': 'en-US,en;q=0.8',
#         'Connection': 'keep-alive'}


# img_link= 'https://choosingchia.com/jessh-jessh/uploads/2018/11/weeknight-slow-cooker-lentil-soup-2-1-of-1-150x150.jpg'
# stop_place = 0
#
# for i in range(len(img_link) - 1, -1, -1):
#     if dash_times > 1:
#         stop_place = i + 2
#         break
#     # print(i, a_link[i])
#     if img_link[i] == '/':
#         stop_place = i + 1
#         break
# img_info = img_link[stop_place:-4]
# print(img_info)



