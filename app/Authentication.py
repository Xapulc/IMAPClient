from pickle import dump, load

from app.file_worker import create_dir, get_files


class Authentication(object):

    def __init__(self, path: str):
        """
        :param path: Path to authentication file
        """
        self._auth_path = path

    def use_old_data(self):
        """
        Find file authentication data
        And ask user about using old data
        :return: True if need to use old data, else False; Also False if data doesnt exist
        """
        index = self._auth_path.rfind('/')
        dir_name = '.' if index == -1 else self._auth_path[:index]
        if self._auth_path[index + 1:] not in get_files(dir_name):
            print("Auth data doesn't exist")
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
        """
        Save data in file
        """
        ind_of_last_slash = self._auth_path.rfind('/')
        if ind_of_last_slash != -1:
            create_dir(self._auth_path[:ind_of_last_slash])

        with open(self._auth_path, "wb") as file:
            dump((host, login, password), file)

    def load_data(self) -> tuple:
        """
        Load data from file
        """
        with open(self._auth_path, "rb") as file:
            data = load(file)
        return data
