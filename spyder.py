import urllib2
import json

dst_url_head = 'http://search.quanjing.com/search?key=%E4%BA%A4%E8%AD%A6&pageSize=100&pageNum='
save_addr = 'E:\\download_img\\'
d_num = 6774

for page in range(70,101):
    try:
        request = urllib2.Request(dst_url_head+str(page))
        response = urllib2.urlopen(request)
        data = response.read()
        data = data.lstrip('searchresult(')
        data = data.rstrip(')')
        jd = json.loads(data)
        print 'It\'s ' + str(page)+ ' page:'
        for i in range(len(jd['imglist'])):
            img_url = jd['imglist'][i]["imgurl"]
            try:
                img = urllib2.urlopen(img_url)
                with open(save_addr+str(d_num)+'.jpg', 'wb') as w:
                    print 'downloading '+ str(d_num) +' image ......'
                    w.write(img.read())
                    d_num += 1
            except:
                print 'error'
    except:
        print 'get error'


print 'success...'


# with open('./1.txt', 'wb') as w:
#     w.write(data)