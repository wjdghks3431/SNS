from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os


# Step 1. 필요한 모듈과 라이브러리를 로딩하고 검색어를 입력 받습니다
search_value=input("1. 검색할 이미지")
num = int(input("2. 검색할 개수"))
f_dir = input('3. 사진을 저장할 폴더를 지정하세요(예: c:\\data\\) : ')
query_txt = '사진저장'

# Step 2. 파일을 저장할 폴더를 생성합니다
now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

os.makedirs(os.path.join(f_dir, s + '-' + query_txt))
f_result_dir = os.path.join(f_dir, s + '-' + query_txt)

# Step 3. 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다
driver = webdriver.Chrome()

s_time = time.time()  # 크롤링 시작 시간을 위한 타임 스탬프를 찍습니다

driver.get(f"https://www.istockphoto.com/kr/search/2/image?phrase={search_value}")
time.sleep(2)  # 페이지가 모두 열릴 때 까지 2초 기다립니다.

try:
    driver.find_element_by_xpath("/html/body/div[8]/div[3]/div[1]/button/svg").click()
except :
    print("팝업창 없음")

# search = driver.find_element(By.CSS_SELECTOR,".oJsi0KFAthcrF4v2Aqxw Jve4u_0OujD9sx_7Jmgi")
# search.click(search_value)

# search.send_keys(Keys.ENTER)
# time.sleep(2)

# 학습목표 1: 자동 스크롤다운 함수 만들기
# Step 4. 스크롤다운 함수를 생성한 후 실행합니다.
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

scroll_down(driver)

# Step 5. 이미지 추출하여 저장하기
file_no = 0                                
count = 1
img_src2=[]

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
img_src = soup.find('div', class_='DE6jTiCmOG8IPNVbM7pJ').find_all('img')

for i in img_src :
    img_src1=i['src']
    img_src2.append(img_src1)
    count += 1
    if count > num:
        break

for img_url in img_src2:
    try:
        file_no += 1
        urllib.request.urlretrieve(img_url, os.path.join(f_result_dir, str(file_no) + '.jpg'))
        print("%s 번째 이미지 저장중입니다=======" % file_no)
    except Exception as e:
        print(e)
        continue

# Step 6. 요약 정보를 출력합니다
e_time = time.time()
t_time = e_time - s_time

print("=" * 70)
print("총 소요시간은 %s 초 입니다 " % round(t_time, 1))
print("총 저장 건수는 %s 건 입니다 " % file_no)
print("파일 저장 경로: %s 입니다" % f_result_dir)
print("=" * 70)

driver.close()

