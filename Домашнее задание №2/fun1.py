def fun(x):
    return x**2 if -2.4 <= x <= 5.7 else 4

input_x = input("Введите значения перменной x: ")
if input_x:
    print(fun(float(input_x)))
else:
    print("Введите число!!!")