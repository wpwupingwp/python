#!/usr/bin/python3
import pyecharts
import requests
from datetime import datetime
from pyecharts import options
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

province = '湖南省'
url = 'https://lab.isaaclin.cn/nCoV/api/area?latest=0&province='
url = url + province
a = requests.get(url)
results = a.json()
b = results['results']
shijian = datetime.fromtimestamp(int(b[0]['updateTime'])/1000)
confirm ={i['cityName']: i['confirmedCount'] for i in b[0]['cities']}
suspect = {i['cityName']: i['suspectedCount'] for i in b[0]['cities']}
cure = {i['cityName']: i['curedCount'] for i in b[0]['cities']}
dead = {i['cityName']: i['deadCount'] for i in b[0]['cities']}
city = [i['cityName'] for i in b[0]['cities']]
bar = Bar(init_opts=options.InitOpts(width='1000px', height='600px',
                                     page_title='Demo', theme=ThemeType.DARK))
bar.add_xaxis(list(confirm.keys()))
bar.add_yaxis('确诊',[confirm[i] for i in city])
bar.add_yaxis('死亡', [dead[i] for i in city],is_selected=False)
bar.set_global_opts(title_opts=options.TitleOpts(title='湖南省'),
                    datazoom_opts=options.DataZoomOpts(type_='slider'),
                    toolbox_opts=options.ToolboxOpts(),
                    visualmap_opts=options.VisualMapOpts())
bar.set_series_opts(markline_opts=options.MarkLineOpts(
                    data=[options.MarkLineItem(type_="average", name="平均值"),]))
#改成别的路径
bar.render('d:\demo.html')
