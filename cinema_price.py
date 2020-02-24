film = input("Введите фильм: ")
date = input("Введите день (сегодня, завтра): ")
time = input("Введите время: ")
count = input("Введите количество билетов: ")

time_paraziti = [12, 16, 20]
time_1917 = [10, 13, 16]
time_sonic = [10, 14, 18]

dates = ["завтра","сегодня"]

def fun_price(film, time):
    '''Цена одного билета.'''
    if film == "Паразиты":
        return {
            time == time_paraziti[0]: 250,
            time == time_paraziti[1]: 350,
            time == time_paraziti[2]: 450,
            time not in time_paraziti: 0
        }[1]
    elif film == "1917":
        return {
            time == time_1917[0]: 250,
            time == time_1917[1]: 350,
            time == time_1917[2]: 350,
            time not in time_1917: 0
        }[1]
    elif film == "Соник в кино":
        return {
            time == time_sonic[0]: 350,
            time == time_sonic[1]: 450,
            time == time_sonic[2]: 450,
            time not in time_sonic: 0
        }[1]
    else:
        return 0

def fun_discount(date, price, count):
    '''Считает скидку на билеты.'''
    if price != 0:
        return {
            date == dates[0] and count > 0: price*0.95,
            date == dates[1] and count > 0: price,
            date == dates[1] and count >= 20: price*0.8,
            date == dates[0] and count >= 20: price*0.75,
            date not in dates or count <= 0: 0
        }[1]
    else:
        return 0

if film and date and time and count:
    print("Выбрали фильм:", film, "День:", date, "Время:", time, "Количество билетов:", count)
    tickets_price = fun_discount(date, int(count)*fun_price(film, int(time)), int(count))
    if tickets_price != 0:
        print("Результат:", tickets_price, "руб.")
    else:
        print("Ошибка ввода!")
else:
    print("Ошибка ввода!")