'''
网址：https://movie.douban.com/top250
获取的数据类型：电影名称、年份、电影评分、评论人数、国家
'''
import time
import random
import pandas as pd
import requests
from lxml import etree


# 数据解析，根据url获取网页上面的数据
def response_to_data(url):
    # 对网页发送请求，获取到网页的代码（数据）
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    # 从网页数据中提取电影名称数据
    movie_name = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
    # 从网页数据中提取电影评分
    moive_pf = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')
    # 提取评论人数
    moive_people = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[4]/text()')
    # 提取上映时间和国家(需分开数据)
    moive_datas = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]')
    # print('电影名称:',len(movie_name),movie_name)
    # print('电影评分:',len(moive_pf),moive_pf)
    # print('评论人数:',len(moive_people),moive_people)
    # print('上映时间和国家:',len(moive_datas),moive_datas)
    # 1.使用正则提取年份和国家
    # re.findall('\xa0(.*?)', i)
    # print(i.split(' '))
    # 2.使用split进行分割
    for i in range(len(moive_datas)):
        # 直接分割提取数据会得到一些空格和换行，这些都是需要进行处理的
        # 对数据进行分割，下标为0的数据是电影年份
        year = moive_datas[i].split('/')[0].replace(' ', '').replace('\n', '').replace('\xa0', '').replace('(中国大陆)', '')
        # 小标为1的数据是国家
        # country = i.split('/')[1].replace(' ','').replace('\n','')
        # print(f'电影年份：{year},国家：{country}')

        # 获取国家数据，由于有些电影存在多个国家，这里我们只取第一个
        countrys = moive_datas[i].split('/')[1]
        if ' ' in countrys:
            country = countrys.split(' ')[0].replace('\xa0', '').replace(' ', '')
        else:
            country = countrys.replace(' ', '')  # ' '这里不是空格，是特殊字符，从结果中copy过来
        if '中国' in countrys:
            country = '中国'
        # 将数据添加到列表中
        moive_name_list.append(movie_name[i])
        # 将字符串类型的电影评分转为浮点型
        moive_pf_list.append(float(moive_pf[i]))
        # 清除‘人评分’字符，再转数据类型 1.使用切片的方式[:-3]   2.replace()替换
        moive_people_list.append(int(moive_people[i].replace('人评价', '')))
        year_list.append(int(year))
        country_list.append(country)


# ctrl+alt+l 快速格式化代码
# 保存数据，将爬虫获取到的数据保存到本地
def save_to(file_name):
    # 创建空的DataFrame
    df = pd.DataFrame()
    df['电影名称'] = moive_name_list
    df['电影评分'] = moive_pf_list
    df['评论人数'] = moive_people_list
    df['电影年份'] = year_list
    df['国家'] = country_list
    # 自定义保存数据
    df.to_csv(file_name, encoding='utf_8_sig',
              # 保存时不保存df行索引
              index=False)


if __name__ == '__main__':
    num = int(input('请输入需要爬取的页数：'))
    # 伪请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    # 定义列表存储数据
    moive_name_list = []
    moive_pf_list = []
    moive_people_list = []
    country_list = []
    year_list = []
    for i in range(num):
        print((f'开始爬取第{i + 1}页'))
        url = f'https://movie.douban.com/top250?start={25 * i}&filter='
        response_to_data(url)
        print((f'第{i + 1}页爬取完成'))
        time.sleep(random.randint(1, 3))
        # 爬取完一个页面之后随机延迟1-3秒，防止爬取过快导致被反爬
    path = '豆瓣.csv'
    save_to(path)

    # response = requests.get(url,headers=headers)
    # print(response.text)
    # print((len(moive_name_list),moive_name_list))
    # print((len(moive_pf_list),moive_pf_list))
    # print((len(moive_people_list),moive_people_list))
    # print((len(country_list),country_list))
    # print((len(year_list),year_list))

# https://movie.douban.com/top250?start=25&filter=  2
# https://movie.douban.com/top250?start=50&filter=  3
# https://movie.douban.com/top250?start=75&filter=  4
# 0*25, 1*25, 2*25，3*25
