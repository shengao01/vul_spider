# -*- coding: utf-8 -*-
import time
import random
import traceback
import requests
import json
# import codecs
# import chardet
from lxml import etree
from selenium import webdriver
from collections import OrderedDict
from common_func import DbProxy


def not_empty(s):
    return s and s.strip()


class BaseSpider(object):
    def __init__(self):
        super(BaseSpider, self).__init__()
        self.db = DbProxy()
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

    def get_content(self, url):
        resp = requests.get(url, headers=self.headers).content.decode()
        html = etree.HTML(resp)
        return html

    def write_file(self, filename, cont):
        item = cont.encode().decode('unicode_escape')
        with open(filename, "a+", encoding='utf-8') as f:
            f.write(item + "\n")


class CnvdSpider(BaseSpider):
    def __init__(self):
        super(CnvdSpider, self).__init__()
        self.start_url = "https://ics.cnvd.org.cn/?max=20&offset={}"

    def parse_detail(self, html):
        list = html.xpath("//tbody[@id='tr']/tr")
        item_list = []
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        # driver = webdriver.PhantomJS()
        for a in list:
            href = a.xpath(".//a/@href")[0]
            print(href)  # 详情页入口
            # judge if exist in db
            select_str = "select count(*) from cnvd_url where href='{}'".format(href)
            res, rows = self.db.read_db(select_str)
            if res == 0 and rows:
                if rows[0][0] > 0:
                    return "end"
            # href = "https://www.cnvd.org.cn/flaw/show/CNVD-2019-21242"
            driver.get(href)
            time.sleep(5)
            try:
                item = {}
                # item = OrderedDict()
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
                item["CVE-ID"] = "".join(temp_list[cveid_start+1: description_start])
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
            except ValueError:
                driver.close()
                driver = webdriver.Chrome()
                driver.get(href)
                time.sleep(10)
                item = {}
                # item = OrderedDict()
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
                item["CVE-ID"] = "".join(temp_list[cveid_start+1: description_start])
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
                # print(item)
            finally:
                item_list.append(item)
                item = json.dumps(item)
                item = item.replace("\\n", "")
                self.write_file("v.log", item)
                sql_str = "insert into cnvd_url(href) values('{}')".format(href)
                self.db.write_db(sql_str)
                # traceback.print_exc()
        driver.close()
        # return item_list

    def run(self):
        for i in range(0, 5):
            url = self.start_url.format(i*20)
            html = self.get_content(url)
            item = self.parse_detail(html)
            if item == "end":
                break


class CnnvdSpider(BaseSpider):
    def __init__(self):
        super(CnnvdSpider, self).__init__()
        self.start_url = "http://www.cnnvd.org.cn/web/vulnerability/querylist.tag?pageno={}"
        self.part_url = "http://www.cnnvd.org.cn"

    def get_detail(self, html):
        url_list = html.xpath("//div[@class='list_list']//li/div/a/@href")
        for a in url_list:
            detail_url = self.part_url + a
            # detail_url = "http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201907-368"
            print(detail_url)
            # judge if exist in db
            select_str = "select count(*) from cnnvd_url where href='{}'".format(detail_url)
            res, rows = self.db.read_db(select_str)
            if res == 0 and rows:
                if rows[0][0] > 0:
                    return "end"
            item = {}
            # item = OrderedDict()
            try:
                detail_html = self.get_content(detail_url)
                cnnvd_id = detail_html.xpath("//div/div/div/div/ul/li/span")[0].text.strip()
                item["CNNVD编号"] = cnnvd_id.split("：")[-1].strip()
                item["危害等级"] = detail_html.xpath("//div/div/div/div/ul/li[2]/a")[0].text.strip() if detail_html.xpath("//div/div/div/div/ul/li[2]/a")[0].text.strip() else "未知"
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
                # print(item)
            except IndexError:
                time.sleep(10)
                detail_html = self.get_content(detail_url)
                cnnvd_id = detail_html.xpath("//div/div/div/div/ul/li/span")[0].text.strip()
                item["CNNVD编号"] = cnnvd_id.split("：")[-1].strip()
                item["危害等级"] = detail_html.xpath("//div/div/div/div/ul/li[2]/a")[0].text.strip() if detail_html.xpath("//div/div/div/div/ul/li[2]/a")[0].text.strip() else "未知"
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
                # print(item)
            except:
                traceback.print_exc()
            finally:
                # write file and db
                item = json.dumps(item)
                self.write_file("v.log", item)
                sql_str = "insert into cnnvd_url(href) values('{}')".format(detail_url)
                self.db.write_db(sql_str)

    def run(self):
        for i in range(1, 11):
            url_1 = self.start_url.format(i)
            html = self.get_content(url_1)
            res = self.get_detail(html)
            if res == "end":
                break
            time.sleep(random.randint(5, 10))


class IcsaSpider(BaseSpider):
    def __init__(self):
        super(IcsaSpider, self).__init__()
        self.start_url = "https://www.us-cert.gov/ics/advisories?page={}"
        self.start_alert_url = "https://www.us-cert.gov/ics/alerts?page={}"
        self.part_url = "https://www.us-cert.gov"

    def get_detail(self, html):
        href_list = html.xpath("//ul//span/a/@href")
        for a in href_list:
            detail_url = self.part_url + a
            # detail_url = "https://www.us-cert.gov/ics/advisories/icsa-19-178-01"
            print(detail_url)
            # judge if exist in db
            select_str = "select count(*) from icsa_url where href='{}'".format(detail_url)
            res, rows = self.db.read_db(select_str)
            if res == 0 and rows:
                if rows[0][0] > 0:
                    return "end"
            item={}
            # item = OrderedDict()
            detail_html = self.get_content(detail_url)
            ics_temp = detail_html.xpath("//div[@id='ncas-header']/h1")[0].text.strip()
            item["ICS-Advisory-ID"] = ics_temp.split("(")[-1].strip(")")
            item["title"] = detail_html.xpath("//div[@id='ncas-header']/h2")[0].text.strip()
            # CVSS = detail_html.xpath("//div[@id='ncas-content']/div/ul[1]/li[1]//text()")[0].strip()
            # item["CVSS v3"] = CVSS[8:]
            item["CVSS v3"] = ""
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
            # print(overview_cont_list)
            for i, cont in enumerate(overview_cont_list):
                if "UPDATE INFORMATION" in cont or "REPOSTED INFORMATION" in cont:
                    overview_cont_list[i] = "2. UPDATE INFORMATION"
                elif "ATTENTION" in cont:
                    if len(cont) > 10:
                        item["ATTENTION"] = cont.strip("ATTENTION:").strip()
                    else:
                        overview_cont_list[i] = "ATTENTION:"
                elif "Vendor" in cont:
                    if len(cont) > 7:
                        item["Vendor"]=cont.strip("Vendor:").strip()
                    else:
                        overview_cont_list[i] = "Vendor:"
                elif "Equipment" in cont:
                    if len(cont) > 10:
                        item["Equipment"]=cont.strip("Equipment:").strip()
                    else:
                        overview_cont_list[i] = "Equipment:"
                elif "Vulnerabilities" in cont:
                    if len(cont) > 16:
                        item["Vulnerabilities"]=cont.strip("Vulnerabilities:").strip()
                    else:
                        overview_cont_list[i] = "Vulnerabilities:"
                elif "RISK EVALUATION" in cont:
                    overview_cont_list[i] = "2. RISK EVALUATION"
                elif "AFFECTED PRODUCTS" in cont:
                    overview_cont_list[i] = "3.1 AFFECTED PRODUCTS"
                elif "VULNERABILITY OVERVIEW" in cont:
                    overview_cont_list[i] = "3.2 VULNERABILITY OVERVIEW"
                elif "BACKGROUND" in cont:
                    overview_cont_list[i] = "3.3 BACKGROUND"
                elif "RESEARCHER" in cont:
                    overview_cont_list[i] = "3.4 RESEARCHER"
                elif "MITIGATION" in cont:
                    overview_cont_list[i] = "4. MITIGATIONS"

            if "ATTENTION:" in overview_cont_list:
                ATTENTION_start = overview_cont_list.index("ATTENTION:")
                vender_start = overview_cont_list.index("Vendor:") if "Vendor:" in overview_cont_list else ATTENTION_start+2
                Equipment_start = overview_cont_list.index("Equipment:") if "Equipment:" in overview_cont_list else vender_start+2
                Vulnerability_start = overview_cont_list.index("Vulnerability:") if "Vulnerability:" in overview_cont_list else Equipment_start+2
                Vulnerability_end = overview_cont_list.index("2. RISK EVALUATION") if "2. RISK EVALUATION" in overview_cont_list else Vulnerability_start+2
                item["CVSS v3"] = overview_cont_list[ATTENTION_start-1][8:]
                item["ATTENTION"] = "".join(overview_cont_list[ATTENTION_start+1: vender_start]).strip(":")
                item["Vendor"] = "".join(overview_cont_list[vender_start+1: Equipment_start]).strip(":")
                item["Equipment"] = "".join(overview_cont_list[Equipment_start+1: Vulnerability_start]).strip(":")
                item["Vulnerabilities"] = "".join(overview_cont_list[Vulnerability_start+1: Vulnerability_end]).replace("\xa0", "")
            elif "Vendor:" in overview_cont_list:
                vender_start = overview_cont_list.index("Vendor:")
                Equipment_start = overview_cont_list.index("Equipment:") if "Equipment:" in overview_cont_list else vender_start+2
                Vulnerability_start = overview_cont_list.index("Vulnerability:") if "Vulnerability:" in overview_cont_list else Equipment_start+2
                Vulnerability_end = overview_cont_list.index("2. RISK EVALUATION") if "2. RISK EVALUATION" in overview_cont_list else Vulnerability_start+2
                item["CVSS v3"] = overview_cont_list[vender_start-1][8:]
                item["ATTENTION"] = ""
                item["Vendor"] = "".join(overview_cont_list[vender_start+1: Equipment_start]).strip(":")
                item["Equipment"] = "".join(overview_cont_list[Equipment_start+1: Vulnerability_start]).strip(":")
                item["Vulnerabilities"] = "".join(overview_cont_list[Vulnerability_start+1: Vulnerability_end]).replace("\xa0", "")
            else:
                if "CVSS v3" not in item:
                    item["CVSS v3"] = ""
                if "ATTENTION" not in item:
                    item["ATTENTION"] = ""
                if "Vendor" not in item:
                    item["Vendor"] = ""
                if "Equipment" not in item:
                    item["Equipment"] = ""
                if "Vulnerabilities" not in item:
                    item["Vulnerabilities"] = ""

            try:
                risk_start = overview_cont_list.index("2. RISK EVALUATION")
                aftprd_start = overview_cont_list.index("3.1 AFFECTED PRODUCTS")
                overview_start = overview_cont_list.index("3.2 VULNERABILITY OVERVIEW") if "3.2 VULNERABILITY OVERVIEW" in overview_cont_list else aftprd_start+2
                overview_end = overview_cont_list.index("3.3 BACKGROUND")
                background_end = overview_cont_list.index("3.4 RESEARCHER") if "3.4 RESEARCHER" in overview_cont_list else overview_end + 2
                res_end = overview_cont_list.index("4. MITIGATIONS")
                item["RISK EVALUATION"] = " ".join(overview_cont_list[risk_start+1: aftprd_start-1])
                item["AFFECTED PRODUCTS"] = " ".join(overview_cont_list[aftprd_start+1: overview_start])
                item["VULNERABILITY OVERVIEW"] = " ".join(overview_cont_list[overview_start+1: overview_end])
                item["BACKGROUND"] = " ".join(overview_cont_list[overview_end+1: background_end])
                item["RESEARCHER"] = " ".join(overview_cont_list[background_end+1: res_end])
                item["MITIGATIONS"] = " ".join(overview_cont_list[res_end + 1:]).replace("\xa0", "")
            except ValueError:
                if "ICSMA" in detail_url:
                    aftprd_start = overview_cont_list.index("3.1 AFFECTED PRODUCTS")
                    risk_start = overview_cont_list.index("IMPACT")
                    back_start = overview_cont_list.index("3.3 BACKGROUND")
                    overview_start = overview_cont_list.index("3.2 VULNERABILITY OVERVIEW")
                    mit_start = overview_cont_list.index("4. MITIGATIONS")
                    detail_start = overview_cont_list.index("VULNERABILITY DETAILS") if "VULNERABILITY DETAILS" in overview_cont_list else mit_start
                    item["AFFECTED PRODUCTS"] = " ".join(overview_cont_list[aftprd_start + 1: risk_start])
                    item["RISK EVALUATION"] = " ".join(overview_cont_list[risk_start + 1: back_start])
                    item["BACKGROUND"] = " ".join(overview_cont_list[back_start + 1: overview_start-1])
                    item["VULNERABILITY OVERVIEW"] = " ".join(overview_cont_list[overview_start + 1: detail_start])
                    item["MITIGATIONS"] = " ".join(overview_cont_list[mit_start + 1:]).replace("\xa0", "")

                elif "IMPACT" in overview_cont_list:
                    aftprd_start = overview_cont_list.index("3.1 AFFECTED PRODUCTS")
                    risk_start = overview_cont_list.index("IMPACT")
                    mit_start = overview_cont_list.index("4. MITIGATIONS")
                    overview_start = overview_cont_list.index("3.2 VULNERABILITY OVERVIEW")
                    res_start = overview_cont_list.index("3.4 RESEARCHER")
                    back_start = overview_cont_list.index("3.3 BACKGROUND")
                    item["AFFECTED PRODUCTS"] = " ".join(overview_cont_list[aftprd_start + 1: risk_start])
                    item["RISK EVALUATION"] = " ".join(overview_cont_list[risk_start + 1: mit_start - 1])
                    item["MITIGATIONS"] = " ".join(overview_cont_list[mit_start + 1: overview_start]).replace("\xa0", "")
                    item["VULNERABILITY OVERVIEW"] = " ".join(overview_cont_list[overview_start + 1: res_start])
                    item["RESEARCHER"] = " ".join(overview_cont_list[res_start + 1: back_start])
                    item["BACKGROUND"] = " ".join(overview_cont_list[back_start + 1:])
            # print(item)
            item = json.dumps(item)
            item = item.replace("\\n", "")
            self.write_file("v.log", item)
            sql_str = "insert into icsa_url(href) values('{}')".format(detail_url)
            self.db.write_db(sql_str)

    def get_alert_detail(self,html):
        href_list = html.xpath("//ul//span/a/@href")
        for a in href_list:
            detail_url = self.part_url + a
            print(detail_url)
            # judge if exist in db
            select_str = "select count(*) from icsa_url where href='{}'".format(detail_url)
            res, rows = self.db.read_db(select_str)
            if res == 0 and rows:
                if rows[0][0] > 0:
                    return "end"
            item = {}
            # item = OrderedDict()
            detail_html = self.get_content(detail_url)
            ics_temp = detail_html.xpath("//div[@id='ncas-header']/h1")[0].text.strip()
            item["ICS-Alerts-ID"] = ics_temp.split("(")[-1].strip(")")
            item["title"] = detail_html.xpath("//div[@id='ncas-header']/h2")[0].text.strip()
            overview_cont_list1 = detail_html.xpath("//div[@id='ncas-content']/div//text()")
            overview_cont_list = [i.strip() for i in list(filter(not_empty, overview_cont_list1))]
            # print(overview_cont_list)
            for i, cont in enumerate(overview_cont_list):
                if "SUMMARY" in cont or "Summary" in cont or "OVERVIEW" in cont or "Overview" in cont:
                    overview_cont_list[i] = "SUMMARY"
                elif "MITIGATION" in cont or "Mitigation" in cont:
                    overview_cont_list[i] = "MITIGATION"
                elif "Follow-Up" in cont or "FOLLOW-UP" in cont:
                    overview_cont_list[i] = "FOLLOW-UP"
            if "FOLLOW-UP" in overview_cont_list:
                item["SUMMARY"] = " ".join(overview_cont_list[overview_cont_list.index("SUMMARY") + 1: overview_cont_list.index("FOLLOW-UP")])
                if "MITIGATION" in overview_cont_list:
                    item["MITIGATION"] = " ".join(overview_cont_list[overview_cont_list.index("MITIGATION") + 1:])
                else:
                    item["MITIGATION"] = ""
            elif "MITIGATION" in overview_cont_list:
                item["SUMMARY"] = " ".join(overview_cont_list[overview_cont_list.index("SUMMARY") + 1: overview_cont_list.index("MITIGATION")])
                item["MITIGATION"] = " ".join(overview_cont_list[overview_cont_list.index("MITIGATION") + 1:])
            else:
                item["SUMMARY"] = " ".join(overview_cont_list[overview_cont_list.index("SUMMARY") + 1:])
                item["MITIGATION"] = ""

            # print(item)
            item = json.dumps(item)
            item = item.replace("\\n", "")
            self.write_file("v.log", item)
            sql_str = "insert into icsa_url(href) values('{}')".format(detail_url)
            self.db.write_db(sql_str)

    def run(self):
        for i in range(4):
            url = self.start_url.format(i)
            html = self.get_content(url)
            res = self.get_detail(html)
            if res == "end":
                break
            time.sleep(6)
        for i in range(4):
            url = self.start_alert_url.format(i)
            html = self.get_content(url)
            res = self.get_alert_detail(html)
            if res == "end":
                break
            time.sleep(5)


class CveSpider(BaseSpider):
    def __init__(self):
        super(CveSpider, self).__init__()
        self.start_url = "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-{}-{}"
        self.end = "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-{}-{}"

    def get_detail(self, url):
        item = {}
        # item = OrderedDict()
        html = self.get_content(url)
        if not html.xpath("//tr/td//h2"):
            return "end"
        item["CVE-ID"] = html.xpath("//tr/td//h2")[0].text.strip()
        item["Description"] = "".join(list(filter(not_empty, html.xpath("//div[@id='GeneratedTable']//tr[4]//text()"))))
        if "RESERVED" in item["Description"]:
            return "RESERVED"
        item["References"] = "".join(list(filter(not_empty, html.xpath("//div[@id='GeneratedTable']//tr[7]//text()"))))
        item["Assigning CNA"] = html.xpath("//div[@id='GeneratedTable']//tr[9]/td[1]//text()")[0].strip()
        item["Date Entry Created"] = html.xpath("//div[@id='GeneratedTable']//tr[11]/td[1]//text()")[0].strip()
        item["Phase (Legacy)"] = html.xpath("//div[@id='GeneratedTable']//tr[13]/td[1]//text()")[0].strip() if html.xpath("//div[@id='GeneratedTable']//tr[13]/td[1]//text()") else ""
        item["Votes (Legacy)"] = html.xpath("//div[@id='GeneratedTable']//tr[15]/td[1]//text()")[0].strip() if html.xpath("//div[@id='GeneratedTable']//tr[15]/td[1]//text()") else ""
        item["Comments (Legacy)"] = html.xpath("//div[@id='GeneratedTable']//tr[17]/td[1]//text()")[0].strip() if html.xpath("//div[@id='GeneratedTable']//tr[17]/td[1]//text()") else ""
        item["Proposed (Legacy)"] = html.xpath("//div[@id='GeneratedTable']//tr[19]/td[1]//text()")[0].strip() if html.xpath("//div[@id='GeneratedTable']//tr[19]/td[1]//text()") else ""
        # print(item)
        item = json.dumps(item)
        item = item.replace("\\n", "")
        self.write_file("v.log", item)
        sql_str = "insert into cve_url(href) values('{}')".format(url)
        self.db.write_db(sql_str)

    def run(self):
        # year_list = [2019]
        # for year in year_list:
        sql_str = "select href from cve_url order by cid desc limit 1"
        res, row = self.db.read_db(sql_str)
        if res == 0 and row:
            start = int(row[0][0].split("-")[-1]) + 1
        else:
            start = 13500
        print(start)
        for num in range(start, 30000):
            if num < 1000:
                num = "%04d" % num
            url = self.start_url.format(2019, num)
            print(url)
            res = self.get_detail(url)
            if res == "end":
                break
            time.sleep(1)


if __name__ == '__main__':
    try:
        cnnvd = CnnvdSpider()
        cnnvd.run()
    except:
        print("get cnnvd_info run error...")
        traceback.print_exc()
    try:
        cnvd = CnvdSpider()
        cnvd.run()
    except:
        print("get cnvd_info run error...")
        traceback.print_exc()
    try:
        icsa = IcsaSpider()
        icsa.run()
    except:
        print("get icsa_info run error...")
        traceback.print_exc()
    try:
        cve = CveSpider()
        cve.run()
    except:
        print("get cve_info run error...")
        traceback.print_exc()
