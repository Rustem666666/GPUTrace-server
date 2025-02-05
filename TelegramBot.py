import Parameters
import Log
from datetime import datetime
import threading
import time
import telebot
from telebot import types
import random
import re

checkSecondDate = datetime.now() #время минутной проверки бота
bot = telebot.TeleBot('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') #Здесь токен для бота

def Init():
    global threadStop
    threadStop = False
    botThread = threading.Thread(target=thread_function, args=(1,))
    botThread.start()


def thread_function(name):
    while True:
        if threadStop:
            Log.AddToLog("Бот остановлен")
            break
        try:
            bot.polling(none_stop=True)
            # Запуск бота
        except Exception as e:
            Log.AddToLog(f'Ошибка {e}')
            time.sleep(5)


def Send(chatid, text):
    """Отправляет сообщение в указанный чат"""
    try:
    	bot.send_message(chatid, text, parse_mode='MarkdownV2')
    except Exception as e:
        Log.AddToLog(f'Ошибка при отправке сообщения в телеграм. {e}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    ChatId = str(message.chat.id)
    Log.AddToChatLog(message.chat.id,f'{message.from_user.username}: {message.text}')
    #Проврка наличия пользователя в файле параметров
    if (Parameters.ParamExist(ChatId)):
        index = Parameters.GetParamIndex(ChatId)
    else:
        par = Parameters.Param(ChatId, datetime.now(), 'нет токена', False, 0, 0, False, 0, 0, False)
        Parameters.Params.append(par)
        index = Parameters.GetParamIndex(ChatId)
    #Отслеживание сообщений
    if message.text == "Получить токен":
        if (Parameters.Params[index].token == "нет токена"):
            Parameters.Params[index].token = GenerateToken(20)
            Send(message.chat.id, f'Твой токен *{Parameters.Params[index].token}*, введи его в программе, чтобы получать уведомления\\.')
        else:
            Send(message.chat.id, f'У тебя уже есть токен *{Parameters.Params[index].token}*, введи его в программе, чтобы получать уведомления\\.')

    if re.fullmatch(r'Лимит GPU [-0-9]{1,3}', message.text):
        result = re.search(r'[-0-9]{1,3}', message.text)
        result = float(result[0])
        if result > 0 and result < 110:
            Parameters.Params[index].gpulim = result
            Send(message.chat.id, f"Установлен лимит температуры GPU\\:\n*{TextConverter(abrakadabra(Parameters.Params[index].gpulim, 'градус', 'градуса', 'градусов'))}*")
        else:
            if result < 0:
                Send(message.chat.id, f'Температура GPU *не может быть меньше* 0 градусов\\.')
            if result > 110:
                Send(message.chat.id, f'Устанавливайте предупреждение *меньше* максимальной температуры GPU, иначе это не имеет смысла\\.')

    if re.fullmatch(r'Лимит памяти [-0-9]{1,3}', message.text):
        result = re.search(r'[-0-9]{1,3}', message.text)
        result = float(result[0])
        if result > 0 and result < 110:
            Parameters.Params[index].memlim = result
            Send(message.chat.id, f"Установлен лимит температуры памяти\\:\n*{TextConverter(abrakadabra(Parameters.Params[index].memlim, 'градус', 'градуса', 'градусов'))}*")
        else:
            if result < 0:
                Send(message.chat.id, f'Температура памяти *не может быть меньше* 0 градусов\\.')
            if result > 110:
                Send(message.chat.id, f'Устанавливайте предупреждение *меньше* максимальной температуры памяти, иначе это не имеет смысла\\.')

    if re.fullmatch(r'(Не )?[Оо]тслеживай (GPU|память)', message.text):
        searchString = re.search(r'(Не отслеживай|[Оо]тслеживай)', message.text)
        searchCommand = str(searchString[0])
        searchString = re.search(r'(GPU|память)', message.text)
        searchDevice = str(searchString[0])
        #Log.AddToChatLog(message.chat.id,f'{message.from_user.username}: {searchString}')
        if (Parameters.Params[index].token != "нет токена"):
            if searchDevice == "GPU":
                if searchCommand == "Отслеживай":
                    if Parameters.Params[index].tracegpu:
                        Send(message.chat.id, f'*Уже отслеживаем*\\. Если хотите выключить, напишите _Не отслеживай_\\.')
                    else:
                        Parameters.Params[index].tracegpu = True
                        Send(message.chat.id, f'*Включено* отслеживание температуры GPU\\.')
                if searchCommand == "Не отслеживай":
                    if Parameters.Params[index].tracegpu:
                        Parameters.Params[index].tracegpu = False
                        Send(message.chat.id, f'*Выключено* отслеживание температуры GPU\\.')
                    else:
                        Send(message.chat.id, f'*Уже не отслеживаем*\\. Если хотите включить, напишите _Отслеживай_\\.')
            if searchDevice == "память":
                if searchCommand == "Отслеживай":
                    if Parameters.Params[index].tracemem:
                        Send(message.chat.id, f'*Уже отслеживаем*\\. Если хотите выключить, напишите _Не отслеживай_\\.')
                    else:
                        Parameters.Params[index].tracemem = True
                        Send(message.chat.id, f'*Включено* отслеживание температуры памяти.')
                if searchCommand == "Не отслеживай":
                    if Parameters.Params[index].tracemem:
                        Parameters.Params[index].tracemem = False
                        Send(message.chat.id, f'*Выключено* отслеживание температуры памяти.')
                    else:
                        Send(message.chat.id, f'*Уже не отслеживаем*\\. Если хотите включить, напишите _Отслеживай_\\.')
        else:
            Send(message.chat.id, f'Необходимо сначала *получить токен* для отслеживания температур\\.')

    if message.text == "Температуры":
        if (Parameters.Params[index].token != "нет токена"):
            if Parameters.Params[index].warning:
                Send(message.chat.id, f'Потеряна связь\\. Последняя отметка *{TextConverter(Parameters.Params[index].checkDate.strftime("%d.%m.%Y %H:%M:%S"))}*')
            else:
                row_one = f"Температура GPU\\:\n *{TextConverter(abrakadabra(Parameters.Params[index].gputemp, 'градус', 'градуса', 'градусов'))}*"
                row_two = f"Температура памяти\\:\n *{TextConverter(abrakadabra(Parameters.Params[index].memtemp, 'градус', 'градуса', 'градусов'))}*"
                Send(message.chat.id, f'{row_one}\n{row_two}')
        else:
            Send(message.chat.id, f'Необходимо сначала *получить токен* для отслеживания температур\\.')

    if message.text == "Лимиты":
        if (Parameters.Params[index].token != "нет токена"):
            row_one = f"Текущий лимит GPU\\:\n *{TextConverter(abrakadabra(Parameters.Params[index].gpulim, 'градус', 'градуса', 'градусов'))}*"
            row_two = f"Текущий лимит памяти\\:\n *{TextConverter(abrakadabra(Parameters.Params[index].memlim, 'градус', 'градуса', 'градусов'))}*"
            Send(message.chat.id, f'{row_one}\n{row_two}')
        else:
            Send(message.chat.id, f'Необходимо сначала *получить токен* для отслеживания температур\\.')

    if message.text == "Помоги":
        if (Parameters.Params[index].token != "нет токена"):
            if Parameters.Params[index].tracegpu: 
                str_one = "Не отслеживай GPU" 
            else: 
                str_one = "Отслеживай GPU"
            if Parameters.Params[index].tracemem: 
                str_two = "Не отслеживай память" 
            else: 
                str_two = "Отслеживай память"
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Температуры", "Лимиты"]
            keyboard.add(*buttons)
            buttons = [str_one, str_two]
            keyboard.add(*buttons)
            buttons = ["Лимит GPU 65", "Лимит памяти 85"]
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, "Что я могу?", disable_notification=True, reply_markup=keyboard)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Получить токен"]
            keyboard.add(*buttons)
            bot.send_message(message.chat.id, "Что я могу?", disable_notification=True, reply_markup=keyboard)

def TextConverter(text):
    #In all other places characters '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'
    st = str(text)
    st = st.replace('_', '\\_')
    st = st.replace('*', '\\*')
    st = st.replace('[', '\\[')
    st = st.replace(']', '\\]')
    st = st.replace("(", "\\(")
    st = st.replace(")", "\\)")
    st = st.replace("~", "\\~")
    st = st.replace("`", "\\`")
    st = st.replace(">", "\\>")
    st = st.replace("#", "\\#")
    st = st.replace("+", "\\+")
    st = st.replace("-", "\\-")
    st = st.replace("=", "\\=")
    st = st.replace("|", "\\|")
    st = st.replace("{", "\\{")
    st = st.replace("}", "\\}")
    st = st.replace('.', '\\.')
    st = st.replace("!", "\\!")
    return st;

def GenerateToken(length):
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password

def Ff(num):
    """Форматирование плавающего числа"""
    return '{0:.2f}'.format(num).rstrip('0').rstrip('.')

def abrakadabra(
    number,
    nominative_singular,
    genetive_singular,
    nominative_plural
):
    """Склонятор слов в зависимости от числа abrakadabra(22, 'собака', 'собаки', 'собак')"""
    number = float(number)
    return Ff(number) + ' ' + (
        (number in range(5, 20)) and nominative_plural or
        (1 in (number, (diglast := number % 10))) and nominative_singular or
        ({number, diglast} & {2, 3, 4}) and genetive_singular or nominative_plural
    )

def Check():
    """Срабатывает раз в секунду из основной программы"""
    global checkSecondDate
    if ((datetime.now() - checkSecondDate).seconds > 60): # Минутная проверка.
        checkSecondDate = datetime.now() #время Минутная проверки
        for chat in Parameters.Params:
            firstrow = ''
            secondrow = ''
            if (chat.token != "нет токена"):
                if chat.warning:
                    if (((datetime.now() - chat.checkDate).total_seconds()//60) < 5): # Если разница меньше 5 минут.
                        chat.warning = False
                        Send(chat.chatId, f'Связь восстановлена\\. Последняя отметка *{TextConverter(chat.checkDate.strftime("%d.%m.%Y %H:%M:%S"))}*')
                        Log.AddToLog(f'Связь восстановлена. Последняя отметка {chat.checkDate.strftime("%d.%m.%Y %H:%M:%S")} usertoken = {chat.token} текущая дата {datetime.now().strftime("%d.%m.%Y %H:%M:%S")} разница {str(((datetime.now() - chat.checkDate).total_seconds()//60))}')
                else:
                    if chat.tracegpu:
                        if chat.gputemp >= chat.gpulim:
                            Log.AddToLog(f"Температура GPU превысила лимит:\nЛимит {Ff(chat.gpulim)}, значение {Ff(chat.gputemp)}, usertoken {chat.token}")
                            firstrow = f"Температура GPU превысила лимит\\:\n*{TextConverter(abrakadabra(chat.gputemp, 'градус', 'градуса', 'градусов'))}*"
                    if chat.tracemem:
                        if chat.memtemp >= chat.memlim:
                            Log.AddToLog(f"Температура памяти превысила лимит:\nЛимит {Ff(chat.memlim)}, значение {Ff(chat.memtemp)}, usertoken {chat.token}")
                            secondrow = f"Температура памяти превысила лимит\\:\n*{TextConverter(abrakadabra(chat.memtemp, 'градус', 'градуса', 'градусов'))}*"
                    if (len(firstrow) > 0 or len(secondrow) > 0):
                            Send(chat.chatId, f'{firstrow}\n{secondrow}')
                    if (((datetime.now() - chat.checkDate).total_seconds()//60) >= 5): # Если разница 5 минут и больше.
                        chat.warning = True
                        Send(chat.chatId, f'Потеряна связь\\. Последняя отметка *{TextConverter(chat.checkDate.strftime("%d.%m.%Y %H:%M:%S"))}*')
                        Log.AddToLog(f'Потеряна связь. Последняя отметка {chat.checkDate.strftime("%d.%m.%Y %H:%M:%S")} usertoken = {chat.token} текущая дата {datetime.now().strftime("%d.%m.%Y %H:%M:%S")} разница {str(((datetime.now() - chat.checkDate).total_seconds()//60))}')
