## crontab 任务执行该脚本下载数据


import requests
import datetime
site_list = ['C10']
base_url = 'http://127.0.0.1:80/site_info/download/'

if __name__ == '__main__':
    for site in site_list:
        url = base_url+site
        r = requests.get(url)
        if r.text == u'文件已下载':
            print(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")+"--"+site+" 数据更新成功")
