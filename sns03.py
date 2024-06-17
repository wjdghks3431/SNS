import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


def search_google(query, num_results):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome()

    query = query.replace(' ', '+') + '+filetype:pdf'
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    driver.get(url)
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    driver.quit()
    return html

def extract_pdf_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if re.search(r'\.pdf$', href):
            links.append(href)
        elif '/url?q=' in href:
            parsed_url = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get('q')
            if parsed_url and re.search(r'\.pdf$', parsed_url[0]):
                links.append(parsed_url[0])
    return links

def download_pdf(url, output_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, 'wb') as file:
        file.write(response.content)

def main():
    query = input("검색어를 입력하세요: ")
    num_files = int(input("다운로드할 파일 개수를 입력하세요: "))
    save_directory = input("파일을 저장할 위치를 입력하세요: ")

    html = search_google(query, num_files)
    pdf_links = extract_pdf_links(html)

    if not pdf_links:
        print("PDF 링크를 찾을 수 없습니다.")
        return

    for i, pdf_link in enumerate(pdf_links[:num_files]):
        output_path = os.path.join(save_directory, f"document_{i+1}.pdf")
        print(f"Downloading {pdf_link} to {output_path}")
        try:
            download_pdf(pdf_link, output_path)
            print(f"Downloaded {pdf_link} to {output_path}")
        except Exception as e:
            print(f"Failed to download {pdf_link}: {e}")

if __name__ == "__main__":
    main()
