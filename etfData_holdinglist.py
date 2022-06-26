from time import sleep
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome('C:/Users/csh09/PycharmProjects/etf/chromedriver.exe')
file_etf_holding = open('C:/Users/csh09/PycharmProjects/etf/etf_holding_list.txt','w+',encoding="utf-8")

with open('C:/Users/csh09/PycharmProjects/etf/etfDataFundBasics.txt', 'r', encoding="utf-8") as f_etf:
    data_etf = f_etf.read()
file_etf_list = data_etf.splitlines()
cnt = 0
for etf in file_etf_list:
    if cnt == 0:
        cnt = cnt + 1
        continue
    etf_name =etf.split("|")[0]
    print("---------------" + etf_name + "------------------" + str(cnt) + "/" + str(len(file_etf_list) - 1))
    cnt = cnt + 1
    url = 'https://research2.fidelity.com/fidelity/screeners/etf/public/etfholdings.asp?symbol='+ etf_name +'&view=Explore'

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html)

    list = soup.find_all('tr')
    for i in list:
        try:
            content = etf_name + "|" + i.find_all("td")[0].get_text() + "|" + i.find_all("td")[1].get_text() + "|" + i.find_all("td")[2].get_text() + "|" + i.find_all("td")[3].get_text() + "\n"
            file_etf_holding.write(content)
        except:
            pass
file_etf_holding.close()
driver.close()
