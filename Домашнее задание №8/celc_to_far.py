from tkinter import *

def celc_to_far():
    try:
        labelOutput.config(text = 9/5*float(entryInput.get())+32)
    except ValueError:
        labelOutput.config(text='Ошибка ввода')

root = Tk()
root.title('Конвертатор')

labelTitle = Label(text='Температура в Цельсиях:')
labelTitle.pack()

entryInput = Entry(width=30, justify='center')
entryInput.pack(padx=5)

labelOutput = Label(text='Тут будет Out :-)')
labelOutput.pack()

btnConvert = Button(text='Конвертировать!', command=celc_to_far)
btnConvert.pack()

btnExit = Button(text='Выход', command= lambda x=root: x.destroy())
btnExit.pack()

root.mainloop()
