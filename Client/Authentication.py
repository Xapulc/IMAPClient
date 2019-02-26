from pickle import dump, load
import os


class Authentication(object):
    def __init__(self, path):
        self._auth_path = path

    def use_old_data(self):
        try:
            with open(self._auth_path, "rb") as _:
                pass
        except FileNotFoundError:
            return False

        while True:
            answer = input("Do you want to use old data?")
            if answer == "yes":
                return True
            elif answer == "no":
                return False
            else:
                print("Please, enter 'yes' or 'no'")

    def save_data(self, host, login, password):
        const_dir_name = os.getcwd()
        for dir_name in self._auth_path.split('/')[:-1]:
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            os.chdir(dir_name)
        os.chdir(const_dir_name)

        with open(self._auth_path, "wb") as file:
            dump((host, login, password), file)

    def load_data(self):
        with open(self._auth_path, "rb") as file:
            data = load(file)
        return data
