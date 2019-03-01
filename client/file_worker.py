import os


def create_dir(dir_path: str):
    const_dir_name = os.getcwd()
    for dir_name in dir_path.split('/'):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        os.chdir(dir_name)
    os.chdir(const_dir_name)


def get_files():
    return os.walk('.')[2]


def get_dirs():
    return os.walk('.')[1]


def goto(dir_name: str):
    os.system(f"cd {dir_name}")


def back():
    os.system("..")
