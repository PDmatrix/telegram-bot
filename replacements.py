import requests
from bs4 import BeautifulSoup


# Функция получения недели(четная или нечётная)
def getStar(day="завтра"):
    if day == "завтра":
        day = "tomorrow"
    elif day == "сегодня":
        day = "today"
    try:
        site = requests.get(
            "http://wwwold.chemk.org/student/raspisanie/4korp/{}.htm".format(
                day))
    except Exception:
        return "Сервер недоступен."
    cont = site.content
    soup = BeautifulSoup(cont, 'html.parser')
    lun = 0
    ne = False
    if len(soup.find_all("tr")[0].p.text) != 49 or len(
            soup.find_all("tr")[0].p.text) != 46:
        for i in range(0, len(soup.find_all("tr"))):
            if len(soup.find_all("tr")[i].p.text) == 49 or len(
                    soup.find_all("tr")[i].p.text) == 46:
                lun = i
                ne = True
                break
        if ne is False:
            return "Что-то не так. Проверьте замены вручную."
    mpa = dict.fromkeys(range(32))
    star = soup.find_all("tr")[2 + lun].text.translate(mpa).find("**")
    if star == -1:
        star = 1
    else:
        star = 2
    return star


# Функция поиска замен
def findChange(group="пр1-15", day="завтра"):
    if day == "завтра":
        day = "tomorrow"
    elif day == "сегодня":
        day = "today"
    try:
        site = requests.get(
            "http://wwwold.chemk.org/student/raspisanie/4korp/{}.htm".format(
                day))
    except Exception:
        return "Сервер недоступен."
    cont = site.content
    soup = BeautifulSoup(cont, 'html.parser')
    lines = soup.find_all("tr")
    if len(lines) == 0:
        return "Расписание не готово."
    lun = 0
    ne = False
    if len(lines[0].p.text) != 49 or len(lines[0].p.text) != 46:
        #
        for i in range(0, len(lines)):
            if len(lines[i].p.text) == 49 or len(lines[i].p.text) == 46:
                lun = i
                ne = True
                break
        if ne is False:
            return "Что-то не так. Проверьте замены вручную."

    for i in range(5 + lun, len(lines)):
        strs = lines[i].find_all("p")
        if strs == []:
            continue
        ans = ""  # Временный держатель
        rem = ""  # Переменная для запоминания пары
        fin = []
        ans2 = ""  # Финальный ответ
        if strs[0].text.lower() == group.lower():
            for k in range(i + 1, len(lines)):
                for j in range(1, len(strs)):
                    if strs[j].text == "1 п/г":
                        rem = strs[j + 1].text
                    ans += strs[j].text + ";"
                    if strs[j].text == "2 п/г":
                        ans += rem + ";"
                strs = lines[k].find_all("p")
                strs.insert(0, '')
                if strs == []:
                    break
                # Проверка на концовку группы
                if ans[0] == u'\xa0' and ans[2] == u'\xa0' \
                        and ans[4] == u'\xa0':
                    break
                # Удаление первого символа
                if ans[0] == u'\xa0':
                    ans = ans[2:]
                if ans[0] == u'\xa0':
                    ans = ans[2:]

                # Удаление всех управляющийх символов
                mpa = dict.fromkeys(range(32))
                fin = ans.translate(mpa).split(";")
                ans = ""
                if len(fin) == 3:
                    ans2 += fin[0] + " пара: " + fin[1] + "\n"
                    break
                elif len(fin) == 4:
                    ans2 += fin[1] + " пара: " + fin[0] + " " + fin[2] + "\n"
                    break
                elif fin[0] == "1 п/г" or fin[0] == "2 п/г" \
                        or fin[0] == "(1/2)":
                    ans2 += fin[1] + " пара: " + fin[0] + " " + \
                        fin[2] + ". " + fin[3] + " " + fin[4] + "\n"
                else:
                    ans2 += fin[0] + " пара: " + fin[1] + ". " + \
                        fin[2] + " " + fin[3] + "\n"
            # Возвращение даты и замен
            return lines[1].p.text.translate(mpa) + "\n" + ans2
    if ans2 == "":
        return "Нет замен."
