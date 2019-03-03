from imaplib import IMAP4, IMAP4_SSL
from socket import gaierror
from email import message_from_bytes

from app.Authentication import Authentication
from app.Compiler import Compiler
from app.file_worker import create_dir, goto, back


class Client(object):
    def __init__(self):
        self._compiler = Compiler()
        self._client: IMAP4_SSL = None
        self._host: str = None
        self._port: int = 993
        self._compile_res = "res"
        self._auth = Authentication(f"{self._compile_res}/auth_data")

        is_new_auth_session = True
        if self._auth.use_old_data():
            host, login, password = self._auth.load_data()
            self._connect(host)
            is_new_auth_session = not self._login(login, password)

        if is_new_auth_session:
            self._connect()
            self._login()

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
            try:
                self._client.login(user=mail, password=password)
            except IMAP4.error:
                print("You have some probles with you authentication data")
                return False

        self._auth.save_data(self._host, mail, password)
        return True

    def request(self):
        while True:
            req_str = input("Enter your request: ")
            req: list = req_str.split()
            if len(req) >= 2 and req[0] == "get" and req[1] == "all":
                self._get_all_files()
                return True
            elif len(req) >= 1 and req[0] == "compile":
                self._compile()
                return True
            elif len(req) >= 1 and req[0] == "exit":
                return False
            else:
                self._help()

    def _check_dir(self, dirname):
        dir_list = dirname.split('/')
        if len(dir_list) != 3:
            return False

        group, theme, person = dir_list
        if not group.isdigit():
            return False

        return True

    def _get_all_files(self):
        try:
            box = "INBOX"
            status, msgs = self._client.select(box, True)
            assert status == "OK", f"Can't select {box}"

            key_word = "group"
            status, num_messages = self._client.search("utf-8", "SUBJECT", key_word)
            assert status == "OK", f"Can't search {key_word}"

            for num in num_messages[0].split():
                status, message = self._client.fetch(num, "(RFC822)")
                if status != "OK":
                    continue

                mail = message_from_bytes(message[0][1])

                if mail.is_multipart():
                    dirname = '/'.join(mail["Subject"].split(' ')[1:])
                    if not self._check_dir(dirname):
                        continue
                    dirname = f"{self._compile_res}/" + dirname
                    create_dir(dirname)

                    for part in mail.walk():
                        filename = part.get_filename()
                        if filename:
                            with open(f"{dirname}/{filename}", 'wb') as new_file:
                                new_file.write(part.get_payload(decode=True))
        except self._client.abort as err:
            print(err)
            return
        except AssertionError as err:
            print(err)
            return

    def _compile(self):
        create_dir(self._compile_res)
        goto(self._compile_res)
        self._compiler.compile_all()
        back()

    def close(self):
        if self._client is not None:
            self._client.logout()

    def _help(self):
        print(f'''****************
        You can use following methods:
        get all: get all files in mails, which consist 'group' in theme
        compile: compile all files in {self._compile_res}
        exit: exit client
****************''')
