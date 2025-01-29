import re
import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model

lines = open('../input/chatbot-data/cornell movie-dialogs corpus/movie_lines.txt', encoding='utf-8',
             errors='ignore').read().split('\n')

convers = open('../input/chatbot-data/cornell movie-dialogs corpus/movie_conversations.txt', encoding='utf-8',
             errors='ignore').read().split('\n')

exchn = []
for conver in convers:
    exchn.append(conver.split(' +++$+++ ')[-1][1:-1].replace(""'"", "" "").replace("","","""").split())

diag = {}
for line in lines:
    diag[line.split(' +++$+++ ')[0]] = line.split(' +++$+++ ')[-1]

## delete
del(lines, convers, conver, line)
questions = []
answers = []

for conver in exchn:
    for i in range(len(conver) - 1):
        questions.append(diag[conver[i]])
        answers.append(diag[conver[i+1]])
del(diag, exchn, conver, i)

# More preprocessing of QnA
# Maximum Length of Questions= 13

sorted_ques = []
sorted_ans = []
for i in range(len(questions)):
    if len(questions[i]) < 13:
        sorted_ques.append(questions[i])
        sorted_ans.append(answers[i])

def clean_text(txt):
    txt = txt.lower()
    txt = re.sub(r""i'm"", ""i am"", txt)
    txt = re.sub(r""he's"", ""he is"", txt)
    txt = re.sub(r""she's"", ""she is"", txt)
    txt = re.sub(r""that's"", ""that is"", txt)
    txt = re.sub(r""what's"", ""what is"", txt)
    txt = re.sub(r""where's"", ""where is"", txt)
    txt = re.sub(r""\'ll"", "" will"", txt)
    txt = re.sub(r""\'ve"", "" have"", txt)
    txt = re.sub(r""\'re"", "" are"", txt)
    txt = re.sub(r""\'d"", "" would"", txt)
    txt = re.sub(r""won't"", ""will not"", txt)
    txt = re.sub(r""can't"", ""can not"", txt)
    txt = re.sub(r""[^\w\s]"", """", txt)
    return txt
