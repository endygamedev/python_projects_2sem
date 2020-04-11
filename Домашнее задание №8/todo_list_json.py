import os
from tkinter import *

# Основная функция

# Я практически не стал переписывать ту функцию, которая была в предыдущих задании с ToDo-листом
# Можно было дефрагментировать этот код для каждого отдельного события, но пусть это будет так :)
def main_todo(in_tasks, out_tasks, action):
    if action == 1: # Добавление элемента в JSON файлик
        taskName = entryTaskName.get()
        taskCategory = entryCategory.get()
        taskDate = entryTime.get()

        if taskName and taskCategory and taskDate:
            out_tasks.write(f"\nЗадача: {taskName} Категория: {taskCategory} Дата: {taskDate}")

    if action == 2: # Демонстрация JSON файлика в TextBox
        textBox.config(state=NORMAL)
        textBox.delete(1.0, END)
        textBox.insert(END,''.join(in_tasks).strip())
        textBox.config(state=DISABLED)

    if action == 3: # Выходим из программы
        root.destroy()

# События для кнопок
def btnEvent(event, action):
    if os.path.exists('task_list.json'): # Проверка на существование текущего файл
        with open("task_list.json", 'r', encoding='utf8') as in_file, open("task_list.json", 'a',encoding='utf8') as out_file:
            main_todo(in_file.read(), out_file, action)
    else:
        with open("task_list.json", 'w', encoding='utf8') as out_file:
            main_todo("", out_file, action)

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

textBox = Text(root, yscrollcommand=scrollBarY.set, width=40,height=10, wrap=WORD, state=DISABLED)
textBox.grid(row=0,column=1, padx=10, pady=10)

scrollBarY.config(command=textBox.yview)

# Привязываем события к кнопкам
btnAddTask.bind('<Button-1>',lambda event, x=1: btnEvent(event, x))
btnShowTasks.bind('<Button-1>', lambda event, x=2: btnEvent(event, x))
btnExit.bind('<Button-1>', lambda event, x=3: btnEvent(event, x))

root.mainloop()
