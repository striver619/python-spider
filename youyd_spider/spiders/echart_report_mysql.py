
import time
from youyd_spider.utils.dbConnPool import MyPymysqlPool
from pyecharts.charts import Pie
from pyecharts import options
from snapshot_phantomjs import snapshot as driver
from pyecharts.render import make_snapshot
import sys

"""
邮件
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


timestamp = "%s.png" % int(round(time.time()*1000))


def senEmail(params):

    host = 'smtp.163.com'
    port = 465
    sender = 'lautomn@163.com'
    pwd = 'RBRAMHZDFQHNNTUE'
    receiver = '1831682775@qq.com'

    msg = MIMEMultipart()
    text_msg = MIMEText("饼图",
                        _subtype='plain',
                        _charset="utf8")
    msg.attach(text_msg)

    file_content = open(timestamp, "rb")
    msg = MIMEMultipart()
    # text_msg = MIMEText("每日短信发送统计",
    #                     _subtype='plain',
    #                     _charset="utf8")
    # msg.attach(text_msg)

    datas = ""
    for data in params:
        datas += ("""<tr>
                            <td text-align="center">%s </td>
                            <td>%s </td>
                       </tr>""" % (data['days'].decode(), data['total']))

    text_msg1 = MIMEText("""
                    <table color="CCCC33" width="800" border="1" cellspacing="0" cellpadding="5" text-align="center">
                            <tr>
                                    <td text-align="center">day</td>
                                    <td text-align="center">total</td>
                            </tr>
                            %s
                    </table>""" % datas,
                         _subtype='HTML',
                         _charset="utf8")
    msg.attach(text_msg1)

    file_msg = MIMEApplication(file_content.read())
    file_msg.add_header('content-disposition',
                        'attachment',
                        filename= timestamp)
    msg.attach(file_msg)
    file_content.close()

    msg['subject'] = '通知：每日数据监测'
    msg['from'] = sender
    msg['to'] = receiver
    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        print('Done.sent email success')
    except smtplib.SMTPException as e:
        print('Error.sent email fail', e)


def saveChart(params):
    """
    https://zhuanlan.zhihu.com/p/133111970
    """
    datas = []
    for data in params:
        datas.append(tuple(data.values()))

    print(params)
    print(datas)

    pie = Pie()
    pie.add(
        series_name='统计',
        data_pair=datas,
        radius=['30%', '70%'],
        rosetype='radius'
    )
    # 设置数据显示的格式
    pie.set_series_opts(label_opts=options.LabelOpts(formatter='{b}：{c}'))
    pie.set_global_opts(title_opts=options.TitleOpts(title='统计'))

    make_snapshot(driver, pie.render(), timestamp)


# def start():
#     """
#     npm install -g phantomjs-prebuilt
#     pip install pyecharts-snapshot
#     统计每日短信发送量。
#     """
#     mysql = MyPymysqlPool("mysql")
#     totalSql = "SELECT DATE_FORMAT(mea.created_date,'%Y%m%d') days ,count(1) + aaa.count as total FROM message mea LEFT JOIN (SELECT DATE_FORMAT(created_date,'%Y%m%d') days,count(1) count FROM information WHERE result_code = '1' group by days ORDER BY days)aaa on aaa.days = DATE_FORMAT(mea.created_date,'%Y%m%d')  WHERE vendor = 'mx' AND result_code = '1' group by DATE_FORMAT(mea.created_date,'%Y%m%d') ORDER BY DATE_FORMAT(mea.created_date,'%Y%m%d');"
#     result = mysql.getAll(totalSql)
#     mysql.dispose()
#
#     print("subtask running---------------->")
#     saveChart(result)
#     senEmail(result)
#     print("subtask Done---------------->")
#
#
# schedule.every().day.at('14:11').do(start)
# while True:
#     schedule.run_pending()
#     time.sleep(1)


if __name__ == '__main__':
    """
    npm install -g phantomjs-prebuilt
    pip install pyecharts-snapshot
    统计每日短信发送量。（提交条数）;
    发送到邮箱以echart方式展示；
    此文件不以 Scrapy 方式执行；
    """
    mysql = MyPymysqlPool("echart_report_mysql")
    totalSql = """
            SELECT
                DATE_FORMAT( mea.created_date, '%Y%m%d' ) days,
                count( 1 ) + aaa.count AS total 
            FROM
                message mea
                LEFT JOIN ( SELECT DATE_FORMAT( created_date, '%Y%m%d' ) days, count( 1 ) count FROM information WHERE platform_type = '1' GROUP BY days ORDER BY days ) aaa ON aaa.days = DATE_FORMAT( mea.created_date, '%Y%m%d' ) 
            WHERE
                vendor = 'mx' 
            GROUP BY
                DATE_FORMAT( mea.created_date, '%Y%m%d' ) 
            ORDER BY
                DATE_FORMAT( mea.created_date, '%Y%m%d' );
                """
    result = mysql.getAll(totalSql)
    mysql.dispose()

    print("subtask running---------------->")
    saveChart(result)
    senEmail(result)
    print("subtask Done---------------->")

    sys.exit()