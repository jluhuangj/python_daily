#-*- coding:utf-8 -*-

import os
import shutil


def moveMyfile(dst_dir):
    file0_list = os.listdir(unicode(dst_dir,'utf-8'))

    for file0 in file0_list:
        file0_dir = os.path.join(unicode(dst_dir,"utf-8"),file0)

        if os.path.isdir(file0_dir):
            file1_list = os.listdir(file0_dir)

            for file1 in file1_list:
                if file1[-3:] == 'wmv':
                    #重命名
                    srcName = os.path.join(file0_dir,file1)
                    dstNname = os.path.join(file0_dir,file0+'.wmv')
                    os.rename(srcName,dstNname)

                    #剪贴文件
                    dstAdr = os.path.join(unicode(dst_dir,'utf-8'),file0+'.wmv')
                    print '正在移动'+str(dstNname)
                    shutil.move(dstNname,dstAdr)




dst = r'F:\学习\5  C++ Primer中级'
moveMyfile(dst)