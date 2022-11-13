import requests
import os
import re
from bs4 import BeautifulSoup
from contextlib import closing
from tqdm import tqdm
import time
import tkinter
from tkinter import *
from tkinter.ttk import *

# 创建窗口
top = tkinter.Tk()
# 设定窗口名
top.title("动漫之家爬虫启动器")
# 设定窗口大小
top.geometry('500x300')
# 设置主窗口的背景颜色,颜色值可以是英文单词，或者颜色值的16进制数,除此之外还可以使用Tk内置的颜色常量
top["background"] = "#C9C9C9"

def WiseSpider(url, name):
    # 创建保存目录
    # save_dir = '妖神记'
    save_dir = name
    if save_dir not in os.listdir('./'):
        os.mkdir(save_dir)
    initial_time = 0
    # target_url = "https://www.dmzj.com/info/yaoshenji.html"
    target_url = url
    # 获取动漫章节链接和章节名
    r = requests.get(url=target_url, verify=False)
    bs = BeautifulSoup(r.text, 'lxml')
    list_con_li = bs.find('ul', class_="list_con_li")
    cartoon_list = list_con_li.find_all('a')
    chapter_names = []
    chapter_urls = []
    for cartoon in cartoon_list:
        href = cartoon.get('href')
        name = cartoon.text
        chapter_names.insert(0, name)
        chapter_urls.insert(0, href)
    # 下载漫画
    for i, url in enumerate(tqdm(chapter_urls)):

        download_header = {
            'Referer': url
        }
        name = chapter_names[i]
        # 去掉.
        while '.' in name:
            name = name.replace('.', '')
        chapter_save_dir = os.path.join(save_dir, name)
        if name not in os.listdir(save_dir):
            os.mkdir(chapter_save_dir)
        r = requests.get(url=url)
        html = BeautifulSoup(r.text, 'lxml')
        script_info = html.script
        pics = re.findall('\d{13,14}', str(script_info))
        for j, pic in enumerate(pics):
            if len(pic) == 13:
                pics[j] = pic + '0'
        pics = sorted(pics, key=lambda x: int(x))
        # str(script_info)中存储了一大堆script信息，从中可以获取两段数字的长度（信息比较混杂）
        # 使得下面两个语句对于大妈之家的所有漫画url都适用
        # print(str(script_info))

        len1 = len2 = 0
        temp = 0
        for i in str(script_info):
            if (i >= '0') and (i <= '9'):
                temp = temp + 1
            elif ((temp >= 3) and temp <= 12) and len1 == 0:
                len1 = temp
                temp = 0
            elif ((temp >= 3) and temp <= 12) and len2 == 0:
                len2 = temp
                temp = 0
            else:
                # print(temp)
                temp = 0
        # print(len1)
        # print(len2)
        # 先len2 再len1
        str1 = '\|(\d{' + str(max(len1,len2)) + '})\|'
        str2 = '\|(\d{' + str(min(len2,len1)) + '})\|'
        #    chapterpic_hou = re.findall(str2, str(script_info))[0] # 获取图片url中的中间段数字
        #    chapterpic_qian = re.findall(str1, str(script_info))[0] # 获取图片url中的最前段数字
        pattern1 = re.compile(str1)
        pattern2 = re.compile(str2)
        chapterpic_hou = re.findall(pattern1, str(script_info))[0]  # 获取图片url中的中间段数字
        chapterpic_qian = re.findall(pattern2, str(script_info))[0]  # 获取图片url中的最前段数字
        #     list1 = re.findall('^\d{3,7}\|$', str(script_info))
        #     chapterpic_hou = list1[0]  # 获取图片url中的中间段数字
        #     chapterpic_qian = list1[1]  # 获取图片url中的最前段数字
        for idx, pic in enumerate(pics):
            if pic[-1] == '0':
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic[:-1] + '.jpg'
            else:
                url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic + '.jpg'
            pic_name = '%03d.jpg' % (idx + 1)
            pic_save_path = os.path.join(chapter_save_dir, pic_name)
            with closing(requests.get(url, headers=download_header, stream=True)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    with open(pic_save_path, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                # https://images.dmzj.com/img/chapterpic/39233/147387/16667538360726.jpg
                else:
                    print('链接异常')
        time.sleep(10)
        initial_time = 1
    EndText = tkinter.Label(text="爬虫进程运行完毕", bg=background, fg="black", font=('微软雅黑', 14))
    # 提示用户进程已经结束
    EndText.place(x=170, y=200)


background = top.cget('bg')
# 添加文本内,设置字体的前景色和背景色，和字体类型、大小
titletext = tkinter.Label(text="动漫之家(dmzj.com)爬虫启动器", bg=background, fg="black", font=('微软雅黑', 20, 'bold italic'))
# 将文本内容放置在主窗口内
titletext.place(x=40, y=20)
# 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
buttonQuit = tkinter.Button(top, text="关闭", command=top.quit)
# 将按钮放置在主窗口内
buttonQuit.place(x=280, y=250, width=60, height=30)

targetinfo = tkinter.Label(text="目标网址：https://www.dmzj.com/info/xiexiuyutianshadizi.html", bg=background, fg="black", font=('微软雅黑', 10))
targetinfo.place(x=40,y=130)
url = "https://www.dmzj.com/info/xiexiuyutianshadizi.html"
name = "邪修与天煞弟子"

# urlBox_var = tkinter.StringVar()
# urlBox_var.set("此处输入url")
# urlBox = tkinter.Entry(x=200,y=200,width=50,textvariable=urlBox_var).place()

buttonRun = tkinter.Button(top, text="启动爬虫", command=lambda: WiseSpider(url, name))
buttonRun.place(x=150, y=250, width=60, height=30)

top.mainloop()
