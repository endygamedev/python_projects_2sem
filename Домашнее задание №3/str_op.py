s = "У лукоморья 123 дуб зеленый 456"

# Пункт 1:
print("Пункт 1\nВстречается ли буква 'я' в слове s:", 'я' in s)
print("Позиция буквы 'я' в слове s:", s.find('я'))
# Пункт 2:
print("\nПункт 2\nБуква 'у' встречается в слове s: {num} раза".format(num=s.count('у')))

# Пункт 3:
if s.isalpha()==False:
    print("\nПункт 3\nСостоит ли строка из букв: {bool} -> {str} ".format(bool=s.isalpha(),str=s.upper()))

# Пункт 4:
if len(s)>4:
    print("\nПункт 4\nДлина строки: {num} -> {str}".format(num=len(s),str=s.lower()))

# Пункт 5:
print("\nПункт 5\nЗамена: {str}".format(str=s.replace("У","О")))
