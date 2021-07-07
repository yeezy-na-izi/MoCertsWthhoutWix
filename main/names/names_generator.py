from .names import male_names, female_names, surnames_list
import random

male = male_names.split('\n')
female = female_names.split('\n')


def false_user():
    gender = random.randint(1, 2)  # 1 male
    if gender == 1:
        name = random.choice(male)
        surname = random.choice(surnames_list)
    else:
        name = random.choice(female)
        surname = random.choice(surnames_list)
        if surname[-1] == 'в' or surname[-1] == 'н':
            surname += 'а'
    return name, surname
