input_value = input("Введите атомный номер элемента: ")
if input_value:
    value = int(input_value)
    if value == 3:
        print("Литий - Li")
    elif value == 25:
        print("Марганец - Mn")
    elif value == 80:
        print("Ртуть - Hg")
    elif value == 17:
        print("Хлор - Cl")
    else:
        print("Я такого не знаю :(")
else:
    print("Введите атомный номер элемента!!!")