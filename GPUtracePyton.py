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
   Parameters.ReadParamList()
   UserData.CheckUserDataSize() #проверка на размер файлов
   Log.AddToLog(f'Запуск прошёл без ошибок.')
except :
   Log.AddToLog("Ошибка при запуске.")


while True:
    # код проверки сюда
    
    UserData.GetUserData() # Данные пользователей
    TelegramBot.Check() # Проверка для бота

    if (((datetime.now() - checkHalfHourDate).seconds//60)%60 >= 30): # Получасовая проверка.
        checkHalfHourDate = datetime.now() #время Получасовой проверки
        Log.AddToLog("Прошло 30 минут.")
        Parameters.BackupParamList()
        UserData.CheckUserDataSize() #проверка на размер файлов
    
    if ((datetime.now() - checkMinuteDate).seconds > 60): # Минутная проверка.
        checkMinuteDate = datetime.now() #время минутной проверки
        Log.AddToLog("Прошла минута.")
        UserData.CheckUserDataSize()
        Parameters.SaveParamList()

    #print(f'{initDate.strftime("%d.%m.%Y %H:%M:%S")} GPU - {Parameters.Params[Parameters.GetParamIndex("557827405")].gputemp} Memory - {Parameters.Params[Parameters.GetParamIndex("557827405")].memtemp}')
    
    
    
    
    
    time.sleep(1) # уснуть на пол секунды


