from subprocess import run, PIPE, CompletedProcess

from app.Compile_log import Log
from app.file_worker import get_files, get_dirs, goto, back


class Compiler(object):
    """
    Class is need for compilation C and C++
    """
    def __init__(self, path):
        self._path = path
        self._c_types = {'.c'}
        self._cpp_types = {'.cc', '.cpp', '.cxx', '.c++'}

    def get_log(self, name: str, complProc: CompletedProcess):
        return Log(name, complProc.stderr, True if complProc.returncode == 0 else False)

    def compile_all(self):
        """
        Recursively compile all files in current directory and its subdirectories
        """
        logs = []
        if "Makefile" in get_files():
            logs.append(self.get_log(path, self._make()))
        else:
            for file_name in get_files():
                if file_name[file_name.rfind('.'):] in self._c_types:
                    complProc = self._compile_c(file_name)
                elif file_name[file_name.rfind('.'):] in self._cpp_types:
                    complProc = self._compile_cpp(file_name)

        for dir_name in get_dirs():
            goto(dir_name)
            self.compile_all()
            back()

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
