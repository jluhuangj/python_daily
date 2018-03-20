#-*- coding:utf-8 -*-
import os
import shutil


def removeMyfile(dst_dir):
    file0_list = os.listdir(unicode(dst_dir,'utf-8'))

    for file0 in file0_list:
        file0_dir = os.path.join(unicode(dst_dir,'utf-8'), file0)

        if os.path.isdir(file0_dir):
            #利用shutil删除非空文件夹，删除空文件夹可以使用os.remove()
            print '正在删除……'+file0_dir
            shutil.rmtree(file0_dir)



dst_dir = r'F:\学习\5  C++ Primer中级'
removeMyfile(dst_dir)