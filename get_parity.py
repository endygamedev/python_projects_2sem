def parity(num):
    return "Чётное" if num%2 == 0 else "Нечётное"

input_num = input("Введите число: ")
if input_num:
    print(parity(int(input_num)))
else:
    print("Введите число!!!")