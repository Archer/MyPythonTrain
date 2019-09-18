import configparser
import requests
import os
import time
import json
import sqlite3
from urllib.parse import quote

class MeiT():
    def __init__(self, user_name):
        # 读取配置信息
        self.config = configparser.RawConfigParser()
        self.configfile_path = r"meituan.config"
        self.config.read(self.configfile_path, encoding='UTF-8')
        self.sys_config_section = "sys"
        self.user_config_section = "mt_user_" + user_name
        self.log_pathdirs = self.config.get(self.sys_config_section, 'log_pathdirs')  # 日志目录
        self.db_name = self.config.get(self.sys_config_section, 'db_name')  # 数据库名称
        self.request_interval = self.config.getint(self.sys_config_section, 'request_interval')  # 请求间隔



    def init_db(self):
        # 初始化数据库
        if self.config.getint(self.sys_config_section, 'initialize_db') == 1:
            try:
                if os.path.exists(self.db_name):
                    os.remove(self.db_name)
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                # 创建t_comments表
                c.execute(''' create table t_comments(
                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                comment_id varchar,
                                                shop_id varchar,
                                                username varchar,
                                                ship_score int,
                                                comment varchar,
                                                ctime int,
                                                utime int,
                                                ship_time int,
                                                order_comment_score int,
                                                food_comment_score int,
                                                delivery_comment_score int,
                                                remark varchar,
                                                scoreMeaning varchar,
                                                praise_food_list varchar
                                            ) ''')
                # 创建t_orders
                c.execute(''' create table t_orders(
                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                order_id varchar,
                                                user_id varchar,
                                                num int,
                                                order_time int,
                                                confirm_time int,
                                                utime int,
                                                privacy_phone varchar,
                                                backup_privacy_phones varchar,
                                                remark varchar,
                                                orderCopyContent varchar,
                                                recipient_phone varchar,
                                                recipient_bindedPhone varchar,
                                                recipient_name varchar
                                            ) ''')
                conn.commit()
                conn.close()
                self.config.set(self.sys_config_section, 'initialize_db', 0)
                with open(self.configfile_path, 'w', encoding='utf-8') as file:
                    self.config.write(file)
                self.log('初始化数据库成功！')
                time.sleep(self.request_interval)
            except Exception as e:
                self.log("Err:" + str(e))

    def add_log(self, dirs_path, text):
        text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ">>>>>" + text
        if not os.path.exists(dirs_path):
            os.makedirs(dirs_path)
        file_path = dirs_path+'/log_'+time.strftime('%Y_%m_%d', time.localtime())+'.txt'
        with open(file_path, 'a', encoding='utf-8') as file:
            file.writelines(text+'\r\n')
        print(text)
        return file_path

    def log(self, text):
        self.add_log(self.log_pathdirs, text)

    def get_comment(self, page_num):
        if self.config.getint(self.user_config_section, 'is_get_comment') == 1:
            try:
                self.log("开始获取评论")
                # 获取评论需要的基本配置
                comment_cookie = self.config.get(self.user_config_section, 'comment_cookie')
                comment_host = self.config.get(self.user_config_section, 'comment_host')
                comment_referer = self.config.get(self.user_config_section, 'comment_referer')
                commnet_url_base = self.config.get(self.user_config_section, 'commnet_url_base')
                # url params
                param_str = "?"
                params = self.config.items(self.user_config_section)
                for param in params:  # 普通参数拼接
                    key = param[0]
                    values = param[1]
                    if key.find('comment_param_') >= 0:
                        if key.find('startdate') >= 0:
                            key = key.replace('startdate', 'startDate')
                        if key.find('enddate') >= 0:
                            key = key.replace('enddate', 'endDate')
                        if key.find('commentkeyword') >= 0:
                            key = key.replace('commentkeyword', 'commentKeyword')
                        if key.find('pagenum') >= 0:
                            key = key.replace('pagenum', 'pageNum')
                            values = str(page_num)
                        param_str += key.replace('comment_param_', '') + '=' + values + '&'

                commnet_url = commnet_url_base + param_str
                print(commnet_url)
                # # 请求数据
                session = requests.Session()
                user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3719.400 QQBrowser/10.5.3715.400'
                # 请求评论数据
                comment_headers = {
                    'User-Agent': user_agent,
                    'Cookie': comment_cookie,
                    'Host': comment_host,
                    'Referer': comment_referer,
                }
                comment_response = session.get(commnet_url, headers=comment_headers)
                comment_json_total = json.loads(comment_response.text)
                # 下载数据保存到数据库
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()

                comments = comment_json_total['data']['comments']
                for i in range(len(comments)):
                    comment_id = str(comments[i]['id'])
                    wm_poi_id = str(comments[i]['wm_poi_id'])
                    username = str(comments[i]['username'])
                    comment = str(comments[i]['comment'])
                    ctime = str(comments[i]['ctime'])
                    utime = str(comments[i]['utime'])
                    ship_time = str(comments[i]['ship_time'])
                    order_comment_score = str(comments[i]['order_comment_score'])
                    food_comment_score = str(comments[i]['food_comment_score'])
                    delivery_comment_score = str(comments[i]['delivery_comment_score'])
                    remark = str(comments[i]['orderStatus']['remark'])
                    scoreMeaning = str(comments[i]['scoreMeaning'])
                    praise_food_list = str(comments[i]['praise_food_list']).replace("'", "")

                    sql = "insert into t_comments(comment_id,shop_id,username,comment,ctime,utime,ship_time" \
                          ",order_comment_score,food_comment_score,delivery_comment_score,remark,scoreMeaning,praise_food_list) " \
                          "values('" + comment_id + "','" + wm_poi_id + "','" + username + "','" + comment + "','" + ctime + "','" + utime + "','" + ship_time + "','" \
                          + order_comment_score + "','" + food_comment_score + "','" + delivery_comment_score + "','" + remark + "','" + scoreMeaning + "','" + praise_food_list + "')"
                    c.execute(sql)
                conn.commit()
                conn.close()
                self.log("获取评论完毕")
                time.sleep(self.request_interval)
            except Exception as e:
                self.log("Err:"+str(e))

    def get_comm_nums(self):
        if self.config.getint(self.user_config_section, 'is_get_comment') == 1:
            try:
                self.log("开始获取评论总数")
                # 获取评论需要的基本配置
                comment_cookie = self.config.get(self.user_config_section, 'comment_cookie')
                comment_host = self.config.get(self.user_config_section, 'comment_host')
                comment_referer = self.config.get(self.user_config_section, 'comment_referer')
                commnet_url_base = self.config.get(self.user_config_section, 'commnet_url_base')
                # url params
                param_str = "?"
                params = self.config.items(self.user_config_section)
                for param in params:  # 普通参数拼接
                    key = param[0]
                    values = param[1]
                    if key.find('comment_param_') >= 0:
                        if key.find('startdate') >= 0:
                            key = key.replace('startdate', 'startDate')
                        if key.find('enddate') >= 0:
                            key = key.replace('enddate', 'endDate')
                        if key.find('commentkeyword') >= 0:
                            key = key.replace('commentkeyword', 'commentKeyword')
                        if key.find('pagenum') >= 0:
                            key = key.replace('pagenum', 'pageNum')
                            values = "1"
                        param_str += key.replace('comment_param_', '') + '=' + values + '&'

                commnet_url = commnet_url_base + param_str
                print(commnet_url)
                # # 请求数据
                session = requests.Session()
                user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3719.400 QQBrowser/10.5.3715.400'
                # 请求评论数据
                comment_headers = {
                    'User-Agent': user_agent,
                    'Cookie': comment_cookie,
                    'Host': comment_host,
                    'Referer': comment_referer,
                }
                comment_response = session.get(commnet_url, headers=comment_headers)
                comment_json_total = json.loads(comment_response.text)
                nums = comment_json_total['data']['total']
                self.log("评论总数："+str(nums))
                time.sleep(self.request_interval)
                return nums
            except Exception as e:
                self.log("Err:" + str(e))
                return -1
        return -1

    def get_order_nums(self):
        if self.config.getint(self.user_config_section, 'is_get_order') == 1:
            try:
                self.log("开始获取订单总数")
                # 获取订单需要的基本配置
                order_cookie = self.config.get(self.user_config_section, 'order_cookie')
                order_host = self.config.get(self.user_config_section, 'order_host')
                order_referer = self.config.get(self.user_config_section, 'order_referer')
                order_url_base = self.config.get(self.user_config_section, 'order_url_base')
                order_param_startdate = self.config.get(self.user_config_section, 'order_param_startdate')
                # url params
                param_str = "?"
                params = self.config.items(self.user_config_section)
                for param in params:  # 普通参数拼接
                    key = param[0]
                    values = param[1]
                    if key.find('order_param_') >= 0:
                        if key.find('getnewvo') >= 0:
                            key = key.replace('getnewvo', 'getNewVo')
                        if key.find('wmorderpaytype') >= 0:
                            key = key.replace('wmorderpaytype', 'wmOrderPayType')
                        if key.find('wmorderstatus') >= 0:
                            key = key.replace('wmorderstatus', 'wmOrderStatus')
                        if key.find('sortfield') >= 0:
                            key = key.replace('sortfield', 'sortField')
                        if key.find('startdate') >= 0:
                            key = key.replace('startdate', 'startDate')
                        if key.find('enddate') >= 0:
                            key = key.replace('enddate', 'endDate')
                        if key.find('requestwmpoiid') >= 0:
                            key = key.replace('requestwmpoiid', 'requestWmPoiId')
                        if key.find('signtoken') >= 0:
                            key = key.replace('signtoken', 'signToken')
                        param_str += key.replace('order_param_', '') + '=' + values + '&'

                order_url = order_url_base + param_str
                print(order_url)
                # 请求订单数据
                session = requests.Session()
                user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3719.400 QQBrowser/10.5.3715.400'
                order_headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Cookie': order_cookie,
                    'Host': order_host,
                    'Referer': order_referer,
                    'User-Agent': user_agent,
                    'X-Requested-With': 'XMLHttpRequest'
                }
                order_response = session.get(order_url, headers=order_headers)
                order_totals = json.loads(order_response.text)
                nums = order_totals['wmOrderList'][0]['num']
                self.log("订单总数："+str(nums))
                time.sleep(self.request_interval)
                return {"nums": nums, "startDate": order_param_startdate}
            except Exception as e:
                self.log("Err:" + str(e))
                return {"nums": -1}
        return {"nums": -1}

    def get_order_nextLabel(self, day, day_seq):
        return quote('{"day":' + str(day) + ',"day_seq":' + str(day_seq) + ',"page":0,"setDay_seq":true,"setDay":true,"setPage":false}', 'utf-8')

    def get_order(self, nextLabel):
        if self.config.getint(self.user_config_section, 'is_get_order') == 1:
            try:
                self.log("开始获取订单列表")
                # 获取订单需要的基本配置
                order_cookie = self.config.get(self.user_config_section, 'order_cookie')
                order_host = self.config.get(self.user_config_section, 'order_host')
                order_referer = self.config.get(self.user_config_section, 'order_referer')
                order_url_base = self.config.get(self.user_config_section, 'order_url_base')

                # url params
                param_str = "?"
                params = self.config.items(self.user_config_section)
                for param in params:  # 普通参数拼接
                    key = param[0]
                    values = param[1]
                    if key.find('order_param_') >= 0:
                        if key.find('getnewvo') >= 0:
                            key = key.replace('getnewvo', 'getNewVo')
                        if key.find('wmorderpaytype') >= 0:
                            key = key.replace('wmorderpaytype', 'wmOrderPayType')
                        if key.find('wmorderstatus') >= 0:
                            key = key.replace('wmorderstatus', 'wmOrderStatus')
                        if key.find('sortfield') >= 0:
                            key = key.replace('sortfield', 'sortField')
                        if key.find('startdate') >= 0:
                            key = key.replace('startdate', 'startDate')
                        if key.find('enddate') >= 0:
                            key = key.replace('enddate', 'endDate')
                        if key.find('requestwmpoiid') >= 0:
                            key = key.replace('requestwmpoiid', 'requestWmPoiId')
                        if key.find('signtoken') >= 0:
                            key = key.replace('signtoken', 'signToken')
                        param_str += key.replace('order_param_', '') + '=' + values + '&'
                param_str += "nextLabel="+nextLabel+"&"
                order_url = order_url_base + param_str
                print(order_url)
                # 请求订单数据
                session = requests.Session()
                user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3719.400 QQBrowser/10.5.3715.400'
                order_headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Cookie': order_cookie,
                    'Host': order_host,
                    'Referer': order_referer,
                    'User-Agent': user_agent,
                    'X-Requested-With': 'XMLHttpRequest'
                }
                order_response = session.get(order_url, headers=order_headers)
                order_totals = json.loads(order_response.text)
                # # 下载数据保存到数据库
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                orders = order_totals['wmOrderList']
                for i in range(len(orders)):
                    order_id = str(orders[i]['wm_order_id_view_str'])
                    user_id = str(orders[i]['user_id'])
                    num = str(orders[i]['num'])
                    order_time = str(orders[i]['order_time'])
                    confirm_time = str(orders[i]['confirm_time'])
                    utime = str(orders[i]['utime'])
                    privacy_phone = str(orders[i]['privacy_phone'])
                    backup_privacy_phones = str(orders[i]['backup_privacy_phones']).replace("'", "")
                    remark = str(orders[i]['remark'])
                    orderCopyContent = str(orders[i]['orderCopyContent']).replace("'", "").replace('"', '')
                    recipient_phone = str(orders[i]['recipient_phone'])
                    recipient_bindedPhone = str(orders[i]['recipient_bindedPhone'])
                    recipient_name = str(orders[i]['recipient_name'])

                    sql = "insert into t_orders(order_id,user_id,num,order_time,confirm_time,utime,privacy_phone,backup_privacy_phones,remark,orderCopyContent,recipient_phone,recipient_bindedPhone,recipient_name) " \
                          "values('"+order_id+"','"+user_id+"','"+num+"','"+order_time+"','"+confirm_time+"','"+utime+"','"+privacy_phone+"','"\
                          +backup_privacy_phones+"','"+remark+"','"+orderCopyContent+"','"+recipient_phone+"','"+recipient_bindedPhone+"','"+recipient_name+"')"
                    c.execute(sql)

                conn.commit()
                conn.close()
                self.log("获取订单列表完成")
                time.sleep(self.request_interval)
            except Exception as e:
                self.log("Err:"+str(e))


if __name__ == '__main__':
    mt = MeiT('chenx')
    mt.init_db()
    # 获取所有评论
    comm_nums = mt.get_comm_nums()
    if comm_nums > 0:
        for i in range(1, (comm_nums // 10) + 2):
            mt.get_comment(i)
    # 获取所有订单
    order_nums_dict = mt.get_order_nums()
    order_nums = order_nums_dict['nums']
    order_startDate = str(order_nums_dict['startDate'])
    if order_nums > 0:
        day = order_startDate.replace("-", "")
        day_seq = order_nums + 1
        while day_seq > 0:
            nextLabel = mt.get_order_nextLabel(day, day_seq)
            print(day_seq)
            mt.get_order(nextLabel)
            day_seq -= 10
    # # 打印匹配信息
    # conn = sqlite3.connect(mt.db_name)
    # c = conn.cursor()
    # sql =
    # c.execute(sql)
    # conn.commit()
    # conn.close()






































