from bs4 import BeautifulSoup
from PIL import Image
import requests
import os
import time


def getpicture():
    BVcode = input("请输入B站视频BV号或视频网址:")
    print('开始获取')
    if len(str(BVcode)) > 20:
        if BVcode.find("?") == -1:
            bvcode = BVcode[BVcode.find("BV"):]
        else:
            bvcode = BVcode[BVcode.find("BV"):BVcode.find("?")]
            if bvcode.find("/") != -1:
                bvcode = bvcode[:bvcode.find("/")]
        print("成功获取到BV号")
        print('BV号是：' + bvcode)
    else:
        bvcode = BVcode
        print("成功获取到BV号")
        print('BV号是：' + bvcode)

    url = url = "https://www.bilibili.com/video/" + str(bvcode)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    response = requests.get(url, headers=headers, timeout=10)
    html_str = response.text

    soup = BeautifulSoup(html_str, 'lxml')

    imagelist = soup.head.contents
    for i in enumerate(imagelist):
        if str(i).find('itemprop="thumbnailUrl"') != -1:
            if i[1]['content'] != "":
                # print(i[1]['content'])
                pictureurl = requests.get(i[1]['content'])

                with open(str(bvcode) + '.jpg', 'wb') as f:
                    f.write(pictureurl.content)
                    print('保存图片成功')
                    print("windows系统可以继续下一步打开图片，其他系统的不确定,图片默认保存在脚本同文件夹下，BV号是文件名")
                    pictureopen = input("打开图片请输0，不打开请输1：")
                    if int(pictureopen) == 0:
                        print('三秒后自动打开图片')
                        print(3)
                        time.sleep(1)
                        print(2)
                        time.sleep(1)
                        print(1)
                        time.sleep(1)
                        im = Image.open(str(bvcode) + '.jpg')
                        im.show()
                    elif int(pictureopen) == 1:
                        print("你选择了不打开图片，程序自动结束")
                        exit()
            else:
                print("这个视频没有封面或者获取失败")
        elif str(i).find('itemprop="thumbnailUrl"') == -1:
            1 == 1
        else:
            print("BV号输入有误，自动退出程序")
            exit()


print('该程序需要先安装beautifulsoup4，Pillow,requests库，你安装好了吗？')
mode = input("装好了请输入0，没有请输入1，然后回车：")
if int(mode) == 1:
    modelist = ['beautifulsoup4', 'Pillow', 'requests']
    for mo in modelist:
        command = 'pip install '+ str(mo)            #直接运行命令
        os.system(command)
    time.sleep(2)
    getpicture()

elif int(mode) == 0:

    getpicture()

else:
    print("别他喵的瞎JB输，看好提示再输")

