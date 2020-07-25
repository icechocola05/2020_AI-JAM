
import time  # 지연시간
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['부제목', '평점', '쪽수', 'ebook 여부'])

# 2020년 6월
# 2020년 6월 첫번째 페이지만 GET 방식이니까 따로 먼저 돌려주기
first_url ="http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?range=1&kind=2&orderClick=DAB&mallGb=KOR&linkClass=A"
raw = requests.get(first_url, headers={"User-Agent":"Mozilla/5.0"})
html = BeautifulSoup(raw.text, 'html.parser')

container = html.select("div.detail")
for c in container:
    title = c.select_one("div.detail div.title a")
    addexplain = c.select_one("div.subtitle").text.strip()
    rank = c.select_one("div.review em").text.strip()
    if(c.select_one(".detail .price a span")):
        eBook = 1
    else:
        eBook = 0
    url = title.attrs["href"]

    each_raw = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    each_html = BeautifulSoup(each_raw.text, 'html.parser')

    bf_page = each_html.select("table.table_simple2 td")
    page = bf_page[1].text.rstrip('쪽')

    print(title)
    print(addexplain)
    print(rank)
    print(page)
    print(eBook)
    print("=" * 50)

    sheet.append([addexplain,rank, page, eBook])


# 두번째 페이지부터 POST 방식으로 크롤링하기
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

# 전체 크롤링

for n in range(2, 11):
    time.sleep(1)

    response = requests.post(result_url, data=data)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    container = soup.select("div.detail")
    for c in container:
        title = c.select_one("div.detail div.title a")
        addexplain = c.select_one("div.subtitle").text.strip()
        rank = c.select_one("div.review em").text.strip()
        if (c.select_one(".detail .price a span")):
            eBook = 1
        else:
            eBook = 0
        url = title.attrs["href"]

        each_raw = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        each_html = BeautifulSoup(each_raw.text, 'html.parser')

        bf_page = each_html.select("table.table_simple2 td")
        page = bf_page[1].text.rstrip('쪽')

        print(title)
        print(addexplain)
        print(rank)
        print(page)
        print(eBook)
        print("=" * 50)
        sheet.append([addexplain, rank, page, eBook])

    data['targetPage'] = n + 1
    data['kind'] = 2
    data['pageNumber'] = n
wb.save('crawling_best_2020060.xlsx')
# 2017/4 ~ 2020/5

# 날짜 리스트 만들기
bestYmd = [2017040, 2017050, 2017060, 2017070, 2017080, 2017090, 2017100, 2017110, 2017120,
           2018010, 2018020, 2018030, 2018040, 2018050, 2018060, 2018070, 2018080, 2018090, 2018100, 2018110, 2018120,
           2019010, 2019020, 2019030, 2019040, 2019050, 2019060, 2019070, 2019080, 2019090, 2019100, 2019110, 2019120,
           2020010, 2020020, 2020030, 2020040, 2020050]

for ymd in bestYmd:

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(['부제목', '평점', '쪽수', 'ebook 여부'])

    data['selBestYmw'] = ymd
    data['targetPage'] = 0
    data['kind'] = 2
    for n in range(1, 11):
        time.sleep(1)

        response = requests.post(result_url, data=data)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        container = soup.select("div.detail")
        for c in container:
            title = c.select_one("div.detail div.title a")
            addexplain = c.select_one("div.subtitle").text.strip()
            rank = c.select_one("div.review em").text.strip()
            if (c.select_one(".detail .price a span")):
                eBook = 1
            else:
                eBook = 0
            url = title.attrs["href"]

            each_raw = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            each_html = BeautifulSoup(each_raw.text, 'html.parser')

            bf_page = each_html.select("table.table_simple2 td")
            try:
                page = bf_page[1].text.rstrip('쪽')
            except:
                page = str(0)

            print(addexplain)
            print(rank)
            print(page)
            print(eBook)
            print("=" * 50)
            sheet.append([addexplain, rank, page, eBook])

        # 페이지 넘어가기
        data['targetPage'] = n + 1
        data['kind'] = 2

    wb.save('crawling_best_'+str(ymd)+'.xlsx')

