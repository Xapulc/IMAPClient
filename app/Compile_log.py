class Log(object):
    def __init__(self, obj: str = None, log: str = None, success: bool = None):
        self._object = obj
        self._log = log
        self._success = success

    def update(self, log, success):
        self._log = log
        self._success = success

    def is_success(self):
        return self._success

    def __str__(self):
        return f'''Object:
{self._object}
Status: {"OK" if self._success else "BAD"}
Log:
{self._log}'''
