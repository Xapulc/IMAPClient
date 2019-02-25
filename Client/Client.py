from imaplib import IMAP4, IMAP4_SSL
from socket import gaierror
from email import message_from_bytes
from pickle import dump, load
import os


class Client(object):
    def __init__(self):
        self._client: IMAP4_SSL = None
        self._host: str = None
        self._port: int = 993
        self._auth_path = "res/auth_data"

        if not self._use_old_data(): # обработай случай, когда я хочу юзать старые данные, но они уже не действительны
            self._connect()
            self._login()
        else:
            host, login, password = self._load_data()
            self._connect(host)
            self._login(login, password)

    def _use_old_data(self):
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

    def _save_data(self, host, login, password):
        const_dir_name = os.getcwd()
        for dir_name in self._auth_path.split('/')[:-1]:
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            os.chdir(dir_name)
        os.chdir(const_dir_name)

        with open(self._auth_path, "wb") as file:
            dump((host, login, password), file)

    def _load_data(self):
        with open(self._auth_path, "rb") as file:
            data = load(file)
        return data

    def _connect(self, hostname=None):
        self._host = hostname
        while self._host is None:
            self._host = input("Enter host name: ")
            try:
                self._client = IMAP4_SSL(host=self._host, port=self._port)
            except gaierror as err:
                print(err)
                self._host = None
            except TimeoutError as err:
                print(err)
                print("Effort of reconnection")
                self._connect(hostname)
            else:
                break
        else:
            self._client = IMAP4_SSL(host=self._host, port=self._port)

    def _login(self, mail=None, password=None):
        while mail is None and password is None:
            try:
                mail, password = input("Enter your mail and password: ").split(' ')
                self._client.login(user=mail, password=password)
            except ValueError:
                print("Please, enter data in right format, i.e. 'petya_pupkin@mail.com qwerty123'")
                mail = None
                password = None
            except IMAP4.error as err:
                print(err)
                if str(err).find("WinError") == -1:
                    answer = input("Do you want to use this login and password for connection?")
                    if answer == "yes":
                        self._login(mail, password)
                mail = None
                password = None
            else:
                break
        else:
            self._client.login(user=mail, password=password)

        self._save_data(self._host, mail, password)

    def request(self):
        while True:
            req_str = input("Enter your request: ")
            req: list = req_str.split()
            if len(req) >= 2 and req[0] == "get" and req[1] == "all":
                self.get_all_files()
                return True
            elif len(req) >= 1 and req[0] == "exit":
                return False
            else:
                self._help()

    def get_all_files(self):
        status, msgs = self._client.select("INBOX", True)
        if status != "OK":
            return

        status, num_messages = self._client.search("utf-8", "SUBJECT", "group")
        if status != "OK":
            return

        for num in num_messages[0].split():
            status, message = self._client.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            mail = message_from_bytes(message[0][1])

            if mail.is_multipart():
                for part in mail.walk():
                    content_type = part.get_content_type()
                    filename = part.get_filename()
                    if filename:
                        with open(f"{filename}", 'wb') as new_file: # нормально сохрани файлы
                            new_file.write(part.get_payload(decode=True))

    def close(self):
        if self._client is not None:
            self._client.logout()

    def _help(self):
        print(f'''****************
        You can use following methods:
        get all: get all files in mails, which consist 'group' in theme
        exit: exit client
****************''')
