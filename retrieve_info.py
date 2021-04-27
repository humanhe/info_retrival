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

"""
This class is for crawling data and saving them into local files.
"""
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

    """
    Gets proper links of a webpage
    """
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



    """
    Gets body text from the web which also includes 
    retriving desire image links.
    """
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

                #1) get text in the link

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

                        self.webpage_id += 1
                    elif not body_text:
                        print("Body text is EMPTY!! Link is: ", a_link)

                    elif not img_link:
                        print("Image link is EMPTY!! Link is: ", a_link)


    """
    Gets rid of unwanted punctuation
    """
    def text_preprocessing(self, text):

        text = text.lower()
        text = text.replace('-', ' ')
        text = text.replace('\n', ' ')

        update_text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

        update_text = " ".join(update_text.split())

        return update_text

    """
    Retrieve desire image links first attempt
    """
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



#For testing purpose
# obj = get_data()
# obj.get_website_data()
