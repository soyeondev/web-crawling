from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from multiprocessing import Pool
from builtins import staticmethod

start = time.time()

# 크롬 headless 모드 실행
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('lang=ko_KR')
 
#selenium의 webdriver로 크롬 브라우저를 실행한다
driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe", options=chrome_options)
driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe")
#enc_query = "밀플랜비"

def get_blog_post(enc_query):
    encode_query = urllib.parse.quote(enc_query)
    
    #"NAVER"에 접속한다
    driver.get("https://search.naver.com/search.naver?where=post&sm=tab_jum&query="+encode_query)

    #링크, 썸네일 받을 배열공간 생성
    list_link = []
    list_thumbnail = []
    
    #링크 태그 받아오기
    list_link_pre = driver.find_elements_by_class_name("sp_thmb.thmb80")
    #썸네일 태그 받아오기
    list_thumbnail_pre = driver.find_elements_by_class_name("sh_blog_thumbnail")
    
    #링크와 썸네일에서 추출한 태그에 src와 href값 append
    for i in range(len(list_link_pre)):
        list_link.append(list_link_pre[i].get_attribute("href"))
        list_thumbnail.append(list_thumbnail_pre[i].get_attribute("src"))
    
    #글제목 받아오기
    list_title = driver.find_elements_by_class_name("sh_blog_title")
    #날짜 받아오기
    list_date = driver.find_elements_by_class_name("txt_inline")
    #글내용 받아오기
    list_passage = driver.find_elements_by_class_name("sh_blog_passage")
    #블로그 이름 받아오기
    list_bname = driver.find_elements_by_class_name("txt84")
    #url 받아오기
    list_url = driver.find_elements_by_class_name("url")
    response_body_dict_pre = {}
    response_body_dict = {}

    for i in range(len(list_link)):
        response_body_dict_pre ["link"] = list_link[i]
        response_body_dict_pre ["thumbnail"] = list_thumbnail[i]
        response_body_dict_pre ["title"] = list_title[i].text
        response_body_dict_pre ["date"] = list_date[i].text
        response_body_dict_pre ["passage"] = list_passage[i].text
        response_body_dict_pre ["bname"] = list_bname[i].text
        response_body_dict_pre ["url"] = list_url[i].text
        response_body_dict[i] = response_body_dict_pre
    return "a"  

if __name__=='__main__':
    start_time = time.time()
    pool = Pool(processes=2)
    pool.map(get_blog_post, get_blog_post("밀플랜비"))
    print("--- %s seconds ---" % (time.time() - start_time))



