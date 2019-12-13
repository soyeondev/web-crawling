from flask import Flask, render_template, app
from bs4 import BeautifulSoup
import requests
import urllib
import re

app = Flask(__name__)

@app.route("/")
def blog_contents():
    enc_query = "밀플랜비"
    encode_query = urllib.parse.quote(enc_query)
    url = ("https://search.naver.com/search.naver?where=post&sm=tab_jum&query="+encode_query)

    response = requests.get(url)
    html = response.text
    bs = BeautifulSoup(html, 'html.parser')

    items = {}
    items_list = []
    tags = bs.findAll('li', attrs={'class':'sh_blog_top'})
    for tag in tags:
        # 썸네일 div(썸네일 이미지, 게시물 링크)

        thum_divs = tag.findAll('div', attrs={'class':'thumb thumb-rollover'})
        #print(type(link_divs))
        for thum_div in thum_divs:
            # 게시물 링크
            #print(thum_div.a['href'])
            items['thumb-nail'] = thum_div.a['href']
            # 썸네일 이미지
            print(thum_div.img['src'])
            items['link'] = thum_div.img['src']

        # 게시물 내용 div(제목, 작성일, 내용, 블로그제목, 블로그링크)
        cont_dls = tag.findAll('dl')
        for cont_dl in cont_dls:
            title = cont_dl.a['title']
            # 제목
            print(title)
            items['title'] = cont_dl.a['title']

            # 작성일
            reg_date = cont_dl.dd
            print(reg_date.text)
            items['reg_date'] = reg_date.text

            # 포스팅내용
            contents_pre = cont_dl.findAll('dd', attrs={'class': 'sh_blog_passage'})
            #print(contents_pre.text)
            contents = re.findall('<dd class="sh_blog_passage">(.+?)</dd>',str(contents_pre),re.DOTALL)
            for contents_str in contents:
                print(contents_str)
                items['contents'] = contents_str
                #print(contents)

            # 제목, 링크 들어있는 span
            span_in = cont_dl.span
            print(span_in.text)

            # 블로그제목
            blog_name = re.findall('<a class="txt84".+?target="_blank">(.+?)</a> ', str(span_in), re.DOTALL)
            for blog_name_str in blog_name:
                print(blog_name_str)
                items['blog_name'] = blog_name_str
            # print(blog_name)

            # 블로그링크
            blog_link = re.findall('<a class="url".+?>.+?(.+?)</a>', str(span_in), re.DOTALL)
            for blog_link_str in blog_link:
                print(blog_link_str)
                items['blog_link'] = blog_link_str
                # print(blog_link)

            print('------------------------------------------------------------------------------------------')
            #print(items)
            #print(items['cont'])
            items_list.append(items)
    return render_template("blog_contents.html", items=items_list)

if __name__ == "__main__":
    app.run()

