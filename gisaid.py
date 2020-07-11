#!/usr/bin/python3

from selenium import webdriver
from time import sleep

url = 'https://platform.gisaid.org/epi3/start'
#url = 'file://g:/a.html'
driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(10)
# single quote inside
user = driver.find_element_by_css_selector('#elogin')
pwd = driver.find_element_by_css_selector('#epassword')
login = driver.find_element_by_xpath("//*[@id='login']/div[2]/input[3]")
user.send_keys('wpwupingwp')
pwd.send_keys('covid-19NCP')
login.click()

