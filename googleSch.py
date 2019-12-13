from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

start = time.time()

# 크롬 headless 모드 실행
chrome_options = webdriver.ChromeOptions()

 
#selenium의 webdriver로 크롬 브라우저를 실행한다
driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe", options=chrome_options)
enc_query = "밀플랜비"
encode_query = urllib.parse.quote(enc_query)

#"NAVER"에 접속한다
driver.get("https://search.naver.com/search.naver?where=post&sm=tab_jum&query="+encode_query)

#검색 입력 부분에 다양한 명령을 내리기 위해 elem 변수에 할당한다
#elem = driver.find_element_by_name("query")
 
#입력 부분에 default로 값이 있을 수 있어 비운다
#elem.clear()

#검색어를 입력한다
#elem.send_keys("밀플랜비")
#검색을 실행한다
#elem.submit()

#블로그 검색으로 이동 
#driver.find_element_by_class_name("lnb3").click()

#xpath = """//*[@id="main_pack"]/div[3]/a[2]"""
#driver.find_element_by_xpath(xpath).click()

def get_blog_post():
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
    #하나씩 프린트
    for i in range(len(list_link)):
        response_body_dict_pre ["link"] = list_link[i]
        response_body_dict_pre ["thumbnail"] = list_thumbnail[i]
        response_body_dict_pre ["title"] = list_title[i].text
        response_body_dict_pre ["date"] = list_date[i].text
        response_body_dict_pre ["passage"] = list_passage[i].text
        response_body_dict_pre ["bname"] = list_bname[i].text
        response_body_dict_pre ["url"] = list_url[i].text
        response_body_dict[i] = response_body_dict_pre
    print(response_body_dict)
    print("time: ", time.time() - start )
    return "a"

get_blog_post()
#브라우저를 종료한다
#driver.close()
