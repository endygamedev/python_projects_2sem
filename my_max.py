def my_max(num1, num2):
    return num1 if num1 > num2 else num2

input_num1 = input("Введите первое число: ")
input_num2 = input("Введите второе число: ")
if input_num1 and input_num2:
    num1 = float(input_num1)
    num2 = float(input_num2)
    print("Наибольшее число:",my_max(num1, num2))
else:
    print("Введите числа!!!")