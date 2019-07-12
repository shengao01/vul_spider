# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import time
import traceback
import logging
import pymysql
pymysql.install_as_MySQLdb()
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class DbProxy(object):
    def __init__(self):
        self.connect_status=1
        self.reconnect_times=0
        self.cur=None
        try:
            self.conn=pymysql.connect(host='192.168.81.4', port=3306, user='root', passwd='123456', db='vul_info')
        except:
            logging.error('connet mysql error')
            logging.error(traceback.format_exc())
            self.connect_status=0
            return
        self.cur=self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()
        return

    def check_db_errno(self, errno):
        if errno == 29 or errno == 1146 or errno == 1194 or errno == 1030 or errno == 1102 or errno == 1712:
            return True
        return False

    def write_db(self, sqlstr):
        try:
            self.cur.execute(sqlstr)
        except pymysql.Error as e:
            try:
                errno=e.args[0]
                errinfo=e.args[1]
                logging.error("write_db error, cmd=%s,errno=[%d],errinfo=%s", sqlstr, errno, errinfo)
            except IndexError:
                logging.error('write_db error')
                logging.error(traceback.format_exc())

            if self.reconnect_times < 5:
                self.reconnect_times+=1
                res=self.reconnect()
                # res = self.write_db(sqlstr)
                if res == 0:
                    self.reconnect_times=0
                else:
                    time.sleep(0.2)
                return res
            else:
                self.reconnect_times=0
                return 1
        try:
            self.conn.commit()
        except:
            logging.error("conn commit fail!!")
            logging.error(traceback.format_exc())
        return 0

    def read_db(self, sqlstr):
        try:
            self.cur.execute(sqlstr)
            rows=self.cur.fetchall()
        except pymysql.Error as e:
            try:
                errno=e.args[0]
                errinfo=e.args[1]
                if self.check_db_errno(errno):
                    logging.error("make mysql_check_error.flag")
                logging.error("read_db error: cmd=%s,errno=[%d],errinfo=%s", sqlstr, errno, errinfo)
            except IndexError:
                logging.error('read_db error')
                logging.error(traceback.format_exc())

            if self.reconnect_times < 5:
                self.reconnect_times+=1
                self.reconnect()
                res, rows=self.read_db(sqlstr)
                if res == 0:
                    self.reconnect_times=0
                else:
                    time.sleep(0.2)
                return res, rows
            else:
                self.reconnect_times=0
                rows=[]
                return 1, rows
        return 0, rows

    def execute(self, sqlstr):
        try:
            self.cur.execute(sqlstr)
        except pymysql.Error as e:
            try:
                errno=e.args[0]
                errinfo=e.args[1]
                if self.check_db_errno(errno):
                    logging.error("make mysql_check_error.flag")
                logging.error("execute error: cmd=%s,errno=[%d],errinfo=%s", sqlstr, errno, errinfo)
            except IndexError:
                logging.error("execute error, cmd=%s", sqlstr)
                logging.error(traceback.format_exc())

            if self.reconnect_times < 5:
                self.reconnect_times+=1
                self.reconnect()
                res, self.cur=self.execute(sqlstr)
                if res == 0:
                    self.reconnect_times=0
                return res, self.cur
            else:
                self.reconnect_times=0
                return 1, self.cur
        return 0, self.cur

    def get_connect_status(self):
        return self.connect_status

    def reconnect(self):
        try:
            self.cur.close()
            self.conn.close()
        except:
            logging.error(traceback.format_exc())
        try:
            self.conn=pymysql.connect(host='192.168.81.4', port=3306, user='root', passwd='123456', db='vul_info')
        except:
            logging.error('connet mysql error')
            logging.error(traceback.format_exc())
            self.connect_status=0
            return
        self.cur=self.conn.cursor()
        self.connect_status=1
        logging.info("DbProxy reconnect ok")


"""
create table `icsa_url` (
`cid` int(11) NOT NULL AUTO_INCREMENT,
`href` varchar(128),
`tmsp` varchar(64),
`res1` varchar(64),
`res2` varchar(64),
PRIMARY KEY (`cid`),
UNIQUE KEY `href` (`href`)
) ENGINE=MyISAM AUTO_INCREMENT=5206 DEFAULT CHARSET=utf8;

create table `cnvd_url` (
`cid` int(11) NOT NULL AUTO_INCREMENT,
`href` varchar(128),
`tmsp` varchar(64),
`res1` varchar(64),
`res2` varchar(64),
PRIMARY KEY (`cid`),
UNIQUE KEY `href` (`href`)
) ENGINE=MyISAM AUTO_INCREMENT=5206 DEFAULT CHARSET=utf8;

create table `cnnvd_url` (
`cid` int(11) NOT NULL AUTO_INCREMENT,
`href` varchar(128),
`tmsp` varchar(64),
`res1` varchar(64),
`res2` varchar(64),
PRIMARY KEY (`cid`),
UNIQUE KEY `href` (`href`)
) ENGINE=MyISAM AUTO_INCREMENT=5206 DEFAULT CHARSET=utf8;

create table `cve_url` (
`cid` int(11) NOT NULL AUTO_INCREMENT,
`href` varchar(128),
`tmsp` varchar(64),
`res1` varchar(64),
`res2` varchar(64),
PRIMARY KEY (`cid`),
UNIQUE KEY `href` (`href`)
) ENGINE=MyISAM AUTO_INCREMENT=5206 DEFAULT CHARSET=utf8;

"""
