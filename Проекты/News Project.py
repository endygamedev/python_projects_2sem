from tkinter import *
from tkinter import messagebox as mb
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

# https://lenta.ru/rss/news
# https://lenta.ru/rss/last24
# https://news.yandex.ru/index.rss
# https://news.rambler.ru/rss/world/
# http://static.feed.rbc.ru/rbc/internal/rss.rbc.ru/rbc.ru/news.rss
# http://www.vsesmi.ru/rss/all/
# https://ria.ru/export/rss2/index.xml


class main:
    def __init__(self, root):
        self.root = root
        self.db = db

        self.menuFrame = LabelFrame(root, text="Меню")

        self.labelUrl = Label(self.menuFrame, text='Введите RSS:')
        self.labelUrl.pack()

        self.entryUrl = Entry(self.menuFrame, width=30)
        self.entryUrl.pack()


        self.labelNews = Label(self.menuFrame, text='Введите интересующие вас темы: ')
        self.labelNews.pack()

        self.entryNews = Entry(self.menuFrame, width=40)
        self.entryNews.pack(padx=3, pady=3)

        self.menuFrame.pack()

        self.textBox = Text(root)
        self.textBox.pack(expand=1, fill=BOTH)

        self.scrollBarX = Scrollbar(self.textBox, orient=HORIZONTAL)
        self.scrollBarX.pack(side=BOTTOM, fill=X, anchor=W)

        self.scrollBarY = Scrollbar(self.textBox, orient=VERTICAL)
        self.scrollBarY.pack(side=RIGHT, fill=Y)

        self.scrollBarX.config(command=self.textBox.xview)
        self.scrollBarY.config(command=self.textBox.yview)

        self.textBox.config(yscrollcommand=self.scrollBarY.set, xscrollcommand=self.scrollBarX.set)

        #self.entryNews.bind('<Return>', lambda event: self.searchNews(event, self))
        self.entryNews.bind('<Return>', lambda event: self.entryNews_Event(event, self, self.entryNews.get(),
                                                                      datetime.datetime.now().strftime("%d/%m/%y"),
                                                                      datetime.datetime.now().strftime("%H:%M")))
        self.entryUrl.bind('<Return>', lambda event: self.checkUrl(event, self))

    @staticmethod
    def checkUrl(event, self):
        '''Парсит новости с RSS ленты'''
        allNews = []
        listWebsites = self.entryUrl.get().split()
        if listWebsites:
            try:
                for url in listWebsites:
                    resp = requests.get(url)
                    soup = BeautifulSoup(resp.content, features="html.parser")
                    themes = soup.findAll('description')
                    for news in themes:
                        allNews.append(news.text)
                return allNews
            except:
                mb.showerror("Ошибка", "Введите корректную ссылку!\nПример: https://lenta.ru/rss/news")
        else:
            mb.showerror("Ошибка", "Введите ссылку!")

    @staticmethod
    def searchNews(event, self):
        '''Выбирает выбранные новости из всех новостей'''
        self.textBox.delete(1.0, END)
        selectedNews = self.entryNews.get().lower().split()
        if selectedNews:
            for allNews in self.checkUrl(event, self):
                for news in selectedNews:
                    if news in allNews.lower():
                        self.textBox.insert(END, allNews)
        else:
            mb.showerror("Ошибка", "Введите темы/ключевые слова!")

    @staticmethod
    def recordData(event, self, inquiries, date, time):
        '''Добавляет запрос в базу данных'''
        self.db.insert_data(inquiries, date, time)

    @staticmethod
    def entryNews_Event(event, self, inquiries, date, time):
        self.searchNews(event, self)
        self.recordData(event, self, inquiries, date, time)

class DB:
     def __init__(self):
        self.conn = sqlite3.connect('search_story.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS search_story(id INTEGER PRIMARY KEY, inquiries TEXT, date TEXT, time TEXT)")
        self.conn.commit()

     def insert_data(self, inquiries, date, time):
        '''Добавляет запросы в базу данных'''
        self.c.execute("INSERT INTO search_story(inquiries, date, time) VALUES(?,?,?)", (inquiries, date, time))
        self.conn.commit()

if __name__ == "__main__":
    root = Tk()
    root.title('Приложение для чтения новостей')
    root.geometry('800x600')
    root.resizable(False, False)
    #root.attributes("-zoomed", True)
    db = DB()
    app = main(root)
    root.mainloop()