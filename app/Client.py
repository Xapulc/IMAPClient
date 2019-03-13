from imaplib import IMAP4, IMAP4_SSL
from socket import gaierror
from email import message_from_bytes

from app.Authentication import Authentication
from app.Compiler import Compiler
from app.Stats import Stats
from app.file_worker import create_dir, goto, back


class Client(object):

    def __init__(self):
        """
        Create an instance client and connect to host if use old data is true
        """
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
        """
        Connect to host
        """
        self._host = hostname
        while self._host is None:
            self._host = input("Enter host name: ")
            try:
                self._client = IMAP4_SSL(host=self._host, port=self._port)
            except gaierror as err:  # Unavailable host
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
        """
        Login into host
        """
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
        """
        Send request to host
        """
        while True:
            req_str = input("Enter your request: ")
            req: list = req_str.split()
            if len(req) >= 2 and req[0] == "get" and req[1] == "all":
                if len(req) >= 3 and req[2] == "unseen":
                    self._load_attachments(unseen=True)
                else:
                    self._load_attachments(unseen=False)
                return True
            elif len(req) >= 1 and req[0] == "compile":
                self._compile()
                return True
            elif len(req) >= 1 and req[0] == "exit":
                return False
            else:
                self._help()

    def _check_dir(self, dirname: str):
        """
        Checking correctness theme of mail
        """
        dir_list = dirname.split('/')
        if len(dir_list) != 3:
            return False

        group, theme, person = dir_list
        if not group.isdigit():
            return False

        return True

    def _load_attachments(self, unseen: bool, with_stats: bool = False):
        """
        Load attachments from mails in mailbox in directories
        :param unseen: if True, load attachments from unseen mails,
        else load attachments from all files (which satisfy _check_dir)
        """
        if with_stats:
            stats = Stats()
        try:
            box = "INBOX"
            status, msgs = self._client.select(box, True)
            assert status == "OK", f"Can't select {box}"

            key_word = "group"
            if unseen:
                status, num_messages = self._client.search("utf-8", "INBOX", "(UNSEEN)", "SUBJECT", key_word)
            else:
                status, num_messages = self._client.search("utf-8", "SUBJECT", key_word)
            assert status == "OK", f"Can't search {key_word}"

            for num in num_messages[0].split():
                status, message = self._client.fetch(num, "(RFC822)")
                if status != "OK":
                    continue

                self._client.store(num, "+FLAGS", "\Seen")
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

                    if with_stats:
                        logs = self._compiler.compile_direct(dirname)
                        for log in logs:
                            log_name = log.get_name()
                            grp_ind = log_name.find(f"{self._compile_res}/") + len(f"{self._compile_res}/") + 1
                            hum_ind = log_name[grp_ind:].find('/') + 1
                            theme_ind = log_name[hum_ind:].find('/') + 1
                            files_ind = log_name[theme_ind:].find('/') + 1

                            group = log_name[grp_ind, hum_ind-1]
                            human = log_name[hum_ind, theme_ind-1]
                            theme = log_name[theme_ind, files_ind-1]
                            stats.add(group, human, theme, log)

            if with_stats:
                with open("log_table.txt") as log_file:
                    log_file.write(stats.get_table())
        except self._client.abort as err:
            print(err)
            return
        except AssertionError as err:
            print(err)
            return

    def _compile(self, files=None):
        """
        Compile files
        """
        create_dir(self._compile_res)
        goto(self._compile_res)
        self._compiler.compile_all('.', files)
        back()

    def close(self):
        """
        Close connection
        """
        if self._client is not None:
            self._client.logout()

    def _help(self):
        print(f'''****************
        You can use following methods:
        get all: get all files in mails, which consist 'group' in theme
        get all unseen: same 'get all', but get only unseen emails
        compile: compile all files in {self._compile_res}
        exit: exit client
****************''')
