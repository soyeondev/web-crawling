import re
import json
import math
import datetime
import requests
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
#from flask import Flask, render_template, redirect, request, url_for

#app = Flask(__name__)

naver_client_id = "id입력"
naver_client_secret = "password입력"

#@app.route('/get_blog_post', methods=['POST'])
def get_blog_post(query, display, start_index, sort):
    global no, fs, response_body_dict, j_file

    encode_query = urllib.parse.quote(query)
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query + "&display=" + str(
        display) + "&start=" + str(start_index) + "&sort=" + sort
    request = urllib.request.Request(search_url)
    print(request)
    request.add_header("X-Naver-Client-Id", naver_client_id)
    request.add_header("X-Naver-Client-Secret", naver_client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()

    if response_code is 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode('utf-8'))

        with open("C:\\Users\ksy\AppData\Local\Programs\Python\Python37/" + query + ".json", 'w',
                  encoding='utf-8') as j_file:
            json.dump(response_body_dict, j_file, ensure_ascii=False, indent='\t')

        for item_index in range(0, len(response_body_dict['items'])):
            try:
                remove_html_tag = re.compile('<.*?>')
                title = re.sub(remove_html_tag, '', response_body_dict['items'][item_index]['title'])
                link = response_body_dict['items'][item_index]['link'].replace("amp;", "")
                description = re.sub(remove_html_tag, '', response_body_dict['items'][item_index]['description'])
                blogger_name = response_body_dict['items'][item_index]['bloggername']
                blogger_link = response_body_dict['items'][item_index]['bloggerlink']
                post_date = datetime.datetime.strptime(response_body_dict['items'][item_index]['postdate'],
                                                       "%Y%m%d").strftime("%y.%m.%d")

                no += 1
                print("--------------------------------------------------------")
                print("#" + str(no))
                print("title: " + title)
                print("Link: " + link)
                print("description: " + description)
                print("blogger_name: " + blogger_name)
                print("blogger_link: " + blogger_link)
                print("post_date: " + post_date)

                post_code = requests.get(link)
                post_text = post_code.text
                post_soup = BeautifulSoup(post_text, 'lxml')

                for mainFrame in post_soup.select('iframe#mainFrame'):
                    blog_post_url = "http://blog.naver.com" + mainFrame.get('src')
                    blog_post_code = requests.get(blog_post_url)
                    blog_post_text = blog_post_code.text
                    blog_post_soup = BeautifulSoup(blog_post_text, 'lxml')

                    for blog_post_content in blog_post_soup.select('div#postViewArea'):
                        blog_post_content_text = blog_post_content.get_text()
                        blog_post_full_contents = str(blog_post_content_text)
                        blog_post_full_contents = blog_post_full_contents.replace("\n\n", "\n")
                        # print("blog_post_contents: "+ blog_post_full_contents + "\n")
                        fs.write(blog_post_full_contents + "\n")
                        fs.write("-------------------------------------------\n")

            except:
                item_index += 1
    return response_body_dict

if __name__ == '__main__':
    print("ok")
    no = 0
    query = "밀플랜비"
    display = 10
    start = 1
    sort = "date"

    fs = open(query + ".txt", 'a', encoding='utf-8')
    print("query: " + query)
    print("display: " + display)
    #blog_count = get_blog_count(query, display)
    for start_index in range(start, blog_count + 1, display):
        get_blog_post(query, display, start_index, sort)

    fs.close()
