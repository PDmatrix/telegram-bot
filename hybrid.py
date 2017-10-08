import replacements, schedule
 
def getHybrid(group = "пр1-15", day = "завтра"):
    zamen = replacements.findChange(group,day).replace(u'\xa0','').split('\n')
    rsps = schedule.getSchedule(day).replace(u'\xa0','').replace(u'\ufeff','').replace(u'\r','').split('\n')
    if zamen[0] == "Расписание не готово.":
        return zamen[0]
    elif zamen[0] == "Что-то не так. Проверьте замены вручную.":
        return zamen[0]
    elif zamen[0] == "Нет замен.":
        return schedule.getSchedule(day)
    elif zamen[0] == "Сервер недоступен.":
        return zamen[0]
    if rsps[0] == "Пятница":
        if replacements.getStar("tomorrow") == 1:
            del rsps[3]
        else:
            del rsps[2]
    last = ""
    zm = 0
    fr = True
    for i in range(0, len(rsps) - 1):
        for j in range(1 + zm, len(zamen)):
            if zamen[j][0:6] == rsps[i][0:6]:
                if fr == True:
                    rsps[i] = zamen[j]
                else:
                    rsps[i] +="\n" + zamen[j]
                zm += 1
                fr = False
        rsps[i] += "\n"
        fr = True
    if len(zamen)-zm != 2:
        for i in range(1 + zm, len(zamen) - 1):
            rsps.append(zamen[i] + "\n")
    ans = ''.join(rsps).rstrip('\n')
    return ans
