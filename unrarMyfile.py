#-*- coding:utf-8 -*-

import os
import rarfile
import shutil

#解决解压过程中中文路径的问题
import sys
reload(sys)
sys.setdefaultencoding('gbk')


def unrarMyfile(dst_dir):
    #获取一级目录
    file0_list = os.listdir(unicode(dst_dir,"utf-8"))
    for file0 in file0_list:
        file0_dir = os.path.join(unicode(dst_dir,"utf-8"),file0)
        #判断当前是否为文件是否为目录文件
        if os.path.isdir(file0_dir) :
            #获取二级目录
            file1_list = os.listdir(file0_dir)
            for file1 in file1_list:
                file1_dir = os.path.join(file0_dir, file1)
                #判断当前文件是否为rar压缩包
                if file1_dir[-3:] == 'rar':
                    print '正在解压……'+ str(file1_dir).encode('utf-8')
                    rar = rarfile.RarFile(file1_dir)
                    rar.extractall(path=file0_dir)
                    rar.close()


dst_dir = r'F:\学习\5  C++ Primer中级'
unrarMyfile(dst_dir)

