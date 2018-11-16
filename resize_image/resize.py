from __future__ import print_function
import sys,os
import cv2

def max_dis_resize(src_img, max_dis):

    max_edge = len(src_img) if len(src_img) > len(src_img[0]) else len(src_img[0])
    print(max_edge, max_dis)
    print(type(max_edge), type(max_dis))
    if max_edge > max_dis :
        rate = float(max_dis)/max_edge
    else:
        return []

    cols = int(len(src_img[0])*rate)
    rows = int(len(src_img)*rate)
    save_img = cv2.resize(src_img, (cols, rows))

    return save_img

def col_row_resize(src_img, dst_width, dst_height):
    save_img = cv2.resize(src_img, (dst_width, dst_height))

    return save_img

if __name__ == '__main__':

    if len(sys.argv) == 4:
        src_dir  = sys.argv[1]
        save_dir = sys.argv[2]
        max_dis  = int(sys.argv[3])
    elif len(sys.argv) == 5:
        src_dir  = sys.argv[1]
        save_dir = sys.argv[2]
        dst_width  = int(sys.argv[3])
        dst_height  = int(sys.argv[4])
    else:
        print("please input:")
        print('\t{} src_img_dir save_img_dir max_dis'.format(__file__))
        print('\t{} src_img_dir save_img_dir dst_width dst_height'.format(__file__))
        sys.exit()

    for file in os.listdir(src_dir):
        print("process {} ...".format(file))

        src_img_path = os.path.join(src_dir, file)
        src_img = cv2.imread(src_img_path)

        if len(sys.argv) == 4:
            save_img = max_dis_resize(src_img, max_dis)
        else:
            save_img = col_row_resize(src_img, dst_width, dst_height)

        if len(save_img) == 0:
            continue

        save_img_path = os.path.join(save_dir, file)
        cv2.imwrite(save_img_path, save_img)
