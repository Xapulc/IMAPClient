import os


def create_dir(dir_path: str):
    """
    Create a new directory;
    If parent folder doesn't exists, method create it too
    :param dir_path:  way to directory
    """
    const_dir_name = os.getcwd()
    for dir_name in dir_path.split('/'):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        os.chdir(dir_name)
    os.chdir(const_dir_name)


def get_files(path: str = '.'):
    """
    Get files in path; By default - current directory
    :param path: way to folder in which need to get files
    """
    return list(os.walk(path))[0][2]


def get_dirs(path: str = '.'):
    """
    Get directories in path(not files); By default - current directory
    :param path: way to folder in which need to get directories
    :return:
    """
    return list(os.walk(path))[0][1]


def goto(path: str):
    """
    Change directory function
    Functions' work like CD in command line or terminal
    """
    os.chdir(path)


def back():
    """
    Go to parent folder
    """
    goto("..")
