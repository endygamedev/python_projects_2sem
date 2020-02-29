import random

str_list=['самовар','весна','лето']
word=random.choice(str_list)
letter=random.choice(word)

print(word.replace(letter,"?"))
input_letter=input('Введите букву: ')

if input_letter==letter:
    print('Победа!\nСлово: {str}'.format(str=word))
else:
    print('Увы! Попробуй в другой раз.\nСлово: {str}'.format(str=word))
