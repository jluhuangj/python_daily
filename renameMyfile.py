#-*- coding:utf-8 -*-

import os

dst_dir = r'E:\download_img\baidu2'
dst_dir_list = os.listdir(dst_dir)

for i,file in enumerate(dst_dir_list):
    src_file = os.path.join(dst_dir, file)
    dst_file = os.path.join(dst_dir, str(i) +  '.jpg')
    os.rename(src_file, dst_file)
