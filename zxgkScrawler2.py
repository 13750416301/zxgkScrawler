import random
import time
import requests
import urllib
from bs4 import BeautifulSoup 
import re
from PIL import Image
from os import path
import pytesseract
import webbrowser
import json
import jsonpath
from threading import Thread


def fall (img1):#img：图片地址 
    white = (255,255,255,255)
    black = (0,0,0,255)
    #img = Image.open('/home/yang/png/0.png') # 读入图片
    img = Image.open(img1)
    pixdata = img.load()
    X = img.size[0]-1#因为我校的验证码二值化后正好剩下一圈宽度为一像素的白边，所以这么处理了
    Y = img.size[1]-1
 
    def icolor(RGBA):
        if RGBA == white:
            return(1)
        else:
            return(0)
 
    for y in range(Y):
        for x in range(X):
            if (x<1 or y<1):
                pass
            else:
                if icolor(pixdata[x,y]) == 1:
                    pass
                else:
                    if (
                         icolor(pixdata[x+1,y])+
                         icolor(pixdata[x,y+1])+
                         icolor(pixdata[x-1,y])+
                         icolor(pixdata[x,y-1])+
                         icolor(pixdata[x-1,y-1])+
                         icolor(pixdata[x+1,y-1])+
                         icolor(pixdata[x-1,y+1])+
                         icolor(pixdata[x+1,y+1])
                         )>6: 
                         #如果一个黑色像素周围的8个像素中白色像素数量大于5个，则判断其为噪点，填充为白色
                        pixdata[x,y] = white 
    #填充白点       
    for y in range(Y):
        for x in range(X):
            if (x<1 or y<1):
                pass
            else:
                if icolor(pixdata[x,y]) == 0:
                    pass
                else:
                    if (
                         (icolor(pixdata[x+1,y]))+
                         (icolor(pixdata[x,y+1]))+
                         (icolor(pixdata[x-1,y]))+
                         (icolor(pixdata[x,y-1]))
                         )<2:
                         #如果一个白色像素上下左右4个像素中黑色像素的个数大于2个，则判定其为有效像素，填充为黑色。
                        pixdata[x,y] = black
    #二次去除黑点   
    for y in range(Y):
        for x in range(X):
            if (x<1 or y<1):
                pass
            else:
                if icolor(pixdata[x,y]) == 1:
                    pass
                else:
                    if (
                         icolor(pixdata[x+1,y])+
                         icolor(pixdata[x,y+1])+
                         icolor(pixdata[x-1,y])+
                         icolor(pixdata[x,y-1])
                         )>2:
                        pixdata[x,y] = white
    img.save('captcha1.png')


def ganraoxian(img2):#img：图片地址
    #img = Image.open('/home/yang/png/'+str(i)+'.png') # 读入图片
    img = Image.open(img2)
    width = img.size[0]
    heigth = img.size[1]  #获取长宽
    smap={}
    slist=[]
    keylist=[]
    for i in range(0,width):
        for j in range(0,heigth):
            argb = img.getpixel((i,j))
            r = argb[0]
            g = argb[1]
            b = argb[2]
            sum = r + g + b   #得到每一点的rgb
        
            if sum not in smap.keys():  #如果没有该sum值的点  进行添加  并且给值为1
                smap[sum]=1
            else:
                num=smap[sum]       
                smap[sum]=num+1  #如果有了这个值  在原基础上+1
    slist=sorted(smap.items(),key=lambda x:x[1],reverse = False)
 
    if (len(slist) > 4):
        num1 = slist[len(slist) - 5][1]
        num2 = slist[len(slist) - 4][1]
        num3 = slist[len(slist) - 3][1]
        num4 = slist[len(slist) - 2][1]     #获取像素点最多的四个点
 
        for key in smap:
            if smap[key] == num1 or smap[key] == num2 or smap[key] == num3 or smap[key] == num4 :
            
            #if num1 in smap or num2 in smap or num3 in smap or num4 in smap :
                keylist.append(key)      #找到对应颜色的点
 
    for x in range(0,width):
        for y in range(0,heigth):
            argb = img.getpixel((x,y))
            r = argb[0]
            g = argb[1]
            b = argb[2]
            ssum = r + g + b 
            flag = True
            for i in range(1,3): #px+1
                if y + i < heigth and y - i > 0 and x - i > 0 and x + i < width:
 
                    upargb = img.getpixel((x,y-i))
                    endargb = img.getpixel((x,y+i))
                    rightupargb = img.getpixel((x+i,y+i))
                    leftupargb = img.getpixel((x-i,y+i))
                    leftdownargb = img.getpixel((x-i,y-i))
                    rightdownargb = img.getpixel((x+i,y-i))
                    r1 = upargb[0]
                    g1 = upargb[1]
                    b1 = upargb[2]
                    sum1 = r1 + g1 + b1
 
                    r2 = endargb[0]
                    g2 = endargb[1]
                    b2 = endargb[2]
                    sum2 = r2 + g2 + b2
 
                    r3 = rightupargb[0]
                    g3 = rightupargb[1]
                    b3 = rightupargb[2]
                    sum3 = r3 + g3 + b3
 
                    r4 = leftupargb[0]
                    g4 = leftupargb[1]
                    b4 = leftupargb[2]
                    sum4 = r4 + g4 + b4
 
                    r5 = leftdownargb[0]
                    g5 = leftdownargb[1]
                    b5 = leftdownargb[2]
                    sum5 = r5 + g5 + b5
 
                    r6 = rightdownargb[0]
                    g6 = rightdownargb[1]
                    b6 = rightdownargb[2]
                    sum6 = r6 + g6 + b6
                    if sum1 in keylist or sum2 in keylist or sum3 in keylist or sum4 in keylist or sum5 in keylist or sum6 in keylist:
                        flag = False
            if (ssum not in keylist and flag):
                img.putpixel((x,y),(255,255,255))
    for x in range(0,width):
        for y in range(0,heigth):    
            if img.getpixel((x,y))==(255,255,255,255):
                continue
            else:
                img.putpixel((x,y),(0,0,0,255))
                        #curImg.setRGB(x, y, Color.white.getRGB())  
    img.save('captcha2.png')


def two(img3): #img：图片地址 
    i = 0
    #img = Image.open('/home/yang/png/0.png') # 读入图片
    img = Image.open(img3)
    img = img.convert("RGBA")
    while i < 4:#循环次数视情况进行调整
        i = i+1
        pixdata = img.load()
        #一次二值化
        
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < 90:#使RGB值中R小于90的像素点变成纯黑
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 190:#使RGB值中G小于90的像素点变成纯黑
                        pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:#使RGB值中B大于0的像素点变成纯白
                    pixdata[x, y] = (255, 255, 255, 255)
      
              
    #理论上的二值化代码只有上面那些，RGB值的调整阈值需要针对不同验证码反复调整。同时实际中一组阈值往往没法做到完美，后面的部分是视实际情况添加的类似部分
  
 
    #二次二值化（除去某些R、G、B值接近255的颜色）                 
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 254:
                pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 254:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)
 
    #三次二值化，怼掉纯黄色（实际使用中发现很多图片最后剩几个纯黄色的像素点）               
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] ==(255,255,0,255):
                pixdata[x, y] = (0, 0, 0, 255)
 
    img.save('captcha3.png')

def getPage(name, pCode, captchaId, page, url, headers):
    data = {
        'pName': name,
        'pCardNum' : '', 
        'selectCourtId': '0',
        'pCode': pCode,
        'captchaId': captchaId,
        'searchCourtName': '全国法院（包含地方各级法院）',
        'selectCourtArrange': '1',
        'currentPage': str(page)
    }
    web2 = requests.post(url + 'searchZhcx.do', data = data, headers = headers).content.decode('utf-8')
    #print(type(web2))
    
    web2 = web2.encode()
    with open('json2\jsonArray' + str(page) +  '.json', 'wb') as jsonFile:
        jsonFile.write(web2)
    jsonFile.close()
    
    with open('json2\jsonArray' + str(page) +  '.json', "r", encoding='utf-8') as jsonFile:
        loadDict = json.load(jsonFile)
    
    jsonData = json.loads(web2)
    #print(type(jsonData))
    jsonPage = []
    for case in range(0, len(loadDict[0]['result'])):
    #for case in range(0, len(jsonData[0]['result'])):
        #caseCodeNewDel = jsonData[0]['result'][case]['caseCode']
        caseCodeNewDel = loadDict[0]['result'][case]['caseCode']
        #print('caseCodeNewDel: ' + caseCodeNewDel)

        url2 = 'http://zxgk.court.gov.cn/zhzxgk/detailZhcx.do?pnameNewDel=' + name + '&cardNumNewDel=&j_captchaNewDel=' + pCode + '&caseCodeNewDel=' + caseCodeNewDel + '&captchaIdNewDel=' + captchaId
        #webbrowser.open(url2)
        web3 = requests.get(url2, headers = headers).content.decode('utf-8')
        soup = BeautifulSoup(web3, 'lxml')
        trs = soup.find_all('td')
        #index = -1
        dictD = {}
        for i in range(0, len(trs)):
            if i % 2 == 0:
                item = trs[i].strong.string
                #print(trs[i].string + '\t', end='')
            else:
                val = trs[i].string
                #print(trs[i].string)
                dictD.update({item: val})
        jsonPage.append(dictD)
    print('Page: ' + str(page))
    with open('json2\jsonPage' + str(page) + '.json', 'wb') as jsonFile:
        jsonFile.write(str(jsonPage).encode())
    jsonFile.close()

if __name__ == "__main__":
    #name = input('请输入被执行人的姓名：')
    name = '张晓东'
    url = "https://zxgk.court.gov.cn/zhzxgk/"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=6FC64237B107193D0844986FA832141E; _gscu_15322769=57994001imyfys20; Hm_lvt_d59e2ad63d3a37c53453b996cb7f8d4e=1559872944,1559875214,1559954172,1560040199; FSSBBIl1UgzbN7N80S=HMZrR8ppJnML_zZ7Rwa1fZDn8xJmkfS9Qz9wCK2MeMIhC.UZ9aCOYM7w_ouZ5gvM; SESSION=9eee440f-c8e0-4414-b876-03eb057b4a76; _gscbrs_15322769=1; _gscs_15322769=60063885ubyxbg12|pv:5; Hm_lpvt_d59e2ad63d3a37c53453b996cb7f8d4e=1560064497; FSSBBIl1UgzbN7N80T=35.wM0L0l48IGlyG1aAHD.Hy_sU2cYggXVxkRqp8jOa0.luxobSUy2bLGB_7CNxu.MZVQEGpXGqFggEUl2qZ9VJFMwxBHep6agOmqefy1lnYtvxBGh.aBoJyzyLvtqs8MEm2dt.kaxgn8UWNZvt4pX6jIg11zDPV6nhDnJrcfOAgIxwNxyjnkFsBzaOhxN6hR2SxsMjxtgZFrUSEW.MNUx.MViXHk0qILe_iVa3VBqbSvElGAwZIWvUFlbLnUkfQH06bR8mIwEXteKU88cbu0QF6siNfm7TIahvk2XjBDufSFyGVQlVzz8FnrwgTd.9cVOUtYR9rkmsL5O_xiYpqGV2Lw7fFH.TSXXk6wLgVdIjj77q',
        'Host': 'zxgk.court.gov.cn',
        'Referer': 'https://zxgk.court.gov.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    #webbrowser.open('https://zxgk.court.gov.cn/zhzxgk/')
    web = requests.get(url, headers = headers).content.decode('utf-8')
    with open('webFile.html', 'wb') as webFile:
        webFile.write(web.encode())
    soup = BeautifulSoup(web, 'lxml')
    imgSrc = soup.find('img', attrs = {'id' : 'captchaImg'})['src']
    imgUrl = url + imgSrc + '/captcha.jpg'
    urllib.request.urlretrieve(imgUrl, 'captcha.jpg')
    captchaId = imgSrc.split('?')[1].split('&')[0].split('=')[1]
    print('imgUrl: ' + imgUrl)
    print('captchaId: ' + captchaId)
    '''
    fall('captcha.jpg')
    ganraoxian('captcha1.png')
    two('captcha2.png')
    info = Image.open('captcha3.png')
    imageInfo = pytesseract.image_to_string(info)
    print(imageInfo)
    '''
    webbrowser.open(imgUrl)
    pCode = input('请输入验证码：')
    print('开始扒取数据：')
    threads = []
    for page in range(1, 113):
        t = Thread(target=getPage, args=(name, pCode, captchaId, page, url, headers))
        t.start()
        threads.append(t)

    for i in threads:
        i.join()