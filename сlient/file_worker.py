import os


def create_dir(dir_path):
    const_dir_name = os.getcwd()
    for dir_name in dir_path.split('/'):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        os.chdir(dir_name)
    os.chdir(const_dir_name)
