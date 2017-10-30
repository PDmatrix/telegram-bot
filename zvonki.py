from datetime import datetime, timedelta
#Расписание звонков
zvonki = [['8:15', '9:55'], ['10:25', '11:55'], ['12:05', '13:35'], ['14:00', '15:35'], ['15:45', '17:20'], ['17:30', '19:05']]
#Текущее время
current_time = datetime.now()
#current_time  = datetime.strptime("12:30", "%H:%M")

#Возвращает номер текущей пары, если ее нет то 0.
def get_para_num():
    para_num = 0
    for idx, para in enumerate(zvonki):
        para_st = datetime.strptime(para[0], "%H:%M")
        para_end = datetime.strptime(para[1], "%H:%M")
        if para_st < current_time and current_time < para_end:
            #print('Сейчас идет {} пара'.format(idx+1))
            para_num = idx+1
    return para_num
#Принимает номер пары, возвращает оставшиеся до конца время
def when_para_ends(para_num):
    para_end = datetime.strptime(zvonki[para_num-1][1], "%H:%M")
    remaining = para_end - current_time
    return remaining
#print('Время: {}'.format(datetime.strftime(current_time, "%H:%M")))
#print('Осталось {} пары'.format(get_para_num()))
#print('До конца пары {} ч.'.format(when_para_ends(get_para_num())))
