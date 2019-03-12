from app.Compile_log import Log


class Stats(object):
    def __init__(self):
        self._logs = {}

    def __add__(self, human: str, theme: str, compile_log: Log):
        if human not in self._logs.keys():
            self._logs[human] = {theme: {compile_log}}
        else:
            if theme not in self._logs[human]:
                self._logs[human][theme] = {compile_log}
            else:
                self._logs[human][theme].add(compile_log)

    def get_total_num(self, only_ok=False):
        total_num = 0
        for human in self._logs.keys():
            for theme in self._logs[human].keys():
                if only_ok:
                    total_num += sum(map(lambda log: log.is_success(), self._logs[human][theme]))
                else:
                    total_num += len(self._logs[human][theme])
        return total_num

    def get_table(self):
        def get_cell(text: str, cell_len: int):
            cell = ""
            for i, c in enumerate(text):
                cell += c
                if (i + 1) % cell_len == 0:
                    cell_len += '\n'
            return cell

        def concatect_cells(cells):


        cell_len = 20
        one_line = cell_len*'-' + '\n'
        table = one_line

        for human in self._logs.keys():
            human_cell = get_cell(human, cell_len)
            for theme in self._logs[human].keys():
                theme_cell = get_cell(theme, cell_len)
                for log in self._logs[human][theme]:
                    log_cell = get_cell(log, cell_len)
                    table += concatect_cells([human_cell, theme_cell, log_cell]) + one_line
        return table

    def __str__(self):
        return f'''There are {self.get_total_num()} compilations.
{self.get_table()}'''
