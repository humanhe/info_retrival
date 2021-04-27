from elasticsearch import Elasticsearch


class send_data:

    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

    def read_from_file(self, text_file):
        # counter = 0

        with open(text_file, 'r') as file_read:
            next(file_read)

            while True:
                line = file_read.readline()
                # line = line.strip('\n')
                record = line.split('###')
                # print(record)

                self.send_to_index(record)

                # if not line or counter == 5:
                #     break
                # counter += 1
                if not line:
                    break

    def send_to_index(self,a_webpage):

        webpage_id = int(a_webpage[1])
        img_link = a_webpage[2]
        web_link = a_webpage[3]
        webpage_title = a_webpage[4]
        web_content = a_webpage[5]

        # print(webpage_id,'\t', img_link,'\t', web_link,'\t', webpage_title)
        if not self.es.exists(index="final_kellyhe", id=webpage_id):
            doc = {'title': webpage_title, 'content': web_content, 'image': img_link, 'link':web_link}
            self.es.index(index='final_kellyhe', id=webpage_id, body=doc)
            print('\tSuccess! ID is:  ', webpage_id)
        else:
            print('Duplicate webpage id exist! ID is: ', webpage_id, webpage_title, web_link)
            exit()
        # if not self.es.exists(index="test_kellyhe", id=webpage_id):
        #     doc = {'title': webpage_title, 'content': web_content, 'image': img_link, 'link':web_link}
        #     self.es.index(index='test_kellyhe', id=webpage_id, body=doc)
        #     print('\tSuccess! ID is:  ', webpage_id)
        # else:
        #     print('Duplicate webpage id exist! ID is: ', webpage_id)
        #     exit()

    def delete_an_index(self, index_name):

        if self.es.indices.exists(index= index_name):
            print('index name exists!')
            self.es.indices.delete(index=index_name)
            print('index deleted!')
        else:
            print('index name NOT exists!')








obj = send_data()
# obj.delete_an_index('test_kellyhe')
# obj.read_from_file('datafile8054.txt')

