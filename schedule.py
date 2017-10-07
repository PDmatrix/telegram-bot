from datetime import datetime, date, time
import codecs

def getNum(day):
    day = day.lower()
    if day == "\ufeffпонедельник\r\n":
        return 0
    elif day == "вторник\r\n":
        return 1
    elif day == "среда\r\n":
        return 2
    elif day == "четверг\r\n":
        return 3
    elif day == "пятница\r\n":
        return 4
    elif day == "суббота\r\n":
        return 5
    else:
        return "Неправильно введён день"
    
def getSchedule(day):
    date = datetime.today()
    week = date.weekday()
    return week
    day = day.lower()
    if day == "пн":
        week = 0
    elif day == "вт":
        week = 1
    elif day == "ср":
        week = 2
    elif day == "чт":
        week = 3
    elif day == "пт":
        week = 4
    elif day == "сб":
        week = 5
    elif day == "сегодня":
        week = date.weekday()
    elif day == "завтра":
        week += 1
        if week == 6:
            week = 0
    else:
        return "Введен неправильный день. Возможные варианты: пн, вт, ср, чт, пт, сб, сегодня, завтра"
    
    f = codecs.open("rs.txt", "r", "utf-8")
    questions = f.readlines()
    answer = ""
    for i in range(0,len(questions) - 1):
        #print(getNum(questions[i]))
        if getNum(questions[i]) == week:
            for j in range(i, len(questions)):
                if questions[j] == '\r\n':
                    break
                answer += questions[j]
            f.close()
            return answer
