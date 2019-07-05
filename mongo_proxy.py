#coding:utf-8
import pymongo


class Dbproxy(object):
    def __init__(self):
        super(Dbproxy, self).__init__()
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.vul_db = self.client["vul_db"]
        self.collections = self.vul_db["vul_db"]

    def insert_db(self, cont):
        self.collections.insert(cont)

    def insert_one(self, cont):
        self.collections.insert_one(cont)

    def insert_many(self, cont_li):
        self.collections.insert_many(cont_li)


if __name__ == '__main__':
    db = Dbproxy()
    al = [{'CNNVD编号': 'CNNVD-201907-284', '危害等级': 'color:#4095cc;cursor:pointer;', 'CVE-ID': 'CVE-2019-13294', '漏洞类型': '其他', '发布时间': '2019-07-04', '威胁类型': '', '更新时间': '2019-07-05', '厂商': '', '漏洞来源': '', '漏洞简介': 'AROX School-ERP Pro是一套基于Web的学校管理系统。该系统包括课程管理、考勤管理、财务管理、人力资源管理和考试管理等功能。AROX School-ERP Pro中存在安全漏洞，该漏洞源于import_stud.php和upload_fille.php文件没有进行会话控制。攻击者可利用该漏洞在系统上执行命令。', '漏洞公告': '目前厂商已发布升级补丁以修复漏洞，详情请关注厂商主页：http://arox.in/', '参考网址': '来源:www.exploit-db.com链接:https://www.exploit-db.com/exploits/46999来源:www.pentest.com.tr链接:http://www.pentest.com.tr/exploits/AROX-School-ERP-Pro-Unauthenticated-RCE-Metasploit.html来源:nvd.nist.gov链接:https://nvd.nist.gov/vuln/detail/CVE-2019-13294', '受影响实体': '', '补丁': ''},{'CNNVD编号': 'CNNVD-201907-284', '危害等级': 'color:#4095cc;cursor:pointer;', 'CVE-ID': 'CVE-2019-13294', '漏洞类型': '其他', '发布时间': '2019-07-04', '威胁类型': '', '更新时间': '2019-07-05', '厂商': '', '漏洞来源': '', '漏洞简介': 'AROX School-ERP Pro是一套基于Web的学校管理系统。该系统包括课程管理、考勤管理、财务管理、人力资源管理和考试管理等功能。AROX School-ERP Pro中存在安全漏洞，该漏洞源于import_stud.php和upload_fille.php文件没有进行会话控制。攻击者可利用该漏洞在系统上执行命令。', '漏洞公告': '目前厂商已发布升级补丁以修复漏洞，详情请关注厂商主页：http://arox.in/', '参考网址': '来源:www.exploit-db.com链接:https://www.exploit-db.com/exploits/46999来源:www.pentest.com.tr链接:http://www.pentest.com.tr/exploits/AROX-School-ERP-Pro-Unauthenticated-RCE-Metasploit.html来源:nvd.nist.gov链接:https://nvd.nist.gov/vuln/detail/CVE-2019-13294', '受影响实体': '', '补丁': ''}]
    db.insert_many(al)
