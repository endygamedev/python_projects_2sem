# Можно было бы сделать и через if, но получилось бы громостко
codes = [343, 381, 473, 485]
times = [15, 18, 13, 11]

def call_cost(code, time):
    return {
        code == codes[0]: time*times[0],
        code == codes[1]: time*times[1],
        code == codes[2]: time*times[2],
        code == codes[3]: time*times[3],
        code not in codes: "Такого кода нет"
    }[1]

input_code = input("Введите код города: ")
input_time = input("Введите длительность переговоров (в минутах): ")
if input_code and input_time:
    print(call_cost(int(input_code), int(input_time)))
else:
    print("Введите значение переменных!!!")