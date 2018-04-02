#-*- coding:utf-8 -*-
import urllib2
import json
import string
import time
import signal


def handler(signum, frame):
    raise AssertionError

def get_url_data(url, num_retries = 2):
    try:
        print 'Downloading http...'
        request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=10)
        data = response.read()
    except urllib2.URLError as e:
        print 'Download http error:'.e.reason
        data = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return get_url_data(url, num_retries -1)
    return data


def decode_url(url):
    in_table = u'0123456789abcdefghijklmnopqrstuvw'
    out_table = u'7dgjmoru140852vsnkheb963wtqplifca'
    translate_table = string.maketrans(in_table, out_table)
    mapping = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
    for k, v in mapping.items():
        url = url.replace(k, v)
    url = url.encode()
    return url.translate(translate_table)

def get_img_url(url_data):
    true_urls = []
    jd = json.loads(url_data)
    for i in range(len(jd['data'])):
        try:
            true_url = decode_url(jd['data'][i]['objURL'])
        except:
            print '没有找到第',i, '个objURL...'
            continue
        true_urls.append(true_url)
    return true_urls

def save_img(img, save_addr, num):
    with open(save_addr + str(num) + '.jpg', 'wb') as w:
        print 'downloading ' + str(num) + ' image ......',
        w.write(img.read())
        print 'success'

def download_img(img_url, save_addr, num, num_retries = 2):
    try:
        img = urllib2.urlopen(img_url, timeout=10)
    except urllib2.URLError as e:
        print 'Download img error:', e.reason
        if num_retries > 0:
            print '正在第',3-num_retries, '次尝试重新下载图片'
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download_img(img_url, save_addr, num, num_retries -1)
        return None
    try:
        save_img(img, save_addr, num)
    except:
        print "save image timeout"

def get_dst_url(dst_url_head, page):
    pn = dst_url_head.find('&pn=')
    rn = dst_url_head.find('&rn=')
    gsm = dst_url_head.find('&gsm=')
    dst_url = dst_url_head[0:pn+4] + str(page * 30) + dst_url_head[rn:gsm+5] + str(hex(page * 30).lstrip('0x'))


dst_url_head = r'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E4%BA%A4%E8%AD%A6+%E6%8C%87%E6%8C%A5&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E4%BA%A4%E8%AD%A6+%E6%8C%87%E6%8C%A5&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=60&rn=30&gsm=3c '
save_addr = 'E:\\download_img\\baidu\\'


#Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding":"gzip",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Referer":"http://http://www.baidu.com/",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
                }

if __name__ == '__main__':
    num_d = 0
    for page in range(1,201):
        dst_url = get_dst_url(dst_url_head, page)
        print '开始下载第' + str(page) + '页.....'

        src_url_data = get_url_data(dst_url_head)
        if src_url_data is None:
            continue
        imgs_url = get_img_url(src_url_data)
        for img_url in imgs_url:
            try:
                download_img(img_url, save_addr, num_d)
            except:
                print '下载失败：',img_url,
                continue

            num_d += 1

    print '下载完成......'




