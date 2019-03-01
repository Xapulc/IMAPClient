from pickle import dump, load

from client.file_worker import create_dir


class Authentication(object):
    def __init__(self, path: str):
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
        ind_of_last_slash = self._auth_path.rfind('/')
        if ind_of_last_slash != -1:
            create_dir(self._auth_path[:ind_of_last_slash])

        with open(self._auth_path, "wb") as file:
            dump((host, login, password), file)

    def load_data(self):
        with open(self._auth_path, "rb") as file:
            data = load(file)
        return data
