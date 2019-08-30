# coding=utf-8
# 第 0002 题: 将 0001 题生成的 200 个激活码（或者优惠券）保存到 sql server 关系型数据库中。
import pymssql

server = "123.58.45.206:9688"
user = "regent"
password = "regent"
database = "test"

def execsql(sql):
    conn = pymssql.connect(server, user, password, database) #获取连接
    #cursor = conn.cursor()
    cursor = conn.cursor(as_dict=True)

    print(sql)
    cursor.execute(sql)
    for row in cursor:
        print("店铺名称:{name},店铺编码：{cusID}".format(name=row['Customer_na'], cusID=row['Customer_id']))

    cursor.close()
    conn.close()

sql = "select top 1 * from customer where customer_id='{}'".format('BZ-00')
execsql(sql)





