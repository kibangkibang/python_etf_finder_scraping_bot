import re
import math
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

othersTitle = []
baseUrl = 'https://www.etf.com/etfanalytics/etf-finder/'
#구글 검색의 기본 url : 검색 여러번하고 주소창 보면 공통 형식이 보인다.
plusUrl = ''
url = baseUrl + quote_plus(plusUrl)
#quote_plus : 문자열을 인터넷 검색가능한 형식으로 바꿔준다.

driver = webdriver.Chrome('C:/Users/csh09/PycharmProjects/etf/chromedriver.exe')
driver.get(url)

wait = WebDriverWait(driver, 10) #최대 한시간 대기
wait.until(EC.presence_of_element_located((By.ID, 'finderTable')))

others = driver.find_elements_by_css_selector('li.Tooltip_default')
for i in others:
othersTitle.append(i)

btn = driver.find_elements_by_css_selector('button.inactiveResult')
btn[2].send_keys(Keys.ENTER)

for num,i in enumerate(othersTitle):
print(i.text)
btnnext = driver.find_element_by_id('nextPage')

html = driver.page_source
soup = BeautifulSoup(html)
file_path_title = 'C:/Users/csh09/PycharmProjects/etf/etfData' + i.find_element_by_tag_name('span').text.replace(" ","") +'.txt'
etf_data_file = open(file_path_title,'w+',encoding="utf-8")

nowpage = 1
totalpage = re.sub('[^0-9]', '', soup.find('label',{'id':'totalPages'}).get_text())

tableHeader = soup.find('tr',{'class':'TableHeader'}).find_all('label')
for i in tableHeader:
etf_data_file.write(i.get_text() + "|")
etf_data_file.write('\n')

while(nowpage <= int(totalpage)):
html = driver.page_source
soup = BeautifulSoup(html)
etf_list = soup.find('table', {'id': 'finderTable'}).find('tbody').find_all('tr')
for tr in etf_list:
tr_list = tr.find_all('td')
for col,td in enumerate(tr_list):
try:
if(num == 0 and col == 4):
p = re.search('[+-]?[0-9]+(.[0-9]+)?', re.sub('[$,%]', '', td.get_text().strip()))
etf_data_file.write(str(p.group()) + "|")
elif(num == 0 and col == 5):
p = re.search('[+-]?[0-9]+(.[0-9]+)?',re.sub('[$,%]','',td.get_text().strip()))
if(td.get_text().strip()[-1] == 'B'):
etf_data_file.write(str(round(float(p.group())*1000000000.0)) + "|")
elif(td.get_text().strip()[-1] == 'M'):
etf_data_file.write(str(round(float(p.group())*1000000.0)) + "|")
elif(td.get_text().strip()[-1] == 'K'):
etf_data_file.write(str(round(float(p.group())*1000.0)) + "|")
else:
etf_data_file.write(str(p.group()) + "|")
elif(num == 1 and (col == 2 or col == 3 or col == 4 or col == 5 or col == 6 or col == 7 or col == 8)):
p = re.search('[+-]?[0-9]+(.[0-9]+)?', re.sub('[$,%]','',td.get_text().strip()))
etf_data_file.write(str(p.group()) + "|")
elif (num == 2 and (col == 2 or col == 3 or col == 4 or col == 5 or col == 6 )):
p = re.search('[+-]?[0-9]+(.[0-9]+)?', re.sub('[$,%]','',td.get_text().strip()))
if (td.get_text().strip()[-1] == 'B'):
etf_data_file.write(str(round(float(p.group()) * 1000000000.0)) + "|")
elif (td.get_text().strip()[-1] == 'M'):
etf_data_file.write(str(round(float(p.group()) * 1000000.0)) + "|")
elif (td.get_text().strip()[-1] == 'K'):
etf_data_file.write(str(round(float(p.group()) * 1000.0)) + "|")
else:
etf_data_file.write(str(p.group()) + "|")
elif (num == 3 and (col == 2)):
if (td.find('span',class_='opListImage') != None):
etf_data_file.write("opListImage" + "|")
elif (td.find('span',class_='analystPickImage') != None):
etf_data_file.write("analystPickImage" + "|")
else:
etf_data_file.write(td.get_text().strip() + "|")
elif (num == 3 and (col == 4 or col == 5 or col == 6)):
p = re.search('[+-]?[0-9]+(.[0-9]+)?', re.sub('[$,%]','',td.get_text().strip()))
etf_data_file.write(str(p.group()) + "|")
elif (num == 4 and (col == 5)):
continue
elif (num == 4 and (col==2 or col == 3 or col == 4 or col == 5 or col == 6 or col == 7 or col == 8)):
p = re.search('[+-]?[0-9]+(.[0-9]+)?', re.sub('[$,%]','',td.get_text().strip()))
etf_data_file.write(str(p.group()) + "|")
elif (num == 5 and (col == 3 or col == 4 or col == 5 or col == 6 or col == 7 or col == 8 )):
p = re.search('[+-]?[0-9]+(.[0-9]+)?', re.sub('[$,%]','',td.get_text().strip()))
etf_data_file.write(str(p.group()) + "|")
else:
etf_data_file.write(td.get_text().strip() + "|")
except Exception as e:
etf_data_file.write("|")
pass

etf_data_file.write('\n')
nowpage = nowpage + 1
driver.execute_script("arguments[0].click();", btnnext)

etf_data_file.close()
if (num == 5):
break
goToInput = driver.find_element_by_id('goToPage')
goToInput.clear()
goToInput.send_keys("1")
goToInput.send_keys(Keys.ENTER)
tabs = '#table-tabs > li:nth-child(' + str(num + 2) + ')'
btnother = driver.find_element_by_css_selector(tabs)
driver.execute_script("arguments[0].click();", btnother)
driver.close()