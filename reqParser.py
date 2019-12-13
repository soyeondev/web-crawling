from bs4 import BeautifulSoup
import requests
import urllib
import re

enc_query = "밀플랜비"
encode_query = urllib.parse.quote(enc_query)
url = ("https://search.naver.com/search.naver?where=post&sm=tab_jum&query="+encode_query)

response = requests.get(url)
html = response.text
bs = BeautifulSoup(html, 'html.parser')

tags = bs.findAll('li', attrs={'class':'sh_blog_top'})
for tag in tags:
    # 썸네일 div(썸네일 이미지, 게시물 링크)
    thum_divs = tag.findAll('div', attrs={'class':'thumb thumb-rollover'})
    #print(type(link_divs))
    for thum_div in thum_divs:
        # 썸네일 이미지
        print(thum_div.a['href'])
        print('썸네일이미지',type(thum_div.a['href']))
        # 게시물 링크
        print(thum_div.img['src'])

    # 게시물 내용 div(제목, 작성일, 내용, 블로그제목, 블로그링크)
    cont_dls = tag.findAll('dl')
    for cont_dl in cont_dls:
        title = cont_dl.a['title']
        # 제목
        print(title)
        # 작성일
        reg_date = cont_dl.dd
        print(reg_date.text)

        # 내용
        contents_pre = cont_dl.findAll('dd', attrs={'class': 'sh_blog_passage'})
        contents = re.findall('<dd class="sh_blog_passage">(.+?)</dd>',str(contents_pre),re.DOTALL)
        print(str(contents))
        print('내용',type(str(contents)))

        # 제목, 링크 들어있는 span
        span_in = cont_dl.span
        # 블로그제목
        blog_name = re.findall('<a class="txt84".+?target="_blank">(.+?)</a> ', str(span_in), re.DOTALL)
        # 블로그링크
        blog_link = re.findall('<a class="url".+?>.+?(.+?)</a>', str(span_in), re.DOTALL)
        print(blog_name)
        print(blog_link)

        print('------------------------------------------------------------------------------------------')
