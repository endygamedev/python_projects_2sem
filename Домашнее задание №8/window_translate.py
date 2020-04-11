from tkinter import *
from tkinter import messagebox as mb
import requests
from bs4 import BeautifulSoup
import random

# Собираем наши словечки
wordList = []
url = 'https://lifehacker.ru/200-essential-english-words/' # Если сайт сломался, то я не причём :-)
resp = requests.get(url)
soup = BeautifulSoup(resp.content, features="html.parser")
words = soup.findAll('li')
for word in words:
    if '\n' not in word:
        wordList.append(word.text)

wordList = ''.join(wordList).replace(';',' — ').replace('.',' — ').split(' — ')

englishWords = wordList[0::2]
russianWords = wordList[1::2]

wordDict = dict(zip(englishWords, russianWords)) # Наконец-то создали наш словарик :-)

def checkAnswer(event):
    if entryTranslate.get().lower() == wordDict[rndWord.get()]:
        mb.showinfo('Выйграли','Вы угадали слово!')
        rndWord.set(random.choice(list(wordDict.keys())))
        entryTranslate.delete(0, END)
        count.set(count.get() + 1)
    else:
        mb.showerror('Проиграли', f'Вы неправильно перевели!\nПравильное значение: {wordDict[rndWord.get()]}')
        rndWord.set(random.choice(list(wordDict.keys())))
        entryTranslate.delete(0, END)
        if count.get() > 0:
            count.set(count.get() - 1)

root = Tk()
root.title('Перевод4ик')

scoreFrame = Frame(root, highlightbackground="black", highlightthickness=1, background='yellow')

rndWord = StringVar()
rndWord.set(random.choice(list(wordDict.keys()))) # Случайное слово из словаря

count = IntVar()
count.set(0)

labelScore = Label(scoreFrame, text='Ваш счёт: ', background='yellow')
labelScore.pack()

labelCount = Label(scoreFrame, textvariable=count, background='yellow', font="Bold")
labelCount.pack()

scoreFrame.pack(pady=5)

labelTitle = Label(root, text='Случайное слово: ')
labelTitle.pack()

labelWord = Label(root, textvariable=rndWord)
labelWord.pack()

labelTranslate = Label(root, text='Укажите слово для перевода: ')
labelTranslate.pack()

entryTranslate = Entry(root, width=40)
entryTranslate.pack(padx=5)

entryTranslate.bind('<Return>', lambda event: checkAnswer(event)) # Возможность отвечать по кнопке Enter из текстового поля

btnAnswer = Button(root, text='Готово!')
btnAnswer.pack()

btnAnswer.bind('<Button-1>', lambda event: checkAnswer(event))

btnExit = Button(text='Выход', command=lambda x=root: x.destroy())
btnExit.pack()

root.mainloop()
