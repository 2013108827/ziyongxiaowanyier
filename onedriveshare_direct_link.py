import time,json,os


'''
提取onedrive分享文件下载直链脚本，具体能干啥，我也不清楚。
该脚本需要先安装beautifulsoup4，requests库
'''
modelist = ['requests', 'beautifulsoup4']

def dir_link():
    share_link = input("请输入分享链接：")

    if len(share_link) > 8:

        try:
            response = requests.get(str(share_link))
        except:
            print("分享链接填错了!!!")
        finally:
            st_code = response.status_code
        if int(st_code) == 200:
            html_str = response.text
            print("分享链接正确，开始获取真实分享链接")
            soup = BeautifulSoup(html_str, 'lxml')  # html.parser是解析器，也可是lxml
            # print(soup.prettify())

            tag1 = str(soup.find(property="og:url"))
            #print(tag1)
            # print(tag1.find('resid'))
            # print(tag1.find('&amp'))
            id = tag1[tag1.find('resid') + 6:tag1.find('&amp')]
            # print(id)
            cid = id[:id.find('!')]
            # print(cid)
            atkey = tag1[tag1.find('authkey') + 8:tag1.find('&amp', tag1.find('authkey'), len(tag1))]
            # print(atkey)
            print("已获取到真实分享链接，继续获取直链下载链接")
            time.sleep(2)

            url = ('https://api.onedrive.com/v1.0/drives/' + str(cid) + '/items/' + str(id))
            params = {
                'select': 'id,@content.downloadUrl',
                'authkey': str(atkey)
            }
            response2 = requests.get(url, params=params)
            response2_json = json.loads(response2.text)
            #print(response2.text)  # 返回结果里的@content.downloadUrl就是文件的下载地址
            try:
                download_url = response2_json['@content.downloadUrl']
            except:
                print("获取失败，请重试")
            finally:
                print("下载直链为："+ str(download_url))
                print("程序将在30秒后结束运行")
                time.sleep(30)
        else:
            print("分享链接不对，好好检查一下!!!")

    else:
        print("分享链接不对!!!")


if __name__ == "__main__":

    print("该脚本需要用到beautifulsoup4，requests库。开始自检")
    for i in list(modelist):
        chec = os.system('pip list | findstr ' + str(i))
        if int(chec) == 0:
            print(str(i) + "已安装")
        elif int(chec) == 1:
            print(str(i) + "模块未安装，开始自动安装")
            os.system('pip install ' + str(i))
    import requests
    from bs4 import BeautifulSoup
    print("完成自检\n")
    dir_link()
