# -*- coding: utf-8 -*-
import random

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
        self.start_url = "https://ics.cnvd.org.cn/?max=50&offset={}"
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
            # href = "https://www.cnvd.org.cn/flaw/show/CNVD-2019-21242"
            driver.get(href)
            time.sleep(5)
            try:
                # item["nameChs"] = driver.find_element_by_xpath("//div[@class='blkContainerSblk']//h1").text
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
                item = {}
                item = OrderedDict()
                temp_list = [i.text.strip() if i.text else "" for i in driver.find_elements_by_xpath(u"//div[@class='blkContainerSblk']//tbody/tr//td")][:-1]
                print(temp_list)
                cid_start = temp_list.index("CNVD-ID")
                date_start = temp_list.index("公开日期")
                risk_level_start = temp_list.index("危害级别")
                affect_product_start = temp_list.index("影响产品")
                BUGTRAQ_start = temp_list.index("BUGTRAQ ID") if "BUGTRAQ ID" in temp_list else affect_product_start+2
                cveid_start = temp_list.index("CVE ID") if "CVE ID" in temp_list else BUGTRAQ_start+2
                description_start = temp_list.index("漏洞描述")
                type_start = temp_list.index("漏洞类型")
                href_start = temp_list.index("参考链接")
                resolve_start = temp_list.index("漏洞解决方案")
                patch_start = temp_list.index("厂商补丁")
                info_start = temp_list.index("验证信息")
                send_date_start = temp_list.index("报送时间")
                cate_date_start = temp_list.index("收录时间")
                update_start = temp_list.index("更新时间")
                attach_start = temp_list.index("漏洞附件")
                item["漏洞标题"] = driver.find_element_by_xpath("//div[@class='blkContainerSblk']//h1").text
                item["CNVD-ID"] = "".join(temp_list[cid_start+1: date_start])
                item["公开日期"] = "".join(temp_list[date_start+1: risk_level_start])
                item["危害级别"] = "".join(temp_list[risk_level_start+1: affect_product_start])[0]
                item["影响产品"] = "".join(temp_list[affect_product_start+1: BUGTRAQ_start])
                # item["BUGTRAQ ID"] = "".join(temp_list[BUGTRAQ_start+1: cveid_start])
                item["CVE ID"] = "".join(temp_list[cveid_start+1: description_start])
                item["漏洞描述"] = "".join(temp_list[description_start+1: type_start])
                item["漏洞类型"] = "".join(temp_list[type_start+1: href_start])
                item["参考链接"] = "".join(temp_list[href_start+1: resolve_start])
                item["漏洞解决方案"] = "".join(temp_list[resolve_start+1: patch_start])
                item["厂商补丁"] = "".join(temp_list[patch_start+1: info_start])
                item["验证信息"] = "".join(temp_list[info_start+1: send_date_start])
                item["报送时间"] = "".join(temp_list[send_date_start+1: cate_date_start])
                item["收录时间"] = "".join(temp_list[cate_date_start+1: update_start])
                item["更新时间"] = "".join(temp_list[update_start+1: attach_start])
                item["漏洞附件"] = "".join(temp_list[attach_start+1:])
                print(item)
                item_list.append(item)
            except ValueError:
                driver.close()
                driver = webdriver.Chrome()
                driver.get(href)
                time.sleep(10)
                item = {}
                item = OrderedDict()
                temp_list = [i.text.strip() if i.text else "" for i in driver.find_elements_by_xpath(u"//div[@class='blkContainerSblk']//tbody/tr//td")][:-1]
                print(temp_list)
                cid_start = temp_list.index("CNVD-ID")
                date_start = temp_list.index("公开日期")
                risk_level_start = temp_list.index("危害级别")
                affect_product_start = temp_list.index("影响产品")
                BUGTRAQ_start = temp_list.index("BUGTRAQ ID") if "BUGTRAQ ID" in temp_list else affect_product_start+2
                cveid_start = temp_list.index("CVE ID") if "CVE ID" in temp_list else BUGTRAQ_start+2
                description_start = temp_list.index("漏洞描述")
                type_start = temp_list.index("漏洞类型")
                href_start = temp_list.index("参考链接")
                resolve_start = temp_list.index("漏洞解决方案")
                patch_start = temp_list.index("厂商补丁")
                info_start = temp_list.index("验证信息")
                send_date_start = temp_list.index("报送时间")
                cate_date_start = temp_list.index("收录时间")
                update_start = temp_list.index("更新时间")
                attach_start = temp_list.index("漏洞附件")
                item["漏洞标题"] = driver.find_element_by_xpath("//div[@class='blkContainerSblk']//h1").text
                item["CNVD-ID"] = "".join(temp_list[cid_start+1: date_start])
                item["公开日期"] = "".join(temp_list[date_start+1: risk_level_start])
                item["危害级别"] = "".join(temp_list[risk_level_start+1: affect_product_start])[0]
                item["影响产品"] = "".join(temp_list[affect_product_start+1: BUGTRAQ_start])
                # item["BUGTRAQ ID"] = "".join(temp_list[BUGTRAQ_start+1: cveid_start])
                item["CVE ID"] = "".join(temp_list[cveid_start+1: description_start])
                item["漏洞描述"] = "".join(temp_list[description_start+1: type_start])
                item["漏洞类型"] = "".join(temp_list[type_start+1: href_start])
                item["参考链接"] = "".join(temp_list[href_start+1: resolve_start])
                item["漏洞解决方案"] = "".join(temp_list[resolve_start+1: patch_start])
                item["厂商补丁"] = "".join(temp_list[patch_start+1: info_start])
                item["验证信息"] = "".join(temp_list[info_start+1: send_date_start])
                item["报送时间"] = "".join(temp_list[send_date_start+1: cate_date_start])
                item["收录时间"] = "".join(temp_list[cate_date_start+1: update_start])
                item["更新时间"] = "".join(temp_list[update_start+1: attach_start])
                item["漏洞附件"] = "".join(temp_list[attach_start+1:])
                print(item)
                item_list.append(item)
            finally:
                traceback.print_exc()
        driver.close()
        return item_list

    def run(self):
        for i in range(41):
            url = self.start_url.format(0)
            html = self.get_content(url)
            item = self.parse_detail(html)
            print(len(item))
            print(item)


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
        url_list = html.xpath("//div[@class='list_list']//li/div/a/@href")
        item_list = []
        for a in url_list:
            detail_url = self.part_url + a
            print(detail_url)
            item = {}
            item = OrderedDict()
            try:
                detail_html = self.get_content(detail_url)
                cnnvd_id = detail_html.xpath("//div/div/div/div/ul/li/span")[0].text.strip()
                item["CNNVD编号"] = cnnvd_id.split("：")[-1].strip()
                item["危害等级"] = detail_html.xpath("//div/div/div/div/ul/li[2]/a/@style")[0].strip()
                item["CVE-ID"] = detail_html.xpath("//div/div/div/div/ul/li[3]/a")[0].text.strip()
                item["漏洞类型"] = detail_html.xpath("//div/div/div/div/ul/li[4]/a")[0].text.strip()
                item["发布时间"] = detail_html.xpath("//div/div/div/div/ul/li[5]/a")[0].text.strip()
                item["威胁类型"] = detail_html.xpath("//div/div/div/div/ul/li[6]/a")[0].text.strip()
                item["更新时间"] = detail_html.xpath("//div/div/div/div/ul/li[7]/a")[0].text.strip()
                item["厂商"] = detail_html.xpath("//div/div/div/div/ul/li[8]/a")[0].text.strip() if detail_html.xpath("//div/div/div/div/ul/li[8]/a") else ""
                item["漏洞来源"] = detail_html.xpath("//div/div/div/div/ul/li[9]/a")[0].text.strip() if detail_html.xpath("//div/div/div/div/ul/li[9]/a") else ""
                item["漏洞简介"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj']/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj']/p") else ""
                item["漏洞公告"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][1]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][1]/p") else ""
                item["参考网址"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][2]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][2]/p") else ""
                item["受影响实体"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][3]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][3]/p") else ""
                item["补丁"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][4]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][4]/p") else ""
                print(item)
            except IndexError:
                time.sleep(10)
                detail_html = self.get_content(detail_url)
                cnnvd_id = detail_html.xpath("//div/div/div/div/ul/li/span")[0].text.strip()
                item["CNNVD编号"] = cnnvd_id.split("：")[-1].strip()
                item["危害等级"] = detail_html.xpath("//div/div/div/div/ul/li[2]/a/@style")[0].strip()
                item["CVE-ID"] = detail_html.xpath("//div/div/div/div/ul/li[3]/a")[0].text.strip()
                item["漏洞类型"] = detail_html.xpath("//div/div/div/div/ul/li[4]/a")[0].text.strip()
                item["发布时间"] = detail_html.xpath("//div/div/div/div/ul/li[5]/a")[0].text.strip()
                item["威胁类型"] = detail_html.xpath("//div/div/div/div/ul/li[6]/a")[0].text.strip()
                item["更新时间"] = detail_html.xpath("//div/div/div/div/ul/li[7]/a")[0].text.strip()
                item["厂商"] = detail_html.xpath("//div/div/div/div/ul/li[8]/a")[0].text.strip() if detail_html.xpath("//div/div/div/div/ul/li[8]/a") else ""
                item["漏洞来源"] = detail_html.xpath("//div/div/div/div/ul/li[9]/a")[0].text.strip() if detail_html.xpath("//div/div/div/div/ul/li[9]/a") else ""
                item["漏洞简介"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj']/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj']/p") else ""
                item["漏洞公告"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][1]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][1]/p") else ""
                item["参考网址"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][2]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][2]/p") else ""
                item["受影响实体"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][3]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][3]/p") else ""
                item["补丁"] = "".join([i.text.strip() for i in detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][4]/p")]) if detail_html.xpath("//div/div/div/div[@class='d_ldjj m_t_20'][4]/p") else ""
                print(item)
            except:
                traceback.print_exc()
            finally:
                item_list.append(item)
        return item_list

    def run(self):
        for i in range(1, 10):
            url_1 = self.start_url.format(1)
            html = self.get_content(url_1)
            vul_list = self.get_detail(html)
            print(len(vul_list))
            print(vul_list)
            time.sleep(random.randint(5, 10))


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
            # item = {}
            item = OrderedDict()
            ics_temp = detail_html.xpath("//div[@id='ncas-header']/h1")[0].text.strip()
            item["ICS Advisory-ID"] = ics_temp.split("(")[-1].strip(")")
            item["title"] = detail_html.xpath("//div[@id='ncas-header']/h2")[0].text.strip()
            item["CVSS v3"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[1]//text()")[0].strip()
            # item["ATTENTION"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[2]/text()")[0].strip()
            # item["Vendor"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[3]/text()")[0].strip()
            # item["Equipment"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[4]/text()")[0].strip()
            # item["Vulnerabilities"] = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[5]/text()")[0].strip()
            """
            CVSS v3 2.7
            ATTENTION: Exploitable remotely/low skill level to exploit
            Vendor: Quest
            Equipment: KACE Systems Management Appliance (SMA)
            Vulnerability: Improper Input Validation
            """

            overview_cont_list1 = detail_html.xpath("//div[@id='ncas-content']/div[1]//text()")
            overview_cont_list = [i.strip() for i in list(filter(not_empty, overview_cont_list1))]
            print(overview_cont_list)
            
            ATTENTION_start = overview_cont_list.index("ATTENTION:") if "ATTENTION:" in overview_cont_list else 1
            vender_start = overview_cont_list.index("Vendor:") if "Vendor:" in overview_cont_list else ATTENTION_start+2
            Equipment_start = overview_cont_list.index("Equipment:") if "Equipment:" in overview_cont_list else vender_start+2
            Vulnerability_start = overview_cont_list.index("Vulnerability:") if "Vulnerability:" in overview_cont_list else Equipment_start+2
            Vulnerability_end = overview_cont_list.index("2. RISK EVALUATION") if "2. RISK EVALUATION" in overview_cont_list else Vulnerability_start+2
            item["ATTENTION"] = overview_cont_list[ATTENTION_start+1: vender_start]
            item["Vendor"] = overview_cont_list[vender_start+1: Equipment_start]
            item["Equipment"] = overview_cont_list[Equipment_start+1: Vulnerability_start]
            item["Vulnerabilities"] = overview_cont_list[Vulnerability_start+1: Vulnerability_end]

            item["RISK EVALUATION"] = detail_html.xpath("//div[@id='ncas-content']/div[1]/p[1]")[0].text.strip()
            
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
    # cnvd = CnvdSpider()
    # cnvd.run()
    # cnnvd = CnnvdSpider()
    # cnnvd.run()
    # icsa = IcsaSpider()
    # icsa.run()
    cve = CveSpider()
    cve.run()
