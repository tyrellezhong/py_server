import getopt
import sys
import os


def get_opt(argv):
    # 定义短选项和长选项
    short_opts = "-h:v"
    long_opts = ["help=", "verbose"]

    # 解析命令行参数
    try:
        # "hi:o:": 短格式分析串, h 后面没有冒号, 表示后面不带参数; i 和 o 后面带有冒号, 表示后面带参数
        # ["help", "input_file=", "output_file="]: 长格式分析串列表, help后面没有等号, 表示后面不带参数; input_file和output_file后面带冒号, 表示后面带参数
        # 返回值包括 `opts` 和 `args`, opts 是以元组为元素的列表, 每个元组的形式为: (选项, 附加参数)，如: ('-i', 'test.png');
        # args是个列表，其中的元素是那些不含'-'或'--'的参数
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except getopt.GetoptError:
        print("Invalid command line arguments")
        sys.exit(2)

    # 处理选项
    verbose = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage: python myprogram.py [-h|--help] [-v|--verbose] [file ...]")
            sys.exit()
        elif opt in ("-v", "--verbose"):
            verbose = True

    # 处理参数
    for arg in args:
        print("Processing file:", arg)

    # 打印选项和参数
    print("Verbose mode:", verbose)
    print("Remaining arguments:", args)

def GetParentPath(strPath):
    if not strPath:
        return None

    lsPath = os.path.split(strPath)
    if lsPath[1]:
        return lsPath[0]

    lsPath = os.path.split(lsPath[0])
    return lsPath[0]

def path_test():
    file_path = os.path.realpath(__file__)
    dir = os.path.dirname(file_path)
    file_parent = GetParentPath(dir)
    cur_path = sys.path[0]
    xx = 0