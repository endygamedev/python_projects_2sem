import sqlite3
from tkinter import *

# Основная функция

# Я практически не стал переписывать ту функцию, которая была в предыдущих задании с ToDo-листом
# Можно было дефрагментировать этот код для каждого отдельного события, но пусть это будет так :)
def main_todo(cursor, action):
    if action == 1: # Добавление элемента в DB
        taskName = entryTaskName.get()
        taskCategory = entryCategory.get()
        taskDate = entryTime.get()

        if taskName and taskCategory and taskDate:
            cursor.execute("INSERT INTO tasks(id, category, name, time) VALUES(NULL,?,?,?)", (taskCategory, taskName, taskDate))

    if action == 2: # Демонстрация DB файлика в TextBox
        textBox.delete(1.0, END)
        for task in cursor.execute("SELECT * FROM tasks").fetchall():
            textBox.insert(END, f"\nЗадача: {task[2]} Категория: {task[1]} Дата: {task[3]}")
    if action == 3: # Выходим из программы
        root.destroy()

# События для кнопок
def btnEvent(event, action):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, category TEXT, name TEXT, time TEXT)")
    main_todo(cursor, action)
    conn.commit()
    conn.close()

# Создаём GUI
root = Tk()
root.title('Менеджер задач')
root.resizable(False,False)

frameMenu = Frame(root)

labelTaskName = Label(frameMenu, text='Задача: ')
labelTaskName.grid(row=0,column=0,padx=3)

entryTaskName = Entry(frameMenu, width=20)
entryTaskName.grid(row=0,column=1, padx=3)

labelCategory = Label(frameMenu, text='Категория: ')
labelCategory.grid(row=1, column=0, padx=3)

entryCategory = Entry(frameMenu, width=20)
entryCategory.grid(row=1, column=1, padx=3)

labelTime = Label(frameMenu, text='Время:')
labelTime.grid(row=2, column=0, padx=3)

entryTime = Entry(frameMenu, width=20)
entryTime.grid(row=2, column=1, padx=3)

btnAddTask = Button(frameMenu, text='Добавить')
btnAddTask.grid(row=3,column=1)

btnShowTasks = Button(frameMenu, text='Список задач')
btnShowTasks.grid(row=4,column=1)

btnExit = Button(frameMenu, text='Выход')
btnExit.grid(row=5,column=1)

frameMenu.grid(row=0,column=0)

scrollBarY = Scrollbar(root, orient=VERTICAL)
scrollBarY.grid(row=0,column=2, sticky='ns')

textBox = Text(root, yscrollcommand=scrollBarY.set, width=40,height=10, wrap=WORD)
textBox.grid(row=0,column=1, padx=10, pady=10)

scrollBarY.config(command=textBox.yview)

# Привязываем события к кнопкам
btnAddTask.bind('<Button-1>',lambda event, x=1: btnEvent(event, x))
btnShowTasks.bind('<Button-1>', lambda event, x=2: btnEvent(event, x))
btnExit.bind('<Button-1>', lambda event, x=3: btnEvent(event, x))

root.mainloop()
