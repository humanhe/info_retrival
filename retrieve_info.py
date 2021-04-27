import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import string
import urllib3
# from BeautifulSoup import BeautifulSoup
import requests
from urllib.error import HTTPError
import re
import ssl
import certifi


# url = 'https://foodgawker.com/'
#
# header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#        'Accept-Encoding': 'none',
#        'Accept-Language': 'en-US,en;q=0.8',
#        'Connection': 'keep-alive'}
#
# request=urllib.request.Request(url,None, header) #The assembled request
# response = urllib.request.urlopen(request)
#
#
# get_tot_page_num = requests.get(url)
# soup = BeautifulSoup(get_tot_page_num.text, 'html.parser')
#
# # soup = BeautifulSoup(response, 'html.parser') #Doesnot work! Dont know why i cant call Beautifulsoup twice
# tot_page_num = soup.find('div', {'class':"post-section"}).get('data-maxpage')
# print(tot_page_num)
#
# #works both ways
# for link in BeautifulSoup(get_tot_page_num.text, "html.parser", parse_only=SoupStrainer('a')):
#     print("HHHHHH   ",link)
#     if link.has_attr('href'):
#         print(link['href'])
#
# #only works if we dont cant call Beautifulsoup constructor twice
# # for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
# #     print("HHHHHH   ",link)
# #     if link.has_attr('href'):
# #         print(link['href'])


class get_data:

    def __init__(self):
        self.url = 'https://foodgawker.com/'
        self.tot_page = self.get_tot_page_num()
        # self.counter = 948
        self.webpage_id = 8054
        self.all_webpages_index = []
        self.all_webpages_extra_info = {}
        self.check_duplicate_link = set()


    def get_tot_page_num(self):

        tot_page_url = requests.get(self.url)
        soup = BeautifulSoup(tot_page_url.text, 'html.parser')
        tot_page_num = soup.find('div', {'class':"post-section"}).get('data-maxpage')
        print(tot_page_num)
        return int(tot_page_num)

    def get_website_data(self):

        # for page in range(3398, self.tot_page):
        for page in range(491, 611):
            # self.counter += 1
        # for page in range(1):
            url = 'https://foodgawker.com/page/' + str(page) + '/'
            page_url = requests.get(url)
            for link in BeautifulSoup(page_url.text, "html.parser", parse_only=SoupStrainer('a')):
                # print("HHHHHH   ", link)
                if link.has_attr('href') and link['href'].startswith('https://track') and 'translate' not in link['href']:
                    # print(link['href'])
                    links = link['href'].splitlines()
                    # print('page is: ', page)
                    # print('\t',links)

                    self.get_body_text(links, page)

        print('Finish and display part of the results')
        # print(self.all_webpages_extra_info[:50])




    def get_body_text(self, links, webpage_num):


        for a_link in links:

            #To count how many links
            # print(self.counter, '    ', a_link)

            #Found an error link on original foodgawker website
            if a_link == 'https://track.foodgawker.com/3707188/https://abiggreenhouse.com/crispy-rice-oatmeal-butterscotch-chocolate-chip-cookies/q':
                a_link = 'https://track.foodgawker.com/3707188/https://abiggreenhouse.com/crispy-rice-oatmeal-butterscotch-chocolate-chip-cookies/'



            #check duplicate links
            if a_link not in self.check_duplicate_link:

                self.check_duplicate_link.add(a_link)

                #link processing
                dash_times = 0
                stop_place = 0
                # for c in reversed(url):
                # print(len(a_link))

                # if a_link[len(a_link)-1] != '/':
                #     dash_times = 1
                # for i in range(len(a_link)-1, -1, -1):
                #     if dash_times > 1:
                #         stop_place = i + 2
                #         break
                #     # print(i, a_link[i])
                #     if a_link[i] == '/':
                #         dash_times += 1
                #
                # web_title = a_link[stop_place:-1]
                # web_title = web_title.replace('-', ' ')
                # print('     1  ',web_title)
                #
                # #1)if it contains other punctuation other than hyphen, it is not a real food name
                # if any(p in web_title for p in string.punctuation):

                    #2) get text in the link

                web_title = ''
                final_soup = None

                try:
                    temp_soup = BeautifulSoup(requests.get(a_link).text, 'html.parser')

                    title = temp_soup.title.get_text()
                    web_title = title
                    # print(web_title)
                    # print('2    ',title)
                    final_soup = temp_soup
                    # print('         CHECK', title == '403 Forbidden')

                    # 3) if still cannot access
                    if web_title == 'Not Acceptable!' or web_title == '403 Forbidden':

                        header = {'User-Agent': 'XYZ/3.0'}
                        request = urllib.request.Request(a_link, None, header)  # The assembled request
                        response = urllib.request.urlopen(request)
                        soup_1 = BeautifulSoup(response, 'html.parser')
                        title = soup_1.title.get_text()
                        web_title = title
                        final_soup = soup_1
                        # print('3    ', title)

                except AttributeError as e:
                    web_title = 'skip'
                    pass
                except requests.exceptions.ConnectionError as e:
                    web_title = 'skip'
                    pass
                except HTTPError as e:
                    web_title = 'skip'
                    # link_ending = 'now it is done'
                    pass
                except UnicodeEncodeError as e:
                    web_title = 'skip'
                    pass
                except requests.exceptions.TooManyRedirects as e:
                    web_title = 'skip'
                    pass


                #     print('in try', link_ending)
                # print('out try', link_ending)

                # print('web title', web_title)

                #We get image links and body text here

                if web_title != 'skip' and len(web_title) > 1 and final_soup:
                    images = final_soup.find_all('img', {"src":True})

                    updated_web_title = self.text_preprocessing(web_title)
                    max_score = -1.0
                    desire_image_link = ''
                    handle_bad_case_link = ''
                    img_link = ''

                    #Retrieve desire image link in a webpage
                    for item in images:

                        image_data = item['src']
                        try:

                            img_link = re.search("(?P<url>https?://[^\s]+)", image_data).group("url")
                            check_img_link = img_link.lower()

                            social_media_list = ['facebook', 'twitter', 'pinterest', 'instagram']
                            if not any(social_media in check_img_link for social_media in social_media_list):

                                if_valid = False
                                try:
                                    # header = {'User-Agent': 'XYZ/3.0'}
                                    # header = {
                                    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                    #            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                    #            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                                    #            'Accept-Encoding': 'none',
                                    #            'Accept-Language': 'en-US,en;q=0.8',
                                    #            'Connection': 'keep-alive'}
                                    # request = urllib.request.Request(img_link, None, header)  # The assembled request
                                    # response = urllib.request.urlopen(request) #, context=ssl.create_default_context(cafile=certifi.where())
                                    # soup_img = BeautifulSoup(response, 'html.parser', from_encoding="iso-8859-1")
                                    # soup_img = BeautifulSoup(response, 'html.parser')
                                    # temp = soup_img.get_text()
                                    # htmldata = urlopen(img_link)
                                    # soup_img = BeautifulSoup(htmldata, 'html.parser', from_encoding="iso-8859-1")
                                    # temp = soup_img.get_text()

                                    # temp_soup = BeautifulSoup(requests.get(a_link).text, 'html.parser')
                                    # title = temp_soup.get_text()

                                    page = requests.get(img_link)

                                    image_formats = ("image/png", "image/jpeg", "image/jpg")
                                    r = requests.head(img_link)

                                    if r.headers["content-type"] in image_formats and img_link.endswith(('.jpg', '.png', '.jpeg')):
                                        if_valid = True
                                    else:
                                        if_valid = False


                                except Exception as e:
                                    print("img link error!!!! ", img_link)
                                    if_valid = False
                                    pass
                                # except AttributeError as e:
                                #     if_valid = False
                                #     pass
                                # except requests.exceptions.ConnectionError as e:
                                #     if_valid = False
                                #     pass
                                # except HTTPError as e:
                                #     if_valid = False
                                #     # link_ending = 'now it is done'
                                #     pass
                                # except UnicodeEncodeError as e:
                                #     if_valid = False
                                #     pass
                                # except requests.exceptions.TooManyRedirects as e:
                                #     if_valid = False
                                #     pass

                                # handle_bad_case_link = img_link
                                if if_valid:
                                    #get info in image link
                                    stop_place = 0
                                    for i in range(len(img_link) - 1, -1, -1):
                                        if dash_times > 1:
                                            stop_place = i + 2
                                            break
                                        # print(i, a_link[i])
                                        if img_link[i] == '/':
                                            stop_place = i + 1
                                            break
                                    img_info = img_link[stop_place:]
                                    updated_img_info = self.text_preprocessing(img_info)
                                    # print('updated_img_info:    ',updated_img_info, '   ', img_link)

                                    score = self.compare_web_title_image(updated_web_title, updated_img_info)
                                    # print(score, '\t\t', img_link)

                                    if score > max_score:
                                        max_score = score
                                        desire_image_link = img_link



                        except AttributeError:
                            pass
                        except urllib.error.URLError:
                            print("url error!!!!!  ", img_link)
                            pass

                    #Retrieve body text
                    # print('final soup is none?', final_soup==None)
                    body_text = ''
                    try:
                        body_text = final_soup.body.get_text()
                    except AttributeError:
                        pass

                    if body_text and desire_image_link:


                        updated_body_text = self.text_preprocessing(body_text)

                        print("     Successful image link:  ", desire_image_link)

                        #For storing into a textfile
                        temp_store = [str(webpage_num), str(self.webpage_id), desire_image_link, a_link, updated_web_title, updated_body_text]
                        temp_store_str = '###'.join(temp_store)
                        with open('datafile8054.txt', 'a') as storage:

                            storage.write(f'\n{temp_store_str}')


                        #For indexing
                        # a_webpage_dict = {}
                        # a_webpage_dict[self.webpage_id] = updated_body_text + ' ' + updated_web_title


                        #store into self.all_webpages_index variable
                        # self.all_webpages_index.append(a_webpage_dict)

                        #For storage of web title(or description) and image link
                        # self.all_webpages_extra_info[self.webpage_id] = [web_title, img_link, a_link, webpage_num]

                        #Update webpage id
                        # print('webpage id', self.webpage_id)
                        self.webpage_id += 1
                    elif not body_text:
                        print("Body text is EMPTY!! Link is: ", a_link)

                    elif not img_link:
                        print("Image link is EMPTY!! Link is: ", a_link)












                    # print(image_link)
            #     self.get_website_image(a_link, web_title)

    def text_preprocessing(self, text):

        text = text.lower()
        text = text.replace('-', ' ')
        text = text.replace('\n', ' ')

        update_text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

        update_text = " ".join(update_text.split())

        return update_text

    def compare_web_title_image(self, web, image):

        web_list = []
        image_list = []

        for word in web.split():
            web_list.append(word)

        for word in image.split():
            image_list.append(word)


        count = 0.0
        for word in image_list:
            if word in web_list:
                count += 1

        return count/len(web_list)



            #*************
            # header = {'User-Agent': 'XYZ/3.0'}
            # # urltemp = 'https://goodbalancedfood.com/en/red-rice-salad/'
            # request = urllib.request.Request(a_link, None, header)  # The assembled request
            # # response = urllib.request.urlopen(request)
            #
            # try:
            #     response = urllib.request.urlopen(request)
            #     soup_temp = BeautifulSoup(response, 'html.parser')
            #     title = soup_temp.title.get_text()
            #     print(title)
            # except HTTPError as e:
            #     content = e.read()
            #     print("\tContent    ", content)

        # header = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #     'Accept-Encoding': 'none',
        #     'Accept-Language': 'en-US,en;q=0.8',
        #     'Connection': 'keep-alive'}


        # urltemp = 'https://goodbalancedfood.com/en/red-rice-salad/'
        # temp_soup = BeautifulSoup(requests.get(urltemp).text, 'html.parser')




obj = get_data()
obj.get_website_data()
