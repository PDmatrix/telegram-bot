import codecs
import json


def getAnswer(question):
    answers = []
    jsn = json.load(codecs.open('test.json', "r", "utf-8"))
    for qa in jsn["source"]["item"]:
        if qa["question"].lower().find(question.lower()) != -1:
            answers.append(qa["question"])
            answers.append(qa["answer"])
    return answers
