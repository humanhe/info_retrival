from elasticsearch import Elasticsearch
import  string
from spellchecker import SpellChecker
import urllib
import os
from PIL import Image


class front_page:

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        self.check_duplicate_web_link = set()
        self.data_info = {}


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
                # self.data_info[a_doc['_id']] = a_doc['_source']['image']
                # print(a_doc['_source']['link'])
                # print("a_doc['_source']['content']", a_doc['_source']['content'])

                # image_link = a_doc['_source']['image']
                # with open('all_image_links.txt', 'a') as storage:
                #     storage.write(f'\n{image_link}')

                description = self.short_description(a_doc['_source']['content'])
                # print('description', description, '\n')
                temp_store = [str(a_doc['_id']),a_doc['_source']['title'], description, a_doc['_source']['image'], a_doc['_source']['link']]
                temp_store_str = '###'.join(temp_store)
                with open('home_page_display.txt', 'a') as storage1:
                    storage1.write(f'\n{temp_store_str}')



    def short_description(self, text):
        web_content_list = text.split()

        description = []
        for i in range(90,121):
            description.append(web_content_list[i])



        return ' '.join(description)


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

                    # if int(webpage_id) != 2759:
                    web_link = web_link.replace('\n', '')
                    webpage_description = '...' + webpage_description + '...'
                    # img_link = 'https://pacificpotluck.com/wp-content/uploads/2020/12/Garlic-sesame-spinach-300x300.jpg'

                    #Check if image file exists
                    my_path = '/Users/humanuk/ir_final_project/static/images/'
                    pic_name = os.path.basename(img_link)

                    pic_name = pic_name.replace("%", "-")

                    image_path = os.path.join(my_path, pic_name)
                    new_path = ''
                    updated_image_path = ''
                    if not os.path.isfile(image_path):
                        print("image file not exists. Image name is: ", pic_name)

                        # pic_name = os.path.basename(img_link)
                        if iterate_image > 15:
                            iterate_image = 1

                        pic_name = str(iterate_image) + '.jpeg'
                        iterate_image += 1
                        new_path = '/static/download_images/'
                        # updated_image_path = os.path.join(new_path, pic_name)
                    else:
                        new_path = '/static/images/'



                    updated_image_path = os.path.join(new_path, pic_name)

                    if not updated_image_path:
                        print("updated_image_path is EMPTY!")

                    final_home_result.append([webpage_id,webpage_title, updated_image_path, web_link, webpage_description])

                    count += 1

                if not line:
                    break

            # print(final_home_result[95:])
            return final_home_result

                # if not line or counter == 5:
                #     break
                # counter += 1






    # def save_local(self):
    #
    #
    #     for info in data1:
    #         request = urllib.request.Request(info[2], None, headers)
    #         response = urllib.request.urlopen(request)
    #
    #         image = Image.open(response)
    #         pic_name = info[0] + '-' + os.path.basename(info[2])
    #         # image_path = os.path.join(my_path, os.path.basename(info[1]))
    #         image_path = os.path.join(my_path, pic_name)
    #         image.save(image_path)

# obj = front_page()
# # # obj.get_image_link() #write 100 image links to file
# obj.get_home_page_display_data()

# name = '/Users/humanuk/ir_final_project/static/images/apple-2Bpie-2Bpuffs-2B&25284&2529.jpg'
# print(os.path.isfile(name))