import os


def create_dir(dir_path: str):
    const_dir_name = os.getcwd()
    for dir_name in dir_path.split('/'):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        os.chdir(dir_name)
    os.chdir(const_dir_name)


def get_files(dir_name: str = '.'):
    return list(os.walk(dir_name))[0][2]


def get_dirs():
    return list(os.walk('.'))[0][1]


def goto(dir_name: str):
    os.chdir(dir_name)


def back():
    os.chdir("..")
