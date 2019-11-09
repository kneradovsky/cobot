from parsers import keyboard_to_list
reg_keyboard = [['Да, хочу!']]
reg_keyboard2 = [['Хочу ещё кофе!'], ['Мои подтверждённые заявки'], ["Мои неподтверждённые заявки"]]
loc_keyboard = [['Москва, Летниковская'], ['Москва, Спартаковская'], ['Москва, Котельническая'], ['Москва, Электрозаводская'],
['Саратов, Орджоникидзе'], ['Саратов, Шелковичная'], ['Новосибирск, Добролюбова,'], ['Новосибирск, Кирова'],
['Казань, Лево-Булачная'], ['Екатеринбург, Толмачёва'], ['Хабаровск, Амурский бульвар'], ['Ханты-Мансийск, Мира']]
time_keyboard = [['Сейчас'], ['с 9 до 12'], ['с 12 до 15'], ['с 15 до 18']]
date_keyboard = [['Сегодня'], ['Завтра'], ['Послезавтра']]

locations = keyboard_to_list(loc_keyboard)
times = keyboard_to_list(time_keyboard)
dates = keyboard_to_list(date_keyboard)
