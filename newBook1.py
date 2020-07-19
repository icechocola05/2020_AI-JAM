from selenium import webdriver
import time

import requests
from bs4 import BeautifulSoup

from urllib.request import urlretrieve
import ssl

driver = webdriver.Chrome("./chromedriver")  #./은 현재 디렉토리에 있는 크롬드라이버켜줘라는 뜻
#베스트셀러에서 분야종합 url
driver.get("http://www.kyobobook.co.kr/newproduct/newProductList.laf?orderClick=Ca1/")


#정적페이지 링크 들어가서 크롤링할 때
##########################정적으로 시도

ssl._create_default_https_context = ssl._create_unverified_context

raw = requests.get("http://www.kyobobook.co.kr/newproduct/newProductList.laf?orderClick=Ca1/",
                    headers={"User-Agent": "Mozilla/5.0"})

html = BeautifulSoup(raw.text, 'html.parser')

container = html.select("div.detail")
for i in range(1, 10):
    for c in container:
        print("="*50)
        title = c.select_one("div.detail div.title a")
        rate = c.select_one(".info_area .score strong")

        # url 구하기
        url = title.attrs["href"]
        url = url.split("',")
        first = url[1][1:]
        second = url[2][1:]
        url = "http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&linkClass=" + str(first) +\
              "&barcode=" + str(second)
        each_raw = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        each_html = BeautifulSoup(each_raw.text, 'html.parser')

        # 속성값 구하기
        add_explain = each_html.select(".box_detail_point .title .back")
        bf_page = each_html.select("table.table_simple2 td")
        page = bf_page[1].text.rstrip("쪽")
        bf_category = each_html.select(".list_detail_category li:nth-of-type(1) a:nth-of-type(1)")
        category = bf_category[0].text.strip()

        # 출력
        print(title.text)
        for explains in add_explain:
            print(explains.get_text().strip())
        print("페이지 수 :" + page)
        print("분야:" + category)
        print(rate.text)
    page_btn = driver.find_elements_by_css_selector(".list_paging ul li")
    page_btn[i + 1].click()

