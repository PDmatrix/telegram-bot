from datetime import datetime, timedelta
#Расписание звонков
zvonki = [['8:15', '9:55'], ['10:25', '11:55'], ['12:05', '13:35'], ['14:00', '15:35'], ['15:45', '17:20'], ['17:30', '19:05']]
zvonki_vtornik = [['8:15', '9:55'], ['10:25', '11:55'], ['12:05', '12:50'], ['13:00', '14:30'], ['14:50', '16:30'], ['16:40', '18:15'], ['18:25', '20:00']]

#За такой костыль надо бить по рукам
def current_time():
	return datetime.strptime(str(datetime.now().hour)+str(datetime.now().minute), "%H%M")

#Возврат расписания с проверкой на вторник
def raspisanie():
	if datetime.today().weekday() == 1:
		return zvonki_vtornik
	else:
		return zvonki
	
#Возвращает номер текущей пары если пар нет то 0
def get_para_num():
	para_num = 0
	for idx, para in enumerate(raspisanie()):
		para_st = datetime.strptime(para[0], "%H:%M")
		para_end = datetime.strptime(para[1], "%H:%M")
		if para_st < current_time() and current_time() < para_end:
			#print('Сейчас идет {} пара'.format(idx+1))
			para_num = idx+1
	return para_num

#Принимает номер пары, возвращает оставшиеся до конца время
def when_para_ends(para_num):
	para_end = datetime.strptime(raspisanie()[para_num-1][1], "%H:%M")
	remaining = para_end - current_time()
	return remaining
#Принимает номер пары возвращает время до ее начала
def when_para_start(para_num):
	para_st = datetime.strptime(raspisanie()[para_num-1][0], "%H:%M")
	remaining = para_st  - current_time()
	return remaining
#print(datetime.strptime(when_para_start(1), "%H:%M"))
#print('Время: {}'.format(datetime.strftime(current_time(), "%H:%M")))
#print('Осталось {} пары'.format(get_para_num()))
#print('До конца пары {} ч.'.format(when_para_ends(get_para_num())))
