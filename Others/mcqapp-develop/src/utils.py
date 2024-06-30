import json
import random

file = open('questions.txt','r')
var = file.read()
questions = json.loads(var)
i = len(questions)


def evaluate(content):
    pass


def generate_questions(num):
    print ("i",i)
    print ("questions",questions)
    que_index = ques_index(num)
    print ("index",que_index)
    questions_exam = []
    for x in que_index:
        questions_exam.append(questions[x])
    return i,que_index,questions_exam


def ques_index(num):
    """ Randon question generator"""
    t=[]
    while len(t)<num:
        x = random.randint(0,i-1)
        if x in t:
            print ("present")
        else:
            t.append(x)
    return t