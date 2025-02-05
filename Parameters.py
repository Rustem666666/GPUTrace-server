import Log
import shutil
from datetime import datetime

paramFile = 'data/Parameters.ini'
paramFileBackup = 'data/backup/Parameters_backup.ini'
Params = list();

class Param:
    """Добавление параметра для чатов"""
    """557827405;24.05.2022 16:07:27;abcd;True;50;67;True;70;110"""
 
    def __init__(self, chatId, checkDate, token, tracegpu, gpulim, gputemp, tracemem, memlim, memtemp):
        """Constructor"""
        self.chatId = chatId #ID чата в который отправляется информация
        self.checkDate = checkDate #Дата последней отметки клиента
        self.token = token #Токен клиента
        self.tracegpu = tracegpu #Переключение отслеживания температуры GPU
        self.gpulim = gpulim #Лимит температуры gpu для уведомления
        self.gputemp = gputemp #Текущая температура Gpu
        self.tracemem = tracemem # Переключение отслеживания температуры памяти
        self.memtemp = memtemp # Текущая температура памяти
        self.memlim = memlim # Лимит температуры памяти для уведомления
    def __repr__(self):
        return '\n<Параметр (chatId={}, checkDate={}, token={}, gpuTemp={}, memTemp={})>'.format( self.chatId, self.checkDate.strftime("%B %d, %Y"), self.token, self.gputemp, self.memtemp)


def ReadParamList():
    sep = ';'
    try:
        with open(paramFile, "r") as f:
            while True:
                # считываем строку
                line = f.readline()
                # прерываем цикл, если строка пустая
                if not line:
                    break
                result = [x for x in line.split(sep)]
                par = Param(result[0], datetime.strptime(result[1], '%d.%m.%Y %H:%M:%S'), result[2], bool(result[3]), float(result[4]), float(result[5]), bool(result[6]), float(result[7]), float(result[8]))
                Params.append(par)
    except :
        Log.AddToLog(f'Ошибка при чтении файла {paramFile}')
    
def CheckParamList():
    sep = ';'
    try:
        with open(paramFile, "r") as f:
            while True:
                # считываем строку
                line = f.readline()
                # прерываем цикл, если строка пустая
                if not line:
                    break
                result = [x for x in line.split(sep)]
                par = Param(result[0], datetime.strptime(result[1], '%d.%m.%Y %H:%M:%S'), result[2], bool(result[3]), float(result[4]), float(result[5]), bool(result[6]), float(result[7]), float(result[8]))
                return True
    except :
        return False
        Log.AddToLog(f'Проверка файла {paramFile}. Результат отрицательный.')

def SaveParamList():
    with open(paramFile, "w") as file:
        for param in Params:
           file.write(f'{param.chatId};{param.checkDate.strftime("%d.%m.%Y %H:%M:%S")};{param.token};{param.tracegpu};{param.gpulim};{param.gputemp};{param.tracemem};{param.memlim};{param.memtemp}\n')
 
def BackupParamList():
    if (CheckParamList()):
        try:
            shutil.copyfile(paramFile, paramFileBackup)
        except :
            Log.AddToLog(f'Ошибка при резервировании файла {paramFile}.')
        Log.AddToLog(f'Создаём резервную копию файла {paramFile}.')

def ParamExist(chatidOrtoken):
    """Возвращает true если существует элемент с chatid или token"""
    for item in Params:
        if item.chatId == chatidOrtoken:
            return True
        if item.token == chatidOrtoken:
            return True
    return False

def GetParamIndex(chatidOrtoken):
    """Возвращает индекс если существует элемент с chatid"""
    for item in Params:
        if item.chatId == chatidOrtoken:
            return Params.index(item)
        if item.token == chatidOrtoken:
            return Params.index(item)
