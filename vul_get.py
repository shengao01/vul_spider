# -*- coding: utf-8 -*-
import requests
from lxml import etree
from selenium import webdriver
import time
from pprint import pprint

url = "http://ics.cnvd.org.cn"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

resp = requests.get(url, headers=headers).content.decode()
html = etree.HTML(resp)


list = html.xpath("//tbody[@id='tr']/tr")
for a in list:
    href = a.xpath(".//a/@href")[0]
    print(href) #详情页入口
    # resp = requests.get(href,headers=headers).content.decode()
    # print(resp)
    # html = etree.HTML(resp)
    # item={}
    # item["id"] = html.xpath("//table[@class='gg_detail']/tbody//text()")
    # print(item)  # 这里反爬用selenium
    driver = webdriver.Chrome()
    driver.get(href)
    time.sleep(3)
    item = {}
    item["nameChs"] = driver.find_element_by_xpath('//div[@class="blkContainerSblk"]/h1').text
    item["cnvd_id"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[1]/td[2]").text
    item["open_date"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[2]/td[2]").text
    item["level"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[3]/td[2]").text[0:1]
    item["affcet_product"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[4]/td[2]").text
    item["cve_id"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[5]/td[2]").text
    item["describe"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[6]/td[2]").text
    item["baosong_date"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[11]/td[2]").text
    item["shoulu_date"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[12]/td[2]").text
    item["update_date"] = driver.find_element_by_xpath("//table[@class='gg_detail']/tbody/tr[13]/td[2]").text
    item["score"] = driver.find_element_by_xpath('//div[@id="showDiv"]/div').text
    driver.close()
    pprint(item)
