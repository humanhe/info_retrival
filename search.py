from elasticsearch import Elasticsearch
import  string
from spellchecker import SpellChecker
import urllib
import os
from PIL import Image


class get_search_result():

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        self.iterate_image = 1
        self.check_duplicates = {}


    def search(self, query, num_of_post = 50):

        #Text Pre-processing
        # query = query.lower()
        # query = query.replace("'", ' ')
        # query = query.replace('-', ' ')
        # query = query.replace('\n', ' ')
        # query = query.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
        # query = " ".join(query.split())

        print('query ',query)



        #Spell Checking
        query_list = query.split(' ')
        # print('updated_query_list', query_list)
        spell = SpellChecker()
        # misspelled = spell.unknown(query_list)
        updated_query_list = []

        for word in query_list:
            updated_query_list.append(spell.correction(word))

        updated_query = " ".join(updated_query_list)

        print("updated_query spell checker", updated_query)

        updated_query = updated_query.lower()
        updated_query = updated_query.replace('-', ' ')
        updated_query = updated_query.replace('\n', ' ')
        updated_query = updated_query.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
        print("updated_query ",updated_query )
        # print('updated_query ',updated_query)



        # final_result = []
        # results = self.es.search(index="final_kellyhe", body={
        #
        #     "query": {
        #         "query_string": {
        #             "fields": ["title^5", 'content^4'],
        #             "query": updated_query
        #         }
        #     }
        #
        # },  size = 100)
        #
        # for i in range(len(results['hits']['hits'])):
        #     a_doc = results['hits']['hits'][i]
        #     final_result.append([a_doc['_id'], a_doc['_source']['title'], a_doc['_score']])
        # print("query_string result is:\t")
        # # print(results)
        # print(final_result)
        # print('result num ',len(final_result))

        # work
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
            # final_result_2.append([a_doc['_id'], a_doc['_source']['title'], a_doc['_score'], a_doc['_source']['image'], a_doc['_source']['link']])
        # print("simple_query_string result is:\t")
        # print(results)
        # print(final_result_2)
        # print('result num ',len(final_result_2), len(final_result_2[0]))

        return final_result_2, updated_query
        # final_result_1 = []
        # results_1 = self.es.search(index="final_kellyhe", body={
        #
        #     "query": {
        #         "multi_match": {
        #             "fields": ["title^5", 'content^4'],
        #             "query": updated_query
        #         }
        #     }
        #
        # },  size = 100)
        #
        #
        # for i in range(len(results_1['hits']['hits'])):
        #     a_doc = results_1['hits']['hits'][i]
        #     final_result_1.append([a_doc['_id'], a_doc['_source']['title'], a_doc['_score']])
        # print("multi_match result is:\t")
        # # print(results)
        # print(final_result_1)
        # print('result num ',len(final_result_1))


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
            # updated_image_path = os.path.join(new_path, pic_name)
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


# #
# obj2 = get_search_result()
# data1 = obj2.search("shepherd's")
# print(data1)



#works!
# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
# headers={'User-Agent':user_agent}
# my_path = '/Users/humanuk/Desktop/for_test/'
# for info in data1:
#     request=urllib.request.Request(info[2] ,None,headers)
#     response = urllib.request.urlopen(request)
#
#     image=Image.open(response)
#     pic_name =  info[0] + '-' + os.path.basename(info[2])
#     # image_path = os.path.join(my_path, os.path.basename(info[1]))
#     image_path = os.path.join(my_path, pic_name)
#     image.save(image_path)

#In table.html
# <td class="table__cell">{{ row[4] | urlize(40, true) }}</td>