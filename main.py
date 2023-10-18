import requests as req
from lxml import etree
import random
import threading

#通过fiddler，打开群精华获取
p_skey = ""
skey = ""
#QQ号
qq_account = ""
#群号
group_id = ""
download_thread_num = 3
illegal_chars = ['\\', '/', '*', '?', ':', '"', '<', '>', '|']

def random_len(length):
    return random.randrange(int('1' + '0' * (length - 1)), int('9' * length))

url = 'https://qun.qq.com/essence/indexPc?gc=' + group_id + '&seq=' + str(random_len(8)) + '&random=' + str(random_len(10))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) QQ/9.6.5.28778 '
                'Chrome/43.0.2357.134 Safari/537.36 QBCore/3.43.1298.400 QQBrowser/9.0.2524.400',
    'Host': 'qun.qq.com',
    'Cookie': 'p_skey='+p_skey+'; p_uin=o'+ qq_account + '; uin=o' + qq_account + '; skey='+skey
}

response = req.get(url, headers=headers)
response.encoding = 'UTF-8'
data = etree.HTML(response.text)
totalData = []
#记录所有图片链接
download_list=[]

for i in range(1,len(data.xpath('//*[@id="app"]/div[2]/*'))):
    essence = {"qq_account": '', "qq_name": '', "send_time": '', "content": []}
    current_pos = '//*[@id="app"]/div[2]/div[' + str(i) + ']'
    essence["qq_account"] = data.xpath(current_pos+'/div[1]/@style')[0][10:-2].split('/')[5]
    essence["qq_name"] = data.xpath(current_pos+'/div[2]')[0].text.strip(" \n")
    essence["send_time"]=data.xpath(current_pos+'/div[3]')[0].text.strip(" \n")
    #处理内容div
    content_node_class = data.xpath(current_pos+'/div[last()-1]/@class')
    #图文/纯文本
    if len(content_node_class) > 0 and content_node_class[0] == 'short':
        for j in data.xpath(current_pos+'/div[last()-1]/*'):
            if j.tag == 'span':
                content = j.text
                essence["content"].append(content)
            elif j.tag == 'img':
                content = j.attrib.get('src')[0:-10]
                essence["content"].append(content)
                download_list.append(content)
    else:
        inside_node_class = data.xpath(current_pos+'/div[last()-1]/div/@class')
        #外部引用
        if len(inside_node_class)>0:
            if inside_node_class[0] == 'img_wrap':
                img = data.xpath(current_pos+'/div[last()-1]/div/img/@src')[0]
                filename = data.xpath(current_pos+'/div[last()-1]/div/div[last()]')[0].text.strip(' \n')
                essence["content"].append(img)
                download_list.append(img)
                essence["content"].append(filename)
            elif inside_node_class[0] == 'doc_wrap':
                title = data.xpath(current_pos+'/div[last()-1]/div/div[1]')[0].text.strip(' \n')
                image = data.xpath(current_pos+'/div[last()-1]/div/i/@style')[0][21:].split(')')[0]
                source = data.xpath(current_pos+'/div[last()-1]/div/div[2]')[0].text.strip(' \n')
                essence["content"].append(title)
                essence["content"].append(image)
                download_list.append(image)
                essence["content"].append(source)
            else:
                print("error: inside_node_class but class:" + inside_node_class[0])
        #纯图片
        else:
            img = data.xpath(current_pos+'/div[last()-1]/div/img/@src')[0][0:-10]
            essence["content"].append(img)
            download_list.append(img)
    totalData.append(essence)
#输出txt文件
file = open("output.txt","w",encoding = "utf-8")
for i in totalData:
  file.write(repr(i))
  file.write('\n')
file.close()

#下载图片(可选，自行修改代码调用download_pic)
def download(imglist):
    for i in imglist:
        imgdata = req.get(i).content
        name = i.split('/')[-1].split('&')[0].split('=')[-1]
        if not '.' in name[-5:]:
            name = name + '.jfif'
        for char in illegal_chars:
            name = name.replace(char,'_')
        with open('img/' + name,'wb') as f:
            f.write(imgdata)
            f.close()

#多线程下载图片至img文件夹下
def download_pic(download_list):
  download_list = list(set(download_list))
  length = len(download_list)//download_thread_num
  for i in range(download_thread_num):
      if i != download_thread_num-1:
          download_thread = threading.Thread(target=download,args=(download_list[i*length:(i+1)*length],))
      else:
          download_thread = threading.Thread(target=download,args=(download_list[i*length:],))
      download_thread.start()
