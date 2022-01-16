import datetime


class Log:
    def __init__(self, _name: str):
        self.name = _name
        try:
            self.file = open(_name, "a")
        except FileNotFoundError:
            self.file = open(_name, "w")
        self.save_data("Log started at " + str(datetime.datetime.now()))
        self.file.close()

    # Сохраняет информацию в файл
    def save_data(self, _data: str):
        self.file = open(self.name, "a")
        self.file.write("{}\n".format(_data))
        self.file.close()

    # Возвращает данные из файла в виде листа
    @staticmethod
    def read_and_return_list(_name: str):
        try:
            file = open(_name, "r")
        except FileNotFoundError:
            return []
        data = file.read()
        return data.split("\n")

    # Останавливает лог
    def kill_log(self):
        self.file = open(self.name, "a")
        self.save_data("Log stopped at {}\n".format(datetime.datetime.now()))
        self.file.close()
