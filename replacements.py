import requests
from bs4 import BeautifulSoup

def findChange(group, day):
    site = requests.get("http://wwwold.chemk.org/student/raspisanie/4korp/{}.htm".format(day))
    cont = site.content
    soup = BeautifulSoup(cont, 'html.parser')
    lines = soup.find_all("tr")
    if len(lines) == 0:
        return "Расписание не готово."
    for i in range(5,len(lines) - 1):
        strs = lines[i].find_all("p")
        ans = ""
        rem = ""
        fin = ""
        if strs[0].text.lower() == group.lower():
            for k in range(i + 1,len(lines) - 1):
                for j in range(1,len(strs)):
                    if strs[j].text == "1 п/г":
                        rem = strs[j + 1].text
                    ans += strs[j].text + " "
                    if strs[j].text == "2 п/г":
                        ans += rem + " "
                strs = lines[k].find_all("p")
                if len(strs[0].text) != 1:
                    break
                ans += "\n"
            return ans
    if ans == "":
        return "Нет замен."

