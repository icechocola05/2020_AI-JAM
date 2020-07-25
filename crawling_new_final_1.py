
# # 정적페이지 > 링크 들어가서 크롤링할 때
import time  # 지연시간
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import openpyxl
#
# wb = openpyxl.Workbook()
# sheet = wb.active
# sheet.append(['부제목', '평점', '쪽수', 'ebook 여부'])

# 2017/4 ~ 2020/6
# 날짜 리스트 만들기
bestYmd = [2017042, 2017052, 2017062, 2017072, 2017082, 2017092, 2017102, 2017112, 2017122,
           2018012,2018022, 2018032, 2018042, 2018052, 2018062, 2018072, 2018082, 2018092, 2018102, 2018112, 2018122,
           2019012, 2019022, 2019032, 2019042, 2019052, 2019062, 2019072, 2019082, 2019092, 2019102, 2019112, 2019122,
           2020012, 2020022, 2020032, 2020042, 2020052, 2020062]

# 리스트 url
result_url = "http://www.kyobobook.co.kr/newproduct/newProductList.laf"
# 특징
lines = '''mallGb: KOR
tabGb: 1
subEjkGb: KOR
newYmw: 2020073
linkClass: 00
sortColumn: near_date
excelYn: N
seeOverYn: Y
pageNumber: 1
perPage: 20
targetPage: 2
filter: ALL
loginYN: N
yyyy: 2020
mm: 07
week: 3
barcode: 9791197070006
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791196744557
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791196699420
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791189909178
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791189356330
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791165040963
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791136228758
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791136005816
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791129706454
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788968571541
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788961412537
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788958077633
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788954673105
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788950989217
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788936486617
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788932037493
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788931589559
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788925568690
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9788925536934
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1: 
barcode: 9791196918033
ejkGb: KOR
notAge: 0 
qty: 1
subBookNm1:
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

# 전체 크롤링

for ymd in bestYmd:
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(['도서명', '부제목', '출간일', '분야', '정가', '평점', '쪽수', '이북 여부', '제목 길이', '순위', '베스트셀러 여부'])

    data['newYmw'] = ymd
    data['targetPage'] = 0
    for n in range(0, 11):
        time.sleep(1)

        response = requests.post(result_url, data=data)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        container = soup.select("div.detail")
        for c in container:
            title = c.select_one("div.detail div.title a")
            title_af = str(title.text.strip())
            title_len = 0
            for t in title_af:
                if t == '(':
                    break
                title_len += 1
            date = c.select_one(".pub_info .publication:nth-of-type(3)").text
            year = date[0:4]
            month = date[6:8]
            day = date[10:12]
            date = year + month + day
            print(date)
            rank = c.select_one(".info_area .score strong").text
            url = title.attrs["href"]
            url = url.split("',")
            first = url[1][1:]
            second = url[2][1:]
            url = "http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&linkClass=" + str(first) + \
                  "&barcode=" + str(second)

            each_raw = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            each_html = BeautifulSoup(each_raw.text, 'html.parser')

            subtitle = each_html.select(".box_detail_point .title .back")
            bf_page = each_html.select("table.table_simple2 td")
            bf_category = each_html.select(".list_detail_category li:nth-of-type(1) a:nth-of-type(1)")
            try:
                price = str(each_html.select_one(".box_detail_price .org_price").text.strip())
                price = price.rstrip('원')
                price = price.replace(",", "")
            except:
                price = ""


            try:
                category = bf_category[0].text.strip()
            except:
                category = ""

            try:
                page = bf_page[1].text.rstrip('쪽')
            except:
                page = str(0)

            if (each_html.select(".box_detail_version ul li:nth-of-type(1)")):
                eBook = 1
            else:
                eBook = 0

            print("제목:", title_af)
            print("제목 길이:", title_len)
            sub = ""
            for i in subtitle:
                sub += str(i.get_text().strip())
            print("출간일:", date)
            print("가격:", price)
            print("부제목:", sub)
            print("평점:", rank)
            print("페이지수:", page)
            print("분야:", category)
            print("eBook:", eBook)
            print("=" * 50)

            sheet.append([title_af, sub, date, category, price, rank, page, eBook, title_len, 0, 0])

        data['targetPage'] = n + 1
    wb.save('crawling_new_' + str(ymd) + '.xlsx')