import requests
import re
from bs4 import BeautifulSoup


def getStar(day = "завтра"):
    if day == "завтра":
        day = "tomorrow"
    elif day == "сегодня":
        day = "today"
    site = requests.get("http://wwwold.chemk.org/student/raspisanie/4korp/{}.htm".format(day))
    cont = site.content
    soup = BeautifulSoup(cont, 'html.parser')
    if len(soup.find_all("tr")[0].p.text) != 49:
        return "Что-то не так. Проверьте замены вручную."
    mpa = dict.fromkeys(range(32))
    star = soup.find_all("tr")[2].text.translate(mpa).find("**")
    if star == -1:
        star = 1
    else:
        star = 2
    return star

def findChange(group = "пр1-15", day = "завтра"):
    if day == "завтра":
        day = "tomorrow"
    elif day == "сегодня":
        day = "today"
    site = requests.get("http://wwwold.chemk.org/student/raspisanie/4korp/{}.htm".format(day))
    cont = site.content
    soup = BeautifulSoup(cont, 'html.parser')
    lines = soup.find_all("tr")
    if len(lines) == 0:
        return "Расписание не готово."
    if len(lines[0].p.text) != 49:
        return "Что-то не так. Проверьте замены вручную."
    for i in range(5,len(lines)):
        strs = lines[i].find_all("p")
        ans = ""#Временный держатель
        rem = ""#Переменная для запоминания пары
        fin = []
        ans2 = ""#Финальный ответ
        if strs[0].text.lower() == group.lower():
            for k in range(i + 1,len(lines)):
                for j in range(1,len(strs)):
                    if strs[j].text == "1 п/г":
                        rem = strs[j + 1].text
                    ans += strs[j].text + ";"
                    if strs[j].text == "2 п/г":
                        ans += rem + ";"
                strs = lines[k].find_all("p")
                if len(strs[0].text) != 1:
                    break
                
                #Удаление всех управляющийх символов
                mpa = dict.fromkeys(range(32))
                fin = ans.translate(mpa).split(";")
        
                ans = ""
                if fin[0] == "1 п/г" or fin[0] == "2 п/г":
                    ans2 += fin[1] + " пара: " + fin[0] +" "+ fin[2] +". " + fin[3] + " " + fin[4] + "\n"
                else:
                    ans2 += fin[1] + " пара: " + fin[2] + ". " + fin[3] + " " + fin[4] + "\n"
            #Возвращение даты и замен
            return lines[1].p.text.translate(mpa) + "\n" + ans2
    if ans2 == "":
        return "Нет замен."
#print(getStar("today"))
#print(findChange("кс5-16","tomorrow"))
