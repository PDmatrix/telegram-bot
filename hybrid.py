import replacements
import schedule


def getHybrid(group="пр1-15", day="завтра"):
    zamen = replacements.getChange(group, day).replace(u'\xa0',
                                                        '').split('\n')
    rsps = schedule.getSchedule(group, day).replace(u'\xa0', '').replace(
        u'\ufeff', '').replace(u'\r', '').split('\n')
    newRsps = []
    newRsps.append(rsps[0])
    for i in range(1, len(rsps) - 1):
        if rsps[i].find('*') == -1:
            newRsps.append(rsps[i])
            continue
        else:
            if rsps[i].find('**') != -1:
                if replacements.getStar(day) == 2:
                    newRsps.append(rsps[i])
            else:
                if replacements.getStar(day) == 1:
                    newRsps.append(rsps[i])
    rsps = newRsps
    if zamen[0] == "Расписание не готово." or \
        zamen[0] == "Что-то не так. Проверьте замены вручную." or \
            zamen[0] == "Сервер недоступен.":
        return zamen[0]
    elif zamen[0] == "Нет замен.":
        return '\n'.join(rsps)
    newZamen = []
    newZamen.append(zamen[0])
    for i in range(1, len(zamen) - 1):
        zamPar = zamen[i][0:zamen[i].find("пара")].replace(' ', '').split(',')
        if len(zamPar) != 1:
            for j in range(0, len(zamPar)):
                newZamen.append(zamPar[j] +
                                ' ' +
                                zamen[i][zamen[i].find("пара"):len(zamen[i])]
                                )
        else:
            newZamen.append(zamen[i])
    zamen = newZamen if len(newZamen) > 1 else zamen
    del newZamen
    for i in range(1, len(zamen)):
        for j in range(1, len(rsps)):
            if zamen[i][0:6] == rsps[j][0:6]:
                del rsps[j]
                break
    for i in range(1, len(zamen)):
        rsps.append(zamen[i])
    rsps = [line for line in rsps if line != '']
    tempDay = rsps[0]
    rsps = rsps[1:len(rsps)]
    rsps.sort(key=lambda x: int(x[0]))
    rsps.insert(0, tempDay)
    ans = '\n'.join(rsps[0:len(rsps)])
    return ans

print(getHybrid("и7-15"))
