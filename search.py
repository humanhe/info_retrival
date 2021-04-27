from elasticsearch import Elasticsearch
import  string
from spellchecker import SpellChecker
import urllib
import os
from PIL import Image

"""
Aims to retrieve search result from the user query. It will also check for duplicate web links
to avoid seeing the same webpage more than once. The user query is being pre-processed before 
sending over to ElasticSearch for search functionality.

"""
class get_search_result():

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        self.iterate_image = 1
        self.check_duplicates = {}

    """
    Returns search results of the user query
    """
    def search(self, query, num_of_post = 50):

        #Spell Checking
        query_list = query.split(' ')

        spell = SpellChecker()

        updated_query_list = []

        for word in query_list:
            updated_query_list.append(spell.correction(word))

        updated_query = " ".join(updated_query_list)

        # Text Pre-processing
        updated_query = updated_query.lower()
        updated_query = updated_query.replace('-', ' ')
        updated_query = updated_query.replace('\n', ' ')
        updated_query = updated_query.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))



        final_result_2 = []
        results_2 = self.es.search(index="final_kellyhe", body= {

              "query": {
                "simple_query_string" : {
                    "fields": ["title^5", 'content^3'],
                    "query": updated_query
                }
              }


        },  size = num_of_post)


        for i in range(len(results_2['hits']['hits'])):
            a_doc = results_2['hits']['hits'][i]

            #Check duplicates
            web_title = a_doc['_source']['title']
            if web_title in self.check_duplicates.keys() and a_doc['_source']['link'] == self.check_duplicates[web_title]:
                print("Duplication! Web page title is: ", web_title, " Link is: ", a_doc['_source']['link'])

            else:
                self.check_duplicates[web_title] = a_doc['_source']['link']

                description = self.short_description(a_doc['_source']['content'])
                description = '...' + description + '...'

                update_image_path = self.image_link_preprocessing(a_doc['_source']['image'])

                final_result_2.append([a_doc['_id'], web_title, update_image_path, a_doc['_source']['link'], description])

        return final_result_2, updated_query



    def image_link_preprocessing(self, img_link):

        my_path = '/Users/humanuk/ir_final_project/static/images/'
        pic_name = os.path.basename(img_link)

        pic_name = pic_name.replace('%', '-')

        image_path = os.path.join(my_path, pic_name)
        new_path = ''
        updated_image_path = ''
        if not os.path.isfile(image_path):
            print("image file not exists. Image name is: ", pic_name)

            # pic_name = os.path.basename(img_link)
            if self.iterate_image > 15:
                self.iterate_image = 1

            pic_name = str(self.iterate_image) + '.jpeg'
            self.iterate_image += 1
            new_path = '/static/download_images/'

        else:
            new_path = '/static/images/'

        updated_image_path = os.path.join(new_path, pic_name)

        if not updated_image_path:
            print("updated_image_path is EMPTY!")

        return updated_image_path


    def short_description(self, text):
        web_content_list = text.split()

        description = []

        if len(web_content_list) > 122:
            for i in range(90,121):
                description.append(web_content_list[i])



        return ' '.join(description)


# #For testing purposes
# obj2 = get_search_result()
# data1 = obj2.search("shepherd's")
# print(data1)
