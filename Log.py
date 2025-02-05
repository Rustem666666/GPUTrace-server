import os
from datetime import datetime

logFile = 'data/log.txt'
dir = 'data/'

def AddToLog(text):
    
    with open(logFile, "a") as file:
        file.write(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}: {text}\n')
        print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}: {text}')
 
def AddToChatLog(chatid , text):
    CheckSize(dir + str(chatid) + '.txt')
    with open(dir + str(chatid) + '.txt', "a") as file:
        file.write(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}: {text}\n')
        print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}: {text}')

def CheckSize(file):
    try:
        if os.path.exists(file):
            file_info = os.stat(file)
            if (file_info.st_size > 5000000): #удаляем файл если он больше 5 мб
                os.remove(file)
                AddToLog(f'{file} превысил допустимый размер. Удаление.')
    except :
        AddToLog(f'Ошибка при попытке удаления файла {file}')
