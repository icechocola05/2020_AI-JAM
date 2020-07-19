# 동적페이지 페이지 넘기면서 크롤링할 때
from selenium import webdriver
import time  # 지연시간

# driver = webdriver.Chrome("./chromedriver")  # ./은 현재 디렉토리에 있는 크롬드라이버켜줘라는 뜻
# # 베스트셀러에서 분야종합 url
# driver.get(
#     "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?range=1&kind=2&orderClick=DAB&mallGb=KOR&linkClass=A")
#
# # 정적페이지 > 링크 들어가서 크롤링할 때
import requests
from bs4 import BeautifulSoup

from urllib.request import urlretrieve
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

first_url ="http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?range=1&kind=2&orderClick=DAB&mallGb=KOR&linkClass=A"
raw = requests.get (first_url, headers={"User-Agent":"Mozilla/5.0"})
html = BeautifulSoup(raw.text, 'html.parser')

container = html.select("div.detail")
for c in container:
    title = c.select_one("div.detail div.title a")
    addexplain = c.select_one("div.subtitle").text.strip()
    rank = c.select_one("div.review em").text.strip()
    url = title.attrs["href"]

    each_raw = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    each_html = BeautifulSoup(each_raw.text, 'html.parser')

    bf_page = each_html.select("table.table_simple2 td")
    page = bf_page[1].text

    print(addexplain)
    print(rank)
    print(page)
    print("=" * 50)

# 2페이지부터 크롤링하기
# 리스트 url
result_url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"
# 특징
lines = '''targetPage: 2
mallGb: KOR
range: 1
kind: 2
kyoboTotalYn: N
selBestYmw: 2020060
linkClass: A
cateDivYn: 
pageNumber: 1
perPage: 20
excelYn: N
seeOverYn: Y
loginYN: N
barcode: 9791190382175
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791130629636
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791188331796
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9788932920337
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791190786355
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791158740757
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791196831059
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9788965963790
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9788954671156
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791130627878
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9788936434267
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791190299060
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9788954672214
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791190456098
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791197016806
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791187481720
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9788993178692
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791197021602
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791165210144
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
barcode: 9791187119845
ejkGb: KOR
notAge: 0 
cartType: addMast
qty: 1
'''.splitlines()

# 빈칸 제거하고 새로 만든 리스트에 key 와 value 값 넣기
lines_change = []
for line in lines:
    line = line.replace(' ', '')
    lines_change.append(line)

data = {}
for line in lines_change:
    key, value = line.split(':', 1)
    data[key] = value

# post 방식으로 조사
response = requests.post(result_url, data=data)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

for n in range(2, 9):
    time.sleep(1)

    response = requests.post(result_url, data=data)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    container = soup.select("div.detail")
    for c in container:
        title = c.select_one("div.detail div.title a")
        addexplain = c.select_one("div.subtitle").text.strip()
        rank = c.select_one("div.review em").text.strip()
        url = title.attrs["href"]

        each_raw = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        each_html = BeautifulSoup(each_raw.text, 'html.parser')

        bf_page = each_html.select("table.table_simple2 td")
        page = bf_page[1].text

        print(addexplain)
        print(rank)
        print(page)
        print("=" * 50)

    data['targetPage'] = n + 1
    data['kind'] = 2
    data['pageNumber'] = n

    # page_bar = driver.find_elements_by_css_selector('div.list_paging>*')
    # driver.execute_script("arguments[0].click();", page_bar[n + 1])

    # page_bar = driver.find_elements_by_css_selector('div.list_paging>*')
    # driver.execute_script("arguments[0].click();", page_bar[n + 1])
    # driver.execute_script("arguments[8].value=page_bar[n + 1]")
    # 클릭까지는 완료

#
# function _go_targetPage(num){
# 	document.frmList.target = '';
# 	document.frmList.targetPage.value = num;
# 	document.frmList.submit();
# }

# page_bar = driver.find_elements_by_css_selector("div.list_paging a")
# bf_page_bar = driver.find_elements_by_css_selector('div.list_paging>*')
# "arguments[0].click();", sample

# sample = html.find_element_by_css_selector('div.list_paging>*')
# driver.execute_script("_go_targetPage('2').click()", sample)  # 자바 명령어 실행

# bf_page_bar[n + 1].send_keys('\n')


# driver.close()
# driver.execute_script("arguments[1].click();", page_bar)


# page_bar[1].click()

#
# try:
#     if n%10 != 0:
#         page_bar[n%10+1].click()

# except:
#     break

# 동적페이지 > 페이지 넘겨서 크롤링할 때

# <절차>
# 1. 베스트셀러 분야종합 접속
# 2. 연도 및 월 선택 버튼 클릭
# 3. 과거부터 월별로 클릭하기
# 4. 제목클릭해서 링크안으로 들어가서 크롤링하기
# 5. 순위/평점/요약설명/쪽수


# 2. 연도 및 월 선택 버튼 클릭
# 시기별 선택자 :span.sort_option2>ul>li>a

# 4. 링크안으로 들어가기(컨테이너 설정)
# 링크안컨테이너:div.detail
# # link_cont = driver.find_element_by_css_selector("div.detail")
# link_for_crawling = driver.find_elements_by_css_selector("div.detail div.title a")
# link_for_crawling[0].click()
#
# #부연설명:span.back (변수명 add_explain)
# #평점:div.review_klover em (변수명 rank)
# #페이지수:table.table_simple2 td (변수명 page)
# #ebook여부:div.box_detail_version li (변수명 ebook)
# add_explain = driver.find_element_by_css_selector("span.back").text
# rank = driver.find_element_by_css_selector("div.review_klover em").text
# bf_page = driver.find_elements_by_css_selector("table.table_simple2 td")
# page = bf_page[1].text
# bf_ebook = driver.find_elements_by_css_selector("div.box_detail_version li")
# ebook = bf_ebook[0].text
# print(add_explain)
# print(rank)
# print(page)
# print(ebook)
#
#
# link_for_crawling = driver.find_elements_by_css_selector("div.detail div.title a")
# ll = link_for_crawling[0]
# # link_for_crawling.click()
# new_driver = ll.get_attribute('href')
# print(new_driver)

# for문 이용하기
######################동적으로 시도
# cont = driver.find_elements_by_css_selector("div.detail")
#
# for c in cont:
#     link_for_crawling = c.find_element_by_css_selector("div.detail div.title a")
#     #그 링크주소를 담아 변수생성
#     link = link_for_crawling.get_attribute('href')
#     new_driver = webdriver.Chrome("./chromedriver")
#     new_driver.get(link)
#     link_for_crawling.click()
#     time.sleep(1)
#
#     add_explain = new_driver.find_element_by_css_selector("span.back").text
#     rank = new_driver.find_element_by_css_selector("div.review_klover em").text
#     # bf_page = new_driver.find_elements_by_css_selector("table.table_simple2 td")
#     #     # page = bf_page[1].text
#     #     # bf_ebook = new_driver.find_elements_by_css_selector("div.box_detail_version li")
#     #     # ebook = bf_ebook[0].text
#     print(add_explain)
#     print(rank)
#     # print(page)
#     # print(ebook)
#     print("="*50)
#     new_driver.close()
#     driver = webdriver.Chrome("./chromedriver")
#     driver.get("http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?range=1&kind=2&orderClick=DAB&mallGb=KOR&linkClass=A")

# for lc in link_cont:
#     time.sleep(1)
#     link_for_crawling = lc.find_elements_by_css_selector("div.detail div.title a")
#     link_for_crawling[0].click()
#     add_explain = lc.find_elements_by_css_selector("span.back").text
#     rank = lc.find_elements_by_css_selector("div.review_klover em").text
#
#     print(add_explain)
#     print(rank)
# driver.find_elements_by_css_selector("table.table_simple2 td")[0]
# driver.find_elements_by_css_selector("div.box_detail_version li")[0]
#     #
#
# #부가제목: span.back
# #평점:div.review_klover em
# #쪽수: table.table_simple2 td #[1]번째
# #ebook:div.box_detail_version li #[0]번째
# driver.find_elements_by_css_selector("span.back")
# driver.find_elements_by_css_selector("div.review_klover em")
# driver.find_elements_by_css_selector("table.table_simple2 td")[0]
# driver.find_elements_by_css_selector("div.box_detail_version li")[0]
#
#
# # info = m.select("dl.info_txt1 dd")  # 리스트 형태로 장르,감독 데이터가 저장됨
# # #장르
# # genre = info[0].select("a")
# # for
# #
# # # 검색창:input#search-input
# # # 검색어 입력하기
# # search_box = driver.find_element_by_css_selector("input#search-input")
# # search_box.send_keys("치킨")  # 검색어 입력 (key핵심어를 send전송해라)
# # # 검색버튼 누르기
# # search_button = driver.find_element_by_css_selector("button.spm")
# # search_button.click()
# #
# # time.sleep(1) #지연시간 1초
# #
# # #컨테이너:dl.lsnx_det
# # #가게명:dl.lsnx_det dt>a
# # #가게주소:dl.lsnx_det dd.addr
# # #가게번호:dl.lsnx_det dd.tel
# #
# #
# #
# # ###############
# # for n in range[0:]
# # genre = m.select("dl.info_txt1 dd:nth-of-type(n) a")
# # director = m.select("dl.info_txt1 dd:nth-of-type(2) a")
# # actor = m.select("dl.info_txt1 dd:nth-of-type(3) a")
# # ######
# #
# # cont = driver.find_elements_by_css_selector("dl.lsnx_det")
# # for c in cont:
# #     name = c.find_element_by_css_selector("dt>a").text
# #     addr = c.find_element_by_css_selector("dd.addr").text
# #     tel = c.find_element_by_css_selector("dd.tel").text
# #
# #     print(name)
# #     print(addr)
# #     print(tel)
# #     print("="*50)
# #
# #     #웹페이지 뜨고 느리고 잘 안 됨
# #     #import time 넣어주고 버튼클릭한 이후에 time.sleep(1) 지연시간 1초 넣어줌으로써 해결가능
# #
#
# # driver.close()