--
select t1.order_id,t1.num,t1.ship_time,t1.privacy_phone,backup_privacy_phones,t1.remark,t1.order_time_str,recipient_phone,recipient_bindedPhone,recipient_name
,t2.comm_time_str,t2.comment_id,t2.username,t2.comment,t2.remark,t2.praise_food_list
from (
select order_id,num,order_time,utime,(utime-order_time)/60 ship_time,privacy_phone,backup_privacy_phones,remark,orderCopyContent
,recipient_phone,recipient_bindedPhone,recipient_name
,datetime(order_time, 'unixepoch', 'localtime') order_time_str
,datetime(utime, 'unixepoch', 'localtime') utime_str
,date(order_time, 'unixepoch', 'localtime') order_date_str
from t_orders  where id in (select MAX(id) from t_orders group by order_id)
)t1
join (
select shop_id,comment_id,username,comment,utime,ship_time,remark,praise_food_list
,datetime(utime, 'unixepoch', 'localtime') comm_time_str
,date(utime, 'unixepoch', 'localtime') comm_date_str
from t_comments where id in (select max(id) from t_comments group by comment_id)
)t2
on t1.ship_time=t2.ship_time and t1.order_time_str<comm_time_str

--
--订单表
select order_id '订单编号',num '订单号',(utime-order_time)/60 '配送时间',privacy_phone,backup_privacy_phones,remark,orderCopyContent
,recipient_phone,recipient_bindedPhone,recipient_name '顾客名称'
,datetime(order_time, 'unixepoch', 'localtime') '下单时间'
,datetime(utime, 'unixepoch', 'localtime')  '收货时间'
,date(order_time, 'unixepoch', 'localtime')  '下单日期'
from t_orders  where id in (select MAX(id) from t_orders group by order_id)