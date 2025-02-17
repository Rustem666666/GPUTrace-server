import os
import Parameters
import Log
from datetime import datetime

dir = 'data/users/'

def GetUserData():
    try:
        files = os.listdir(dir)
        for item in files:
            token = item.replace('.txt','')
            with open(dir + token + ".txt", "r") as f:
                line = f.readlines()[-1]
                sep = ';'
                result = [x for x in line.split(sep)]

                if (Parameters.ParamExist(token)):
                    ind = Parameters.GetParamIndex(token)
                    readDate = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S') #2022-05-24 15:16:34
                    if Parameters.Params[ind].checkDate != readDate:
                        Parameters.Params[ind].checkDate = readDate
                        Parameters.Params[ind].gputemp = float(result[1])
                        if (len(result[2]) > 1): Parameters.Params[ind].gpulim = float(result[2])
                        Parameters.Params[ind].memtemp = float(result[3])
                        if (len(result[4]) > 1): 
                            Parameters.Params[ind].memlim = float(result[4])
                            Parameters.SaveParamList()
    except Exception as e:
        Log.AddToLog(f'Ошибка при попытке чтения данных пользователя. {e}')
    

def CheckUserDataSize():
    files = os.listdir(dir)
    for item in files:
        try:
            file_info = os.stat(dir + item)
            if (file_info.st_size > 5000000): #удаляем файл если он больше 5 мб
                os.remove(dir + item)
                Log.AddToLog(f'{item} превысил допустимый размер. Удаление.')
        except :
            Log.AddToLog(f'Ошибка при попытке удаления файла {item}')
