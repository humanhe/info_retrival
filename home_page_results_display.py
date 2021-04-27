from elasticsearch import Elasticsearch
import  string
from spellchecker import SpellChecker
import urllib
import os
from PIL import Image

"""
This is designed for displaying data on home page. 
"""
class front_page:

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        self.check_duplicate_web_link = set()
        self.data_info = {}

    """
    Gets image links and saves them to local files. It makes the whole process easier
    in the way that we can track the process just by taking a lot at the local files 
    instead of having to run it every time.
    """
    def get_image_link(self):

        all_result = self.es.search(index="final_kellyhe", body={

            "query": {
                "match_all": {}
            }

        }, size=100)

        for i in range(len(all_result['hits']['hits'])):
            a_doc = all_result['hits']['hits'][i]
            # final_result_2.append([a_doc['_id'], a_doc['_source']['title'], a_doc['_source']['image'], a_doc['_source']['link']])
            if a_doc['_source']['link'] not in self.check_duplicate_web_link:
                self.check_duplicate_web_link.add(a_doc['_source']['link'])

                description = self.short_description(a_doc['_source']['content'])
                # print('description', description, '\n')
                temp_store = [str(a_doc['_id']),a_doc['_source']['title'], description, a_doc['_source']['image'], a_doc['_source']['link']]
                temp_store_str = '###'.join(temp_store)
                with open('home_page_display.txt', 'a') as storage1:
                    storage1.write(f'\n{temp_store_str}')


    """
    Retrieves a small part of body text for short description.
    """
    def short_description(self, text):
        web_content_list = text.split()

        description = []
        for i in range(90,121):
            description.append(web_content_list[i])



        return ' '.join(description)

    """
    This is only responsible for sending data over to the front end.
    """
    def get_home_page_display_data(self, home_page_data_file = 'home_page_display.txt'):

        final_home_result = []
        count = 0
        iterate_image = 1
        with open(home_page_data_file, 'r') as file_read:
            next(file_read)

            while True:
                line = file_read.readline()
                # line = line.strip('\n')
                record = line.split('###')
                # print(record)
                if count % 100 == 0:
                    print("Progress: ", count)

                if len(record) > 1:


                    webpage_id = record[0]
                    webpage_title = record[1]
                    webpage_description = record[2]
                    img_link = record[3]
                    web_link = record[4]

                    web_link = web_link.replace('\n', '')
                    webpage_description = '...' + webpage_description + '...'


                    #Check if image file exists
                    my_path = '/Users/humanuk/ir_final_project/static/images/'
                    pic_name = os.path.basename(img_link)

                    pic_name = pic_name.replace("%", "-")

                    image_path = os.path.join(my_path, pic_name)
                    new_path = ''
                    updated_image_path = ''
                    if not os.path.isfile(image_path):
                        print("image file not exists. Image name is: ", pic_name)


                        if iterate_image > 15:
                            iterate_image = 1

                        pic_name = str(iterate_image) + '.jpeg'
                        iterate_image += 1
                        new_path = '/static/download_images/'

                    else:
                        new_path = '/static/images/'



                    updated_image_path = os.path.join(new_path, pic_name)

                    if not updated_image_path:
                        print("updated_image_path is EMPTY!")

                    final_home_result.append([webpage_id,webpage_title, updated_image_path, web_link, webpage_description])

                    count += 1

                if not line:
                    break

            return final_home_result

#For testing purposes
# obj = front_page()
# # # obj.get_image_link() #write 100 image links to file
# obj.get_home_page_display_data()
