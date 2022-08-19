import eventlet
import requests
from duo import distance
from temperature import read_dht11_dat

urls = ["https://sctapi.ftqq.com/SCT165116TqneFO2PJ7lMcDgDsXQHXTixD.send?title=messagetitle",
        "https://sctapi.ftqq.com/SCT165257ThlcIj28JPnCD0WCQUdxS9kIb.send?title=messagetitle"]


def wechat_send(text):
    url_i = "http://open.iciba.com/dsapi/"
    r = requests.get(url_i)
    content = r.json()['content']
    note = r.json()['note']

    result = read_dht11_dat()
    eventlet.monkey_patch()

    with eventlet.Timeout(10, False):
        while not result:
            result = read_dht11_dat()

    if result:
        temperature, humidity = result
        myParams = {"title": "提醒事项",
                    "desp": text + "今天的气温是%s摄氏度, 今天的湿度是: %s %% 垃圾桶内垃圾与垃圾盖的距离为： %s "
                                   "祝你度过美好一天！ 今日必应美图： "
                                   "如果垃圾桶内垃圾高度过高，可以在公众号中回复换袋来进行垃圾袋的更换。"
                                   "![Bing](https://www.todaybing.com/api/today/cn)"
                                   "每日格言：%s " % (humidity, temperature, content, distance())}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
        for url in urls:
            res = requests.get(url=url, params=myParams)
    else:
        myParams = {"title": "提醒事项",
                    "desp": text + "今天的气温以及湿度无法获取，可能是传感器故障。垃圾桶内垃圾与垃圾盖的距离为： %s  "
                                   "祝你度过美好一天！ 今日必应美图： "
                                   "如果垃圾桶内垃圾高度过高，可以在公众号中回复换袋来进行垃圾袋的更换。"
                                   "![Bing](https://www.todaybing.com/api/today/cn)"
                                   "每日格言：%s" % (content, distance())}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url

        for url in urls:
            res = requests.get(url=url, params=myParams)
