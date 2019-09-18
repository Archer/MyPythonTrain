import requests

cookie = r"_lxsdk_cuid=16d2d7d926ec8-062020c93377d8-34594872-1fa400-16d2d7d926fc8; _lxsdk=16d2d7d926ec8-062020c93377d8-34594872-1fa400-16d2d7d926fc8; uuid=26189c907879d229d700.1568426269.1.0.0; token=0jW44cS1IZ8Cwdij6_TVhG2cGa-o7lW1UaABvUyMqEzE*; acctId=41421701; wmPoiId=5168729; _source=PC; bsid=A-nFV4Gtsjvk05l2jcoHQCYIYoQsoz8DxVOTAWuQLd5uu2MX4Y9tYXNhiLvrIXrZ7Alu2SHGf4h7spZjtvXxCQ; JSESSIONID=1hulx1dfkucwkgato6q8fkvrb; _lxsdk_s=16d2db0ff5c-399-723-d7b%7C%7C43"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
    'Cookie': cookie,
    'Host': r'waimaieapp.meituan.com',
    'Referer': r'https://waimaieapp.meituan.com/other/v2/customer/comment?_source=PC&token=0jW44cS1IZ8Cwdij6_TVhG2cGa-o7lW1UaABvUyMqEzE*&acctId=41421701&wmPoiId=5168729&region_id=1000420900&bsid=A-nFV4Gtsjvk05l2jcoHQCYIYoQsoz8DxVOTAWuQLd5uu2MX4Y9tYXNhiLvrIXrZ7Alu2SHGf4h7spZjtvXxCQ&appType=3&fromPoiChange=false',
}
url = r"https://waimaieapp.meituan.com/other/v2/customer/comment/r/list?wmPoiId=5168729&acctId=41421701&token=0jW44cS1IZ8Cwdij6_TVhG2cGa-o7lW1UaABvUyMqEzE*&rate=-1&reply=-1&context=1&startDate=2019-09-01&endDate=2019-09-13&commentKeyWord=&pageNum=1"
session = requests.Session()
response = session.get(url, headers=headers)
print(response.status_code)
print(response.text)
