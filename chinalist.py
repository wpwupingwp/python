#!/usr/bin/python3

from selenium import webdriver
from time import sleep

address = 'http://www.tropicos.org/RankBrowser.aspx?letter=1&ranklevel=species&projectid=8'
button_xpath = '//*[@id="ctl00_MainContentPlaceHolder_SimplePagingControlTop_nextPageButton"]'
option = webdriver.ChromeOptions()
option.add_argument('--proxy-server=socks5://127.0.0.1:1080')
driver = webdriver.Chrome(chrome_options=option)
driver.get(address)
with open('1.html', 'w') as out:
    out.write(driver.page_source)
for i in range(2, 334):
    sleep(3)
    driver.find_element_by_xpath(button_xpath).click()
    with open(str(i)+'.html', 'w') as out:
        out.write(driver.page_source)
