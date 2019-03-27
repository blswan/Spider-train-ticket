import requests
from urllib.parse import urlencode
from lxml import etree


def my_format(str, width, align):
    sigle = 0
    double = 0
    sep = ' '
    for i in str:
        if len(i.encode('gb2312')) == 1:
            sigle += 1
        elif len(i.encode('gb2312')) == 2:
            double += 1
    if align == 'l':
        return str + (width * 2 - sigle - double * 2) * sep
    elif align == 'r':
        return (width * 2 - sigle - double * 2) * sep + str
    elif align == 'c':
        return int((width * 2 - sigle - double * 2) // 2) * sep + str + int(
            (width * 2 - sigle - double * 2) - (width * 2 - sigle - double * 2) // 2) * sep


print("请按格式输入信息 出发地-到达地-年/月/日")
search_code = input("查询框：")

search_list = search_code.split('-')
date_list = search_list[2].split('/')
start = search_list[0]
end = search_list[1]
date = "{0}-{1:02d}-{2:02d}".format(
    date_list[0],
    int(date_list[1]),
    int(date_list[2]))


base_url = 'https://vip.huoche.net/train/search?'
params = {
    'k1': start,
    'k2': end,
    'goDate': date
}
search_url = base_url + urlencode(params)
headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac Os X 10_11_4) AppleWebKit/537.36 (KHML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
response = requests.get(url=search_url, headers=headers).text
html = etree.HTML(response)
selectors = html.xpath('//*[@class="train-list"]//li[@class="train-data"]')
print("*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*")
print(
    '|', my_format("车次", 4, 'c'),
    '|', my_format("车站", 4, 'c'),
    '|', my_format("时间", 4, 'c'),
    '|', my_format("耗时", 4, 'c'),
    '|', my_format("商务座", 4, 'c'),
    '|', my_format("一等座", 4, 'c'),
    '|', my_format("二等座", 4, 'c'),
    '|', my_format("高级软卧", 4, 'c'),
    '|', my_format("软卧", 4, 'c'),
    '|', my_format("硬卧", 4, 'c'),
    '|', my_format("硬座", 4, 'c'),
    '|', my_format("无座", 4, 'c'),
    '|'
)
print("*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*")
for selector in selectors:
    train_number = selector.xpath(
        './/div[@class="w1"]//strong/text()')[0].strip()
    departure_time = selector.xpath(
        './/div[@class="w2"]//strong/text()')[0].strip()
    departure_station = selector.xpath(
        './/div[@class="w2"]//span/text()')[0].strip()
    time_spend = selector.xpath(
        './/div[@class="w4"]//div[@class="haoshi"]/text()')[0].strip()
    arrival_time = selector.xpath(
        './/div[@class="w3"]//strong/text()')[0].strip()
    arrival_station = selector.xpath(
        './/div[@class="w3"]//span/text()')[0].strip()
    level = {seat.xpath('./span/text()')[0].strip(): (price.xpath('./b/text()')[0].strip(), remain.xpath('./strong/text()')[0].strip())
             for seat in selector.xpath('.//div[@class="w5"]//div')
             for price in selector.xpath('.//div[@class="w5"]//div')
             for remain in selector.xpath('.//div[@class="w5"]//div')}
    seats = ['商务座', '一等座', '二等座', '高级软卧', '软卧', '硬卧', '硬座', '无座']
    for key in seats:
        level.setdefault(key, ('--', '--'))
    print(
        '|', my_format(train_number, 4, 'c'),
        '|', f"\033[32;0m{my_format(departure_station,4,'c')}\033[0m",
        '|', f"\033[32;0m{my_format(departure_time,4,'c')}\033[0m",
        '|', my_format(time_spend, 4, 'c'),
        '|', my_format(level.get('商务座')[1], 4, 'c'),
        '|', my_format(level.get('一等座')[1], 4, 'c'),
        '|', my_format(level.get('二等座')[1], 4, 'c'),
        '|', my_format(level.get('高级软卧')[1], 4, 'c'),
        '|', my_format(level.get('软卧')[1], 4, 'c'),
        '|', my_format(level.get('硬卧')[1], 4, 'c'),
        '|', my_format(level.get('硬座')[1], 4, 'c'),
        '|', my_format(level.get('无座')[1], 4, 'c'),
        '|'
    )
    print(
        '|', my_format('', 4, 'c'),
        '|', f"\033[31;0m{my_format(arrival_station, 4, 'c')}\033[0m",
        '|', f"\033[31;0m{my_format(arrival_time, 4, 'c')}\033[0m",
        '|', my_format('', 4, 'c'),
        '|', my_format(level.get('商务座')[0], 4, 'c'),
        '|', my_format(level.get('一等座')[0], 4, 'c'),
        '|', my_format(level.get('二等座')[0], 4, 'c'),
        '|', my_format(level.get('高级软卧')[0], 4, 'c'),
        '|', my_format(level.get('软卧')[0], 4, 'c'),
        '|', my_format(level.get('硬卧')[0], 4, 'c'),
        '|', my_format(level.get('硬座')[0], 4, 'c'),
        '|', my_format(level.get('无座')[0], 4, 'c'),
        '|'
    )
print("*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*")
