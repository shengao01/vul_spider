# -*- coding: utf-8 -*-
import requests
from lxml import etree
from selenium import webdriver
import time
import traceback
from collections import OrderedDict
from pprint import pprint


def not_empty(s):
    return s and s.strip()


class CnvdSpider(object):
    def __init__(self):
        super(CnvdSpider, self).__init__()
        self.start_url = "http://ics.cnvd.org.cn"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

    def get_content(self, url):
        resp = requests.get(url, headers=self.headers).content.decode()
        html = etree.HTML(resp)
        return html

    def parse_detail(self, html):
        list = html.xpath("//tbody[@id='tr']/tr")
        item_list = []
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        for a in list:
            href = a.xpath(".//a/@href")[0]
            print(href)  # 详情页入口
            driver.get(href)
            time.sleep(3)
            item = {}
            try:
                item["nameChs"] = [i.text for i in driver.find_elements_by_xpath(u"//div[@class='blkContainerSblk']//tbody/tr")]
                # item["nameChs"] = driver.find_element_by_class_name("blkContainerSblk").text.split("\n")
                # item["cnvd_id"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[1]/td[2]").text
                # item["open_date"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[2]/td[2]").text
                # item["level"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[3]/td[2]").text[0:1]
                # item["affcet_product"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[4]/td[2]").text
                # item["cve_id"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[5]/td[2]").text
                # item["describe"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[6]/td[2]").text
                # item["baosong_date"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[11]/td[2]").text
                # item["shoulu_date"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[12]/td[2]").text
                # item["update_date"] = driver.find_element_by_xpath(u"//table[@class='gg_detail']/tbody/tr[13]/td[2]").text
                # item["score"] = driver.find_element_by_xpath(u"//div[@id='showDiv']/div").text
                print(item)
                item_list.append(item)
            except:
                driver.save_screenshot("a.png")
                traceback.print_exc()
        driver.close()

        # for a in list:
        #     href = a.xpath(".//a/@href")[0]
        #     print(href)  # 详情页入口
        #     html = self.get_content(href)
        #     item={}
        #     item["id"] = html.xpath("//table[@class='gg_detail']/tbody//tr[1]/td[2]//text()")[0]
        #     print(item)  # 这里反爬用selenium
        #     item_list.append(item)
        # pprint(item)
        return item_list

    def run(self):
        html = self.get_content(self.start_url)
        item = self.parse_detail(html)
        pprint(item)


class CnnvdSpider(object):
    def __init__(self):
        super(CnnvdSpider, self).__init__()
        self.start_url = "http://www.cnnvd.org.cn/web/vulnerability/querylist.tag?pageno={}"
        self.part_url = "http://www.cnnvd.org.cn"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

    def get_content(self, url):
        resp = requests.get(url, headers=self.headers).content.decode()
        html = etree.HTML(resp)
        return html

    def get_detail(self, html):
        list = html.xpath("//div[@class='list_list']//li/div/a/@href")
        item_list = []
        for a in list:
            detail_url = self.part_url + a
            print(detail_url)
            detail_html = self.get_content(detail_url)
            item = {}
            item = OrderedDict()
            item["cnnvd_id"] = detail_html.xpath("//div/div/div/div/ul/li/span")[0].text.strip()
            item["cnnvd_id"] = item["cnnvd_id"].split("：")[-1].strip()
            item["risk_level"] = detail_html.xpath("//div/div/div/div/ul/li[2]/a/@style")[0].strip()
            item["cve_id"] = detail_html.xpath("//div/div/div/div/ul/li[3]/a")[0].text.strip()
            item["vul_type"] = detail_html.xpath("//div/div/div/div/ul/li[4]/a")[0].text.strip()
            item["pub_date"] = detail_html.xpath("//div/div/div/div/ul/li[5]/a")[0].text.strip()
            item["thread_type"] = detail_html.xpath("//div/div/div/div/ul/li[6]/a")[0].text.strip()
            item["update_date"] = detail_html.xpath("//div/div/div/div/ul/li[7]/a")[0].text.strip()
            item["vender"] = detail_html.xpath("//div/div/div/div/ul/li[8]/a")[0].text.strip() if detail_html.xpath("//div/div/div/div/ul/li[8]/a") else ""
            item["vul_src"] = detail_html.xpath("//div/div/div/div/ul/li[9]/a")[0].text.strip() if detail_html.xpath("//div/div/div/div/ul/li[9]/a") else ""
            item["description"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj']/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj']/p") else ""
            item["公告"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][1]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][1]/p") else ""
            item["参考网址"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][2]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][2]/p") else ""
            item["受影响实体"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][3]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][3]/p") else ""
            item["补丁"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][4]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][4]/p") else ""
            print(item)

    def run(self):
        url_1 = self.start_url.format(1)
        html = self.get_content(url_1)
        self.get_detail(html)
        # print(item)


class IcsaSpider(object):
    def __init__(self):
        super(IcsaSpider, self).__init__()
        self.start_url = "https://www.us-cert.gov/ics/advisories?page={}"
        self.part_url = "https://www.us-cert.gov"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

    def get_content(self, url):
        resp = requests.get(url, headers=self.headers).content.decode()
        html = etree.HTML(resp)
        return html

    def get_detail(self, html):
        href_list = html.xpath("//ul//span/a/@href")
        for a in href_list:
            detail_url = self.part_url + a
            # detail_url = "https://www.us-cert.gov/ics/advisories/icsa-19-178-01"
            print(detail_url)
            detail_html = self.get_content(detail_url)
            item = {}
            # item = OrderedDict()
            ics_temp = detail_html.xpath("//div[@id='ncas-header']/h1")[0].text.strip()
            item["ICS Advisory-ID"] = ics_temp.split("(")[-1].strip(")")
            item["title"] = detail_html.xpath("//div[@id='ncas-header']/h2")[0].text.strip()
            item["CVSS v3"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[1]//text()")[0].strip()
            item["ATTENTION"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[2]/text()")[0].strip()
            item["Vendor"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[3]/text()")[0].strip()
            item["Equipment"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[4]/text()")[0].strip()
            item["Vulnerabilities"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[5]/text()")[0].strip()
            item["RISK EVALUATION"] = detail_html.xpath("//div[@id='ncas-content']/div[1]/p[1]")[0].text.strip()
            overview_cont_list1 = detail_html.xpath("//div[@id='ncas-content']/div[1]//text()")
            overview_cont_list = list(filter(not_empty, overview_cont_list1))
            print(overview_cont_list)
            aftprd_start = overview_cont_list.index("3.1 AFFECTED PRODUCTS")
            overview_start = overview_cont_list.index("3.2 VULNERABILITY OVERVIEW")
            overview_end = overview_cont_list.index("3.3 BACKGROUND")
            background_end = overview_cont_list.index("3.4 RESEARCHER")
            res_end = overview_cont_list.index("4. MITIGATIONS")
            item["AFFECTED PRODUCTS"] = " ".join(overview_cont_list[aftprd_start+1: overview_start])
            item["VULNERABILITY OVERVIEW"] = " ".join(overview_cont_list[overview_start+1: overview_end]).replace("\xa0", "")
            item["BACKGROUND"] = " ".join(overview_cont_list[overview_end+1: background_end])
            item["RESEARCHER"] = " ".join(overview_cont_list[background_end+1: res_end])
            item["MITIGATIONS"] = " ".join(overview_cont_list[res_end+1:])
            print(item)

    def run(self):
        url = self.start_url.format(0)
        html = self.get_content(url)
        self.get_detail(html)


class CveSpider(object):
    def __init__(self):
        super(CveSpider, self).__init__()
        self.start_url = "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-{}-{}"
        self.end = "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-{}-{}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

    def get_content(self, url):
        resp = requests.get(url, headers=self.headers).content.decode()
        html = etree.HTML(resp)
        return html

    def get_detail(self, html):
        item = {}
        item = OrderedDict()
        item["CVE-ID"] = html.xpath("//tr/td//h2")[0].text.strip()
        item["Description"] = "".join(list(filter(not_empty, html.xpath("//div[@id='GeneratedTable']//tr[4]//text()"))))
        item["References"] = "".join(list(filter(not_empty, html.xpath("//div[@id='GeneratedTable']//tr[7]//text()"))))
        item["Assigning CNA"] = html.xpath("//div[@id='GeneratedTable']//tr[9]/td[1]//text()")[0].strip()
        item["Date Entry Created"] = html.xpath("//div[@id='GeneratedTable']//tr[11]/td[1]//text()")[0].strip()
        item["Phase (Legacy)"] = html.xpath("//div[@id='GeneratedTable']//tr[13]/td[1]//text()")[0].strip() if html.xpath("//div[@id='GeneratedTable']//tr[13]/td[1]//text()") else ""
        item["Votes (Legacy)"] = html.xpath("//div[@id='GeneratedTable']//tr[15]/td[1]//text()")[0].strip() if html.xpath("//div[@id='GeneratedTable']//tr[15]/td[1]//text()") else ""
        item["Comments (Legacy)"] = html.xpath("//div[@id='GeneratedTable']//tr[17]/td[1]//text()")[0].strip() if html.xpath("//div[@id='GeneratedTable']//tr[17]/td[1]//text()") else ""
        item["Proposed (Legacy)"] = html.xpath("//div[@id='GeneratedTable']//tr[19]/td[1]//text()")[0].strip() if html.xpath("//div[@id='GeneratedTable']//tr[19]/td[1]//text()") else ""
        print(item)

    def run(self):
        year_list = [2019, 2018, 2017, 2016]
        for year in year_list:
            for num in range(1, 30000):
                num = "%04d" % num
                url = self.start_url.format(year, num)
                print(url)
                html = self.get_content(url)
                self.get_detail(html)
                time.sleep(1)


if __name__ == '__main__':
    cnvd = CnvdSpider()
    cnvd.run()
    # cnnvd = CnnvdSpider()
    # cnnvd.run()
    # icsa = IcsaSpider()
    # icsa.run()
    # cve = CveSpider()
    # cve.run()
