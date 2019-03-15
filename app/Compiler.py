from subprocess import run, PIPE, CompletedProcess
from os.path import abspath
from os import chdir

from app.Compile_log import Log
from app.file_worker import get_files, get_dirs, goto, back


def get_log(name: str, compl_proc: CompletedProcess):
    return Log(name, compl_proc.stderr, True if compl_proc.returncode == 0 else False)


class Compiler(object):
    """
    Class is need for compilation C and C++
    """
    def __init__(self):
        self._c_types = {'.c'}
        self._cpp_types = {'.cc', '.cpp', '.cxx', '.c++'}

    def compile_all(self, path='.'):
        """
        Recursively compile all files in current directory and its subdirectories
        :param path: needs for log
        """
        logs = []
        if "Makefile" in get_files():
            logs.append(get_log(path, self._make()))
        else:
            for file_name in get_files():
                point_ind = file_name.rfind('.')
                if file_name[point_ind:] in self._c_types:
                    logs.append(get_log(f"{path}/{file_name}", self._compile_c(file_name)))
                elif file_name[point_ind:] in self._cpp_types:
                    logs.append(get_log(f"{path}/{file_name}", self._compile_cpp(file_name)))

        for dir_name in get_dirs():
            goto(dir_name)
            logs += self.compile_all(f"{path}/{dir_name}")
            back()

        return logs

    def compile_direct(self, path='.'):
        start_dir = abspath('.')
        chdir(path)
        logs = self.compile_all(path)
        chdir(start_dir)
        return logs

    def _compile_cpp(self, file_name: str):
        """
        Compile C++ file
        """
        return run(["g++", file_name], stdout=PIPE, stderr=PIPE, encoding='utf-8')

    def _compile_c(self, file_name: str):
        """
        Compile C file
        """
        return run(["gcc", file_name], stdout=PIPE, stderr=PIPE, encoding='utf-8')

    def _make(self):
        """
        Build project in current directory
        """
        return run(["make"], stdout=PIPE, stderr=PIPE, encoding='utf-8')
