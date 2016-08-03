# -*- coding:utf-8 -*-
# filename:TestPost
# 16/1/20 下午4:01

# 安装依赖包
# ---------------------------------------
# 云片网sdk
#  pip install yunpian-sdk-python
#  pip install pyquery
#  pip install
# ---------------------------------------

__author__ = 'bingone'
from yunpian.SmsOperator import SmsOperator
from yunpian.VoiceOperator import VoiceOperator
from yunpian.TplOperator import TplOperator
from yunpian.UserOperator import UserOperator
from yunpian.FlowOperator import FlowOperator
import sys
import json
from pyquery import PyQuery as pQuery # 从pyquery模块导入PyQuery类
import urllib2
import time, os, sched
import MySQLdb
import datetime

# 设置默认的编码
reload(sys)
sys.setdefaultencoding('utf-8')

# 日志文件名字
LOG_FILE_NAME = r"d:/log/novelsmstip.log"


# 写入日志
def write_log(filename = LOG_FILE_NAME,text="null"):
    curtime = time.strftime('%Y-%m-%d %X', time.localtime())
    print curtime + "\t" + text
    file = open(filename,'a')
    file.write(curtime + "\t" + text + "\n")
    file.close()

# 更新数据库记录
def update_db_row(title,updatetime,chapter):
    # 数据库配置信息
    conn = MySQLdb.connect(
            host='localhost',
            port = 3306,
            user='root',
            passwd='123456',
            db ='ot_statis',
            charset='utf8',
            )
    cur = conn.cursor()

    # 查询数据
    sql = unicode("select id,name,chapter,updatetime from otstatis_noveseek order by id desc limit 1;")
    cur.execute(sql)
    # 获取一条数据
    row = cur.fetchone()

    bUpdate = False
    if (row is None) == False:
        print row
        logtext = u"判断条件 " + row[3].strftime('%Y-%m-%d %H:%M:%S') + " < " + updatetime
        write_log(LOG_FILE_NAME,logtext)

    if (row is None) or (row[3].strftime('%Y-%m-%d %H:%M:%S') < updatetime):
        bUpdate = True
    else:
        bUpdate = False

    if  bUpdate:
        #插入一条数据
        sql = "insert into otstatis_noveseek(name,chapter,updatetime) values('%s','%s','%s');" % (title,chapter,updatetime)
        sql = unicode(sql)
        print "执行SQL：" + sql
        # sql = u"insert into student(name,class,age) values('那','311 year 2 class','119');"
        row = cur.execute(sql)
        print "执行结果: ",row
    else:
        curtime = time.strftime('%Y-%m-%d %X', time.localtime())
        print curtime + "\t--------现在没有更新-------"
    # 关闭连接
    cur.close()
    # 提交数据
    conn.commit()
    conn.close()

    return bUpdate

# 自动检测小说更新，并发送短信
def auto_checknovelupdate():
    url = "http://www.biquge.la/book/14/"
    # url = "http://www.baidu.com"
    # 抓取网页
    page = urllib2.urlopen(url)
    # 解码
    text = unicode(page.read(), "gbk")
    # print text

    # 转成jQuery对象
    jQuery = pQuery(text)

    # 取出页面元素
    title = jQuery("#info>h1").html()
    updatetime = jQuery("#info>p:eq(2)").text()
    chapter = jQuery("#info>p:eq(3)>a").text()

    # 提取更新时间
    strTime = u"最后更新："
    pos_start = updatetime.find(strTime);
    time_len = len(strTime)
    pos_start = pos_start + time_len
    updatetime = updatetime[pos_start:]

    # 字符串转成时间
    t = datetime.datetime.strptime(updatetime, "%Y-%m-%d %H:%M")
    updatetime = t.strftime('%Y-%m-%d %H:%M:%S')
    # 更新数据库
    bUpdate = update_db_row(title,updatetime,chapter)

    smstext = ""
    if bUpdate:
         # 拼接短信内容
        smstext = u"【赢创天下科技】[%s]更新了,最后更新：%s,最新章节：%s" % (title,updatetime,chapter)
        write_log(LOG_FILE_NAME,smstext)
        send_smd(smstext)
    else:
        logtext = "--------不发送短信--------"
        write_log(LOG_FILE_NAME,logtext)

    return smstext

def send_smd(smdcontent):
    # 单条短信发送
    APIKEY = 'xxbxxxxxxxxxxxxxxxxx'
    smsOperator = SmsOperator(APIKEY)
    # 发送短信
    result = smsOperator.single_send({'mobile': 'xxxxxxxxxxxx', 'text': smdcontent})
    print json.dumps(result.content, ensure_ascii=False)
    json_result = json.dumps(result.content, ensure_ascii=False)
    # curtime = time.strftime('%Y-%m-%d %X', time.localtime())
    # open('d:/log/novelsmstip.log','a').write(curtime + "\t" + json_result + "\n")
    write_log(LOG_FILE_NAME,json_result)

# 检查小说是否更新，并发送短信
def checknovelupdate_sendsms():
    logtext = "--------检测更新--------"
    write_log(LOG_FILE_NAME,logtext)
    text = auto_checknovelupdate()


# 循环执行任务，inc表示间隔秒数
def re_exe(cmd, inc = 60):
    while True:
        # 执行循环任务
        checknovelupdate_sendsms()
        time.sleep(inc)

re_exe("",300)
# checknovelupdate_sendsms()
