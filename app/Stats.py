from app.Compile_log import Log


class Stats(object):
    def __init__(self):
        self._files = {}

    def __add__(self, human: str, subject: str, compile_log: Log):
        
