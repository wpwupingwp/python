#!/usr/bin/python3
import pyecharts
import requests
import json


from pyecharts import options
from pyecharts.charts import Bar, Pie, Line, Kline
from pyecharts.globals import ThemeType

province = '湖北省'
url = 'https://lab.isaaclin.cn/nCoV/api/area?latest=0&province='
url = url + province
print('开始下载')
a = requests.get(url)
results = a.json()
with open('f:\\a.json', 'w') as out:
    json.dump(results, out, sort_keys=True, indent=4, separators=(',', ':'))
print('下载完了')
b = results['results']
confirm = {i['cityName']: i['confirmedCount'] for i in b[0]['cities']}
suspect = {i['cityName']: i['suspectedCount'] for i in b[0]['cities']}
cure = {i['cityName']: i['curedCount'] for i in b[0]['cities']}
dead = {i['cityName']: i['deadCount'] for i in b[0]['cities']}
city = [i['cityName'] for i in b[0]['cities']]
bar = Bar(init_opts=options.InitOpts(width='1500px', height='600px',
                                     page_title='Demo', theme=ThemeType.DARK))
bar.add_xaxis(city)
bar.add_yaxis('确诊', [confirm[i] for i in city])
bar.add_yaxis('死亡', [dead[i] for i in city], is_selected=False)
bar.add_yaxis('治愈', [cure[i] for i in city], is_selected=False)
zuidazhi = max(confirm.values())
zuidazhi = (1+zuidazhi // 1000) * 1000
bar.set_global_opts(title_opts=options.TitleOpts(title=province+'20200206'),
                    datazoom_opts=options.DataZoomOpts(type_='inside'),
                    toolbox_opts=options.ToolboxOpts(),
                    visualmap_opts=options.VisualMapOpts(max_=zuidazhi,
                                                         split_number=10,
                                                         is_piecewise=True))
bar.set_series_opts(markline_opts=options.MarkLineOpts(
                    data=[options.MarkLineItem(type_="average", name="平均值"),]))
# 改成别的路径
bar.render('f:\demo.html')