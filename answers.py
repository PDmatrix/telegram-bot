import codecs

def getAnswer(question):
    f = codecs.open("qu.txt", "r", "utf-8")
    answers = []
    questions = f.readlines()
    for i in range(0,len(questions),3):
        lowq = questions[i].lower()
        if lowq.find(question.lower()) != -1:
            answers.append(questions[i])
            answers.append(questions[i + 1])
    result = ""
    f.close()
    return answers
    num = 0
    for ns in answers:
        result = result + ns;
        if num % 2 != 0:
            result = result + "\n"
        num = num + 1
    if result == "":
        result = "Вопрос не найден."

    f.close()
    return result