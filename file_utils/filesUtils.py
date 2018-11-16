#-*- coding:utf8 -*-
from __future__ import print_function

import sys
import os
import shutil
import readline
import json

mode_info =  '\nmode options:\n'
mode_info += '@ 1: del\n'
mode_info += '@ 2: move\n'
mode_info += '@ 3: copy\n'

del_info =  '\n@ 删除src里和conf共有的file\n'
del_info += '@ src、conf均可为文件夹或文本\n'

move_info =  '\n@ 既在src也在conf里的file move => dst\n'
move_info += '@ src、conf、dst均可为文件夹或文本\n'

copy_info =  '\n@ 既在src也在conf里的file copy => dst\n'
copy_info += '@ src、conf、dst均可为文件夹或文本\n'

def completer(text, state):
    options = [cmd for cmd in CMD if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

def get_files_from_dir(dir):
    return os.listdir(dir)

def get_files_from_file(conf_file):
    with open(conf_file) as f:
        f_data = f.readlines()
    f_data = [line.strip() for line in f_data]
    return f_data

def get_files(src):
    src_list = []
    if os.path.isdir(src):
        src_list = get_files_from_dir(src)
    else:
        src_list = get_files_from_file(src)
    return src_list

def get_union(src1_list, src2_list, reverse):
    dst_list = []
    for file1 in src1_list:
        if not reverse:
            if file1 in src2_list:
                dst_list.append(file1)
        else:
            if file1 not in src2_list:
                dst_list.append(file1)
    return dst_list

def get_true_files(src_list, dst_list):
    ret = []
    for file_true in src_list:
        for file in dst_list:
            if file in file_true:
                ret.append(file_true)
    return ret

def del_files_from_dst_dir(del_list_true, dst):
    print()
    for file in del_list_true:
        print('start removing {}'.format(file))
        file_path = os.path.join(dst, file)
        os.remove(file_path)
    print()

def del_result_from_dst_file(del_list, dst):
    src_list = get_files_from_file(dst)
    save_list = []
    for file in src_list:
        if file in del_list:
            continue
        save_list.append(file)
    save_result_to_dst_file(save_list, dst)

def delete(conf_dict = {}):
    if len(conf_dict) == 0:
        print(del_info)
        if sys.version_info.major < 3:
            line_argv = raw_input('src conf\n')
        else:
            line_argv = input('src conf\n')
        line_argv = line_argv.split()
        if len(line_argv) != 2:
            print('parse error ...')
            return

        src = line_argv[0]
        conf = line_argv[1]

        print('\n是否reverse(删除src里独有的file)?, 默认no')
        if sys.version_info.major < 3:
            reverse = raw_input('please set reverse(y or n): ')
        else:
            reverse = input('please set reverse(y or n): ')
        if reverse == 'yes' or reverse == 'y':
            reverse = True
        else:
            reverse = False
    else:
        try:
            src = conf_dict['src']
            print("src: {}".format(src))

            conf = conf_dict['conf']
            print("conf: {}".format(conf))

            if conf_dict['reverse'] == "yes":
                reverse = True
                print("reverse: yes")
            else:
                reverse = False
                print("reverse: no")
        except:
            print("conf file parse false")
            sys.exit()


    # get files from src
    src_list = get_files(src)
    src_list_new = [file.split('.')[0] for file in src_list]

    # get files from dst
    conf_list = get_files(conf)
    conf_list_new = [file.split('.')[0] for file in conf_list]

    # get union of files1 and files2
    del_list = get_union(src_list_new, conf_list_new, reverse)

    # get true files from dst
    del_list_true = get_true_files(src_list, del_list)

    # del result from dst
    if os.path.isfile(src):
        del_result_from_dst_file(del_list_true, src)
    elif os.path.isdir(src):
        del_files_from_dst_dir(del_list_true, src)

    print('success...')

def save_result_to_dst_file(result, dst_file):
    str_res = '\n'.join(result)
    with open(dst_file, 'w') as f:
        f.write(str_res)

def move_files_to_dst_dir(result, src1_dir, dst_dir):
    print()
    for file in result:
        print('start moving {}'.format(file))
        src_file_path = os.path.join(src1_dir, file)
        dst_file_path = os.path.join(dst_dir, file)
        shutil.move(src_file_path, dst_file_path)
    print()

def move(conf_dict = {}):
    if len(conf_dict) == 0:
        print(move_info)
        if sys.version_info.major < 3:
            line_argv = raw_input('src conf dst\n')
        else:
            line_argv = input('src conf dst\n')
        line_argv = line_argv.split()
        if len(line_argv) != 3:
            print('parse error ...')
            return

        src = line_argv[0]
        conf = line_argv[1]
        dst = line_argv[2]

        print('\n是否reverse(copy src里独有的file到dst)?, 默认no')
        if sys.version_info.major < 3:
            reverse = raw_input('please set reverse(y or n): ')
        else:
            reverse = input('please set reverse(y or n): ')
        if reverse == 'yes' or reverse == 'y':
            reverse = True
        else:
            reverse = False
    else:
        try:
            src = conf_dict['src']
            print("src: {}".format(src))

            conf = conf_dict['conf']
            print("conf: {}".format(conf))

            dst  = conf_dict['dst']
            print("dst: {}".format(dst))

            if conf_dict['reverse'] == "yes":
                reverse = True
                print("reverse: yes")
            else:
                reverse = False
                print("reverse: no")
        except:
            print("conf file parse false")
            sys.exit()


    # get files1 from src
    src_list = get_files(src)
    src_list_no_post = [file.split('.')[0] for file in src_list]

    # get files2 from conf
    conf_list = get_files(conf)
    conf_list_no_post = [file.split('.')[0] for file in conf_list]

    # get union of files1 and files2
    dst_list_no_post = get_union(src_list_no_post, conf_list_no_post, reverse)

    # get true union files from files1
    dst_list = get_true_files(src_list, dst_list_no_post)

    # save result to dst
    if os.path.isfile(src):
        save_result_to_dst_file(dst_list, dst)
    elif os.path.isdir(src):
        if '.' in dst:
            save_result_to_dst_file(dst_list, dst)
        else:
            move_files_to_dst_dir(dst_list, src, dst)

    print('success...')

def copy_files_to_dst_dir(result, src1_dir, dst_dir):
    print()
    for file in result:
        print('start copying {}'.format(file))
        src_file_path = os.path.join(src1_dir, file)
        dst_file_path = os.path.join(dst_dir, file)
        shutil.copy(src_file_path, dst_file_path)
    print()

def copy(conf_dict = {}):
    if len(conf_dict) == 0:
        print(copy_info)
        if sys.version_info.major < 3:
            line_argv = raw_input('src conf dst\n')
        else:
            line_argv = input('src conf dst\n')

        line_argv = line_argv.split()
        if len(line_argv) != 3:
            print('parse error ...')
            return

        src = line_argv[0]
        conf = line_argv[1]
        dst = line_argv[2]

        print('\n是否reverse(copy src里独有的file到dst)?, 默认no')
        if sys.version_info.major < 3:
            reverse = raw_input('please set reverse(y or n): ')
        else:
            reverse = input('please set reverse(y or n): ')

        if reverse == 'yes' or reverse == 'y':
            reverse = True
        else:
            reverse = False
    else:
        try:
            src  = conf_dict['src']
            print("src: {}".format(src))

            conf = conf_dict['conf']
            print("conf: {}".format(conf))

            dst  = conf_dict['dst']
            print("dst: {}".format(dst))

            if conf_dict['reverse'] == "yes":
                reverse = True
                print("reverse: yes")
            else:
                reverse = False
                print("reverse: no")
        except:
            print("conf file parse false")
            sys.exit()

    # get files1 from src
    src_list = get_files(src)
    src_list_no_post = [file.split('.')[0] for file in src_list]

    # get files2 from conf
    conf_list = get_files(conf)
    conf_list_no_post = [file.split('.')[0] for file in conf_list]

    # get union of files1 and files2
    dst_list_no_post = get_union(src_list_no_post, conf_list_no_post, reverse)

    # get true union files from files1
    dst_list = get_true_files(src_list, dst_list_no_post)

    # save result to dst
    if os.path.isfile(src):
        save_result_to_dst_file(dst_list, dst)
    elif os.path.isdir(src):
        if '.' in dst:
            save_result_to_dst_file(dst_list, dst)
        else:
            copy_files_to_dst_dir(dst_list, src, dst)

    print('success...')

def load_conf(conf):
    lines_data = get_files_from_file(conf)

    new_lines_data = []
    for line in lines_data:
        pos = line.find("#")
        if pos == -1:
            new_lines_data.append(line)
        else:
            if len(line[0:pos]):
                new_lines_data.append(line[0:pos])

    true_data = "".join(new_lines_data)

    json_data = json.loads(true_data)
    return json_data

def main(conf = None):
    if conf == None:
        print(mode_info)
        if sys.version_info.major < 3:
            mode = raw_input('please set mode: ')
        else:
            mode = input('please set mode: ')

        if mode == '1' or mode == 'del':
            delete()
        elif mode == '2' or mode == 'move':
            move()
        elif mode == '3' or mode == 'copy':
            copy()
    else:
        conf_dict = load_conf(conf)
        try:
            if conf_dict['mode'] == 'del':
                delete(conf_dict)
            elif conf_dict['mode'] == 'move':
                move(conf_dict)
            elif conf_dict['mode'] == 'copy':
                copy(conf_dict)
        except:
            sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 1:
        main()

