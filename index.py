import vk_api
from datetime import datetime
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token="Ваш токен")
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, "id группы, к которой привязан бот")
string = ""
result = ""
date_count = 0  
path_homework_base = "путь до файла, в котором будет храниться домашка/homework.txt" #Пример для Windows: C:\\users\\Desktop\\vk-bot-for-homework\\homework.txt ; Linux: /home/user/Documents/vk-bot-for-homework/homework.txt
path_admin_base = "путь до файла, в котором будут хранится админы/admins.txt" #Пример для Windows: C:\\users\\Desktop\\vk-bot-for-homework\\admins.txt ; Linux: /home/user/Documents/vk-bot-for-homework/homework.txt

for event in longpoll.listen(): 
    file = open(path_homework_base, "r")
    output = open(path_homework_base, "a")

    if event.type == VkBotEventType.MESSAGE_NEW:
        admins = open(path_admin_base).read().split('\n')
        if event.from_chat:
            comannd_user = event.obj.text.split(";")
            comand = comannd_user[0].split(" ")
            if len(comand) > 1:
                comannd_user[0] = comand[1]
            if comand[0] == "/add" and str(event.raw['object']['from_id']) in admins:
                if len(comannd_user) > 2:
                    check_zero_data = comand[1].split(".")
                    if (len(check_zero_data) == 3) and (check_zero_data[0] != "00") and (check_zero_data[1] != "00") and (check_zero_data[2] != "00") and (len(check_zero_data[0]) == 2) and (len(check_zero_data[1]) == 2) and (len(check_zero_data[2]) == 2):
                        for index in range(len(comannd_user)):
                            result += comannd_user[index] + "; "
                        result = result[:-2]
                        output.write(result)
                        output.write("\n")
                        result = ""
                        vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Добавил, можешь проверить командой: /list")
                        
                        output.close()
                        output = open(path_homework_base, "a")

                        unix_date = datetime(1970, 1, 1)
                        date_now = datetime.today()
                        date_now = datetime(date_now.year, date_now.month, date_now.day)
                        date_now = (date_now - unix_date).total_seconds()
                        
                        matrix = []
                        time_in_seconds = []
                        with open(path_homework_base) as inf:
                            for index in inf:
                                matrix.append(index.split(";"))

                        for index in range(len(matrix)):
                            string = matrix[index][0].split(".")
                            if len(string[2]) == 2:
                                string[2] += "20"
                            elif len(string[2]) == 4:
                                pass
                            time_dz = datetime(int(string[2]), int(string[1]), int(string[0]))
                            time_dz = (time_dz - unix_date).total_seconds()
                            if time_dz not in time_in_seconds:
                                time_in_seconds.append(time_dz)
                            time_in_seconds.sort()

                        for index in range(len(time_in_seconds)):
                            for jendex in range(len(matrix)):
                                string = matrix[jendex][0].split(".")
                                if len(string[2]) == 2:
                                    string[2] += "20"
                                elif len(string[2]) == 4:
                                    pass
                                time_dz = datetime(int(string[2]), int(string[1]), int(string[0]))
                                time_dz = (time_dz - unix_date).total_seconds()
                                if time_dz == time_in_seconds[len(time_in_seconds)-index-1]:
                                    for kendex in range(len(matrix[jendex])):
                                        matrix[jendex][kendex] = matrix[jendex][kendex].strip()
                                        result += matrix[jendex][kendex] + "; "
                                    result = result[:-2] + '\n'

                        output.close()
                        output = open(path_homework_base, "w")
                        output.close()
                        output = open(path_homework_base, "a")
                        output.write(result)
                        date_count = date_now
                        matrix = []
                        result = ""
                        string = ""
                    else:
                        vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Неверно введенные данные, проверьте все пункты:\n1) Формат данных такой: дата;предмет;домашняя работа \n2) Формат даты такой: 01.10.10 или 01.10.2010")
                else:
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Неверно введенные данные, проверьте все пункты:\n1) Формат данных такой: дата;предмет;домашняя работа \n2) Формат даты такой: 01.10.10 или 01.10.2010")

            if event.obj.text == "/list":
                with open(path_homework_base) as inf:
                    for index in inf:
                        string += index.strip() + "\n" + "\n"
                if string != "":# or string != " " or string != "\n\n" or string != "\n" or string != "  ":
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message=string)
                else: 
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Список пустой")
                string = ""

            if event.obj.text == "/help":
                vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Вот список команд:\n/add 'дата;предмет;дз' - добавить домашку\n/del 'предмет' - удаляет все домашки по данному предмету \n/del 'дата;предмет' - удаляет домашку по предмету и по дате \n/list - список домашки")
            
            #if event.obj.text == "/doc":
            #    vk.messages.send(chat_id = event.chat_id, random_id = get_random_id(), message = "Ссылка на таблицу с домашкой:\n")
            
            if comand[0] == "/del" and str(event.raw['object']['from_id']) in admins:
                if len(event.obj.text.split(" ")) > 1:
                    file.close()
                    output.close() 
                    for index in range(len(comannd_user)):
                        result += comannd_user[index] + "; "
                    with open(path_homework_base,"r+") as file2:
                        new_f = file2.readlines()
                        file2.seek(0)
                        for line in new_f:
                            if result not in line:
                                file2.write(line)
                        file2.truncate()
                        file2.close()
                    result = ""
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Удалил, можешь проверить командой: /list")
                else:
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Неверно введена операция, синтаксис такой:\n/del 'предмет' - удаляет все домашки по данному предмету\n/del 'дата;предмет' - удаляет домашку по предмету и по дате\n/del 'дата' - удаляет всю домашку по этой дате")
            
            if comand[0] == "/admin" and str(event.raw['object']['from_id']) in admins:
                admins_file = open(path_admin_base, "a")
                admins_file.write(comannd_user[0])
                admins_file.write("\n")
                vk.messages.send(chat_id = event.chat_id, random_id = get_random_id(), message = "Администратор " + str(comannd_user[0]) + " добавлен.")
                admins_file.close()

            if comand[0] == "/alist" and str(event.raw['object']['from_id']) in admins:
                with open(path_admin_base) as inf:
                    for index in inf:
                        string += "https://vk.com/id" + index.strip() + "\n"
                if string != "":
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message= "Вот список всех администраторов:\n" + string)
                else: 
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Список пустой")
                string = ""
   
            
            if comand[0] == "/adel" and str(event.raw['object']['from_id']) in admins:
                if len(comannd_user) > 2:
                    file.close()
                    output.close()
                    for index in range(len(comannd_user)):
                        result += comannd_user[index] + "; "
                    result = result[:-2]
                    with open(path_admin_base,"r+") as file2:
                        new_f = file2.readlines()
                        file2.seek(0)
                        for line in new_f:
                            if result not in line:
                                file2.write(line)
                        file2.truncate()
                        file2.close()
                    result = ""
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Удалил, можешь проверить командой \n /alist")
                else:
                    vk.messages.send(chat_id = event.chat_id, random_id=get_random_id(), message="Неверно введена операция, синтаксис такой:\n/adel id - пользователя")

    file.close()
    output.close()
