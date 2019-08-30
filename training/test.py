from t002 import execsql

sql = "select top 1 * from customer where customer_id='{}'".format('za83')
execsql(sql)
