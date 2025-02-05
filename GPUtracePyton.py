import os
import Parameters
import UserData
import time
import Log
import TelegramBot
from datetime import datetime

initDate = datetime.now() #время запуска программы
checkMinuteDate = datetime.now() #время минутной проверки
checkHalfHourDate = datetime.now() #время Получасовой проверки


try:
   if Parameters.ReadParamList() == False:
        Log.AddToLog(f'Попытка восстановить из резерва.')
        Parameters.RecoverParam()
   for chat in Parameters.Params:
        if (((datetime.now() - chat.checkDate).total_seconds()//60)%60 >= 5): # Если разница 5 минут и больше.
            chat.warning = True
        print(chat)
   UserData.CheckUserDataSize() #проверка на размер файлов
   TelegramBot.Init()
   Log.AddToLog(f'Запуск прошёл без ошибок.')
except Exception as e:
   Log.AddToLog(f'Ошибка при запуске. {e}')


while True:
    # код проверки сюда
    #Log.AddToLog((datetime.now() - initDate).total_seconds())
    UserData.GetUserData() # Данные пользователей
    TelegramBot.Check() # Проверка для бота

    if (((datetime.now() - checkHalfHourDate).total_seconds()//60)%60 >= 30): # Получасовая проверка.
        checkHalfHourDate = datetime.now() #время Получасовой проверки
        #Log.AddToLog("Резервирование параметров.")
        Parameters.BackupParamList()
        Log.CheckSize(Log.logFile) #проверка размера файла лога
        UserData.CheckUserDataSize() #проверка на размер файлов
    
    if ((datetime.now() - checkMinuteDate).total_seconds() > 60): # Минутная проверка.
        checkMinuteDate = datetime.now() #время минутной проверки
        Parameters.SaveParamList()
        

    #print(f'{initDate.strftime("%d.%m.%Y %H:%M:%S")} GPU - {Parameters.Params[Parameters.GetParamIndex("557827405")].gputemp} Memory - {Parameters.Params[Parameters.GetParamIndex("557827405")].memtemp}')
    
    
    
    
    
    time.sleep(1) # уснуть на пол секунды


