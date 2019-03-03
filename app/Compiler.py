import os

from app.file_worker import get_files, get_dirs, goto, back


class Compiler(object):
    def __init__(self):
        self._c_types = {'.c'}
        self._cpp_types = {'.cc', '.cpp', '.cxx', '.c++'}

    def compile_all(self):
        if "Makefile" in get_files():
            self._make()
            return

        for file_name in get_files():
            if file_name[file_name.rfind('.'):] in self._c_types:
                self._compile_c(file_name)
            elif file_name[file_name.rfind('.'):] in self._cpp_types:
                self._compile_cpp(file_name)

        for dir_name in get_dirs():
            goto(dir_name)
            self.compile_all()
            back()

    def _compile_cpp(self, file_name: str):
        os.system(f"g++ {file_name}")

    def _compile_c(self, file_name: str):
        os.system(f"gcc {file_name}")

    def _make(self):
        os.system("make")
