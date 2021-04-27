import string
import urllib.request
from PIL import Image
import os

class download_image:

    def __init__(self):
        self.check_duplicate_image_link = set()
        self.check_duplicate_web_link = set()


    def read_from_txt(self, text_file):

        with open(text_file, 'r') as file_read:
            next(file_read)

            while True:
                line = file_read.readline()
                # line = line.strip('\n')
                record = line.split('###')
                # print(record)

                if len(record) > 1:
                    webpage_id = str(record[1])
                    img_link = record[2]
                    web_link = record[3]
                    webpage_title = record[4]
                    # web_content = record[5]

                    img_link_stop_place = self.stop_place(img_link, False)
                    updated_img_link = self.text_preprocessing(img_link[img_link_stop_place:])

                    # print(web_link)
                    web_link_stop_place = self.stop_place(web_link, True)
                    # print('web_link_stop_place', web_link_stop_place)
                    updated_web_link = self.text_preprocessing(web_link[web_link_stop_place:])

                    # print('updated_img_link', updated_img_link, ' updated_web_link', updated_web_link)
                    score = self.compare_web_title_image(updated_web_link, updated_img_link)

                    if score > 0:
                        if img_link not in self.check_duplicate_image_link:
                            self.check_duplicate_image_link.add(img_link)

                            # self.send_to_index(record)
                            temp_store = [webpage_id, img_link, webpage_title, web_link]
                            temp_store_str = '###'.join(temp_store)

                            with open('all_image_links.txt', 'a') as storage:
                                storage.write(f'\n{temp_store_str}')

                            # print("\tOK! ", webpage_id, " score is: ", score)

                        else:

                            print("Duplicate image link exists! ", webpage_id, img_link, webpage_title, web_link)
                    else:
                        print("score = 0! ", img_link, web_link)

                if not line:
                    break


    def text_preprocessing(self, text):

        text = text.lower()
        text = text.replace('-', ' ')
        text = text.replace('\n', ' ')

        update_text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))

        update_text = " ".join(update_text.split())

        return update_text

    def stop_place(self, link, if_web):
        stop_place = 0
        dash_times = 0
        for i in range(len(link) - 1, -1, -1):

            if dash_times > 1:
                stop_place = i + 1
                break
            # print(i, a_link[i])
            if link[i] == '/':

                if not if_web:

                    stop_place = i + 1
                    break
                dash_times += 1

        return stop_place

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

    def save_image_to_static(self, image_link_file):

        # user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        user_agent = 'Mozilla/5.0'
        headers={'User-Agent':user_agent}
        my_path = '/Users/humanuk/Desktop/final_project_images/'
        count = 0
        with open(image_link_file, 'r') as file_read:
            next(file_read)

            while True:
                line = file_read.readline()
                # line = line.strip('\n')
                record = line.split('###')
                # print(record)
                if count % 100 == 0:
                    print("Progress: ", count)


                img_link = record[1]
                # img_link = 'https://pacificpotluck.com/wp-content/uploads/2020/12/Garlic-sesame-spinach-300x300.jpg'

                try:
                    request = urllib.request.Request(img_link, None, headers)
                    response = urllib.request.urlopen(request)

                    image = Image.open(response)
                    pic_name = os.path.basename(img_link)
                    # print(pic_name)

                    image_path = os.path.join(my_path, pic_name)
                    image.save(image_path)

                except Exception as e:
                    print('\tError: ',e, '\t', img_link)
                    pass

                count += 1
                # if not line or counter == 5:
                #     break
                # counter += 1
                if not line:
                    break





obj = download_image()
# obj.read_from_txt('datafile8054.txt')
# obj.save_image_to_static('all_image_links.txt')