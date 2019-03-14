from app.Compile_log import Log


class Stats(object):
    def __init__(self):
        self._logs = {}

    def add(self, group: str, human: str, theme: str, compile_log: Log):
        if group not in self._logs.keys():
            self._logs[group] = {human: {theme: {compile_log}}}
        else:
            if human not in self._logs[group].keys():
                self._logs[group][human] = {theme: {compile_log}}
            else:
                if theme not in self._logs[human]:
                    self._logs[group][human][theme] = {compile_log}
                else:
                    self._logs[group][human][theme].add(compile_log)

        print(f"g: {group}, h: {human}, t: {theme}")

    def get_total_num(self, only_ok=False):
        total_num = 0
        for group in self._logs.keys():
            for human in self._logs[group].keys():
                for theme in self._logs[group][human].keys():
                    if only_ok:
                        total_num += sum(map(lambda log: log.is_success(), self._logs[group][human][theme]))
                    else:
                        total_num += len(self._logs[group][human][theme])
        return total_num

    def get_table(self):
        def get_cell(text: str, cell_len: int):
            # print(f"Text: {text}")
            cell = ""
            for i, c in enumerate(text):
                cell += c
                if (i + 1) % cell_len == 0:
                    cell += '\n'
            # print(cell)
            return cell

        def concatect_cells(cells, cell_len, log_len):
            lines = [cell.split('\n') for cell in cells]
            print(f"Lines\n{lines}")
            max_lines = max(len(cell) for cell in lines)
            print(max_lines)

            line = (3 * (cell_len+1) + (log_len+1) + 1) * '-' + '\n'
            emply_line = cell_len * ' '
            cell_row = ""

            for i in range(max_lines):
                cell_row += '|'
                for j, cell in enumerate(lines):
                    if len(cell) <= i:
                        cell_row += emply_line
                    else:
                        cell_row += cell[i] + ' ' * \
                                    ((log_len if j == len(lines)-1 else cell_len) - len(cell[i]))
                    cell_row += '|'
                cell_row += '\n'

            return cell_row

        cell_len = 10
        log_len = 30
        one_line = (3 * (cell_len+1) + (log_len+1) + 1)*'-' + '\n'
        table = one_line

        for group in self._logs.keys():
            group_cell = get_cell(group, cell_len)
            for human in self._logs[group].keys():
                human_cell = get_cell(human, cell_len)
                for theme in self._logs[group][human].keys():
                    theme_cell = get_cell(theme, cell_len)
                    for log in self._logs[group][human][theme]:
                        log_cell = get_cell(str(log), log_len)
                        table += concatect_cells([group_cell, human_cell, theme_cell, log_cell], cell_len, log_len) + one_line
        return table

    def __str__(self):
        return f'''There are {self.get_total_num()} compilations.
{self.get_table()}'''
