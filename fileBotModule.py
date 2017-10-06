def getAnswer(question):
    f = open("qu.txt", "r")
    answers = []
    questions = f.readlines()
    for i in range(0,len(questions) - 1,3):
        lowq = questions[i].lower()
        if lowq.find(question.lower()) != -1:
            answers.append(questions[i])
            answers.append(questions[i + 1])
    result = ""
    num = 0
    for ns in answers:
        result = result + ns;
        if num % 2 != 0:
            result = result + "\n"
        num = num + 1
    if result == "":
        result = "Error 404. Not found"
    f.close()
    return result
