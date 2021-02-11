#!/usr/bin/env python
# coding: utf-8

# # Бот в консоли

# In[ ]:


def send_message(s):
    print(f'> Бот:\n{s}')
    
def get_message():
    message = input('> Пользователь:\n')
    message = message.lower()
    message = message.strip()
    return message

def helpp():
    send_message('Чтобы посмотреть список команд введите commands, для выхода введите exit')
    
# функции для проверки ввода
def encode(feature_name):
    input_feature = get_message()
    try:
        return encoder[feature_name].transform([input_feature])[0]
    except:
        send_message('введены некорректные данные')
        encode(feature_name, get_message())
        
def get_feature():
    try:
        return int(get_message())
    except:
        send_message('введены некорректные данные')
        get_feature(get_message()) 

# предсказание
def get_predict():
    X_df = {}
    
    send_message('Ведите возраст')
    X_df['age'] = encode('age')
    
    send_message('Ведите время проведенное в госпитале')
    X_df['time_in_hospital'] = get_feature()
    
    send_message('Ведите количество лабораторных процедур')
    X_df['num_lab_procedures'] = get_feature()
    
    send_message('Ведите количество лекарств')
    X_df['num_medications'] = get_feature()

    send_message('Ведите количество диагнозов')
    X_df['number_diagnoses'] = get_feature()
    
    send_message('Ведите результат A1Cresult')
    X_df['A1Cresult'] = encode('A1Cresult')
    
    send_message('Ведите результат на insulin')
    X_df['insulin'] = encode('insulin')
    
    send_message('введенные данные:\n'+ ('\n'.join([k+' - '+str(v) for k, v in X_df.items()])))
    
    
    pred = model.predict([list(X.values())])
    res = encoder['readmitted'].inverse_transform(pred)[0] if encoder['readmitted'].inverse_transform(pred)[0] != 'NO' else '0'
    send_message(f'Наиболее вероятно, что пациент будет повторно принят: {res} раз')


# In[ ]:


# список команд
commands = {
    'help': helpp,
    'помощь': helpp,
    'get_predict': get_predict,
    'commands': lambda: send_message(', '.join(commands.keys())),
}

commands_exit = [
    'exit', 
    'выход'
]


# In[ ]:


while True:
    put = get_message()
    if put in commands_exit:
        break        
    elif put in commands:
        commands[put]()
    else:
        send_message('Я вас не понимаю. Введите commands, чтобы посмотреть список команд')


# # Бот в окне

# In[ ]:


from tkinter import *


# In[ ]:


# словарь с фичами
X_def = {
    'age': None,
    'time_in_hospital': None,
    'num_lab_procedures': None,
    'num_medications': None,
    'number_diagnoses': None,
    'A1Cresult': None,
    'insulin': None,
}


# In[ ]:


predicting = False
X = X_def.copy()

def send(event=None):
    put = get_message()
    if put == '':
        return
    if put == ('exit' or 'выход'):
        root.destroy()
    elif predicting:
        predict(put)
    elif put == ('commands' or 'команды'):
        send_message(', '.join(commands.keys()))
    elif put in commands:
        commands[put]()
    else:
        send_message('Я вас не понимаю. Введите "help" для помощи')
    
def send_message(s):
    chat.configure(state=NORMAL)
    chat.insert(END,f'> Бот: {s}\n')
    chat.configure(state=DISABLED)
    
def get_message():
    message = input_field.get()
    message = message.strip()
    if message == '':
        return ''
    chat.configure(state=NORMAL)
    chat.insert(END,"> Пользователь: " + message + '\n')
    chat.configure(state=DISABLED)
    input_field.delete(0, 'end')
    return message


def helps():
    send_message('''
-введите "commands" или "команды" для просмотра списка команд
-введите "get_predict" или "предсказание" для предсказания по введенным данным
-Lля того чтобы выйти наберите "exit" или "выход"
''')
    

# предсказание
def get_predict():
    global predicting
    predicting = True    
    send_message('Нужно ввести данные, чтобы сделать предсказание')
    predict()

def predict(message=None):
    global predicting
    global X
    
    for k in X.keys(): 
        if X[k] is None:
            X[k] = message
            break
    
    for k in X.keys(): 
        if X[k] is None:
            send_message(f'Введите {k}')
            return           
            
    send_message('введенные данные:\n'+ ('\n'.join([k+' - '+str(v) for k, v in X.items()])))
    try:
        X = {
            'age': encoder['age'].transform([X['age']])[0],
            'time_in_hospital': X['time_in_hospital'],
            'num_lab_procedures': X['num_lab_procedures'],
            'num_medications': X['num_medications'],
            'number_diagnoses': X['number_diagnoses'],
            'A1Cresult': encoder['A1Cresult'].transform([X['A1Cresult']])[0],
            'insulin': encoder['insulin'].transform([X['insulin']])[0],
        }
    except:
        X = X_def.copy()
        predicting = False
        send_message('Введены некорректные данные')
        return
    
    pred = model.predict([list(X.values())])
    res = encoder['readmitted'].inverse_transform(pred)[0] if encoder['readmitted'].inverse_transform(pred)[0] != 'NO' else '0'
    send_message(f'Наиболее вероятно, что пациент будет повторно принят: {res} раз')
    
    X = X_def.copy()
    predicting = False


# In[ ]:


# список команд
commands = {
    'help': helps,
    'помощь': helps,
    'get_predict': get_predict,
}


# In[ ]:


root = Tk()

# Настройки окна
root.title("Чат-бот")
root.geometry("680x630+400+200")
root.resizable(width=False, height=True)

# Поле вывода текста
scroll_chat = Scrollbar(root)
scroll_chat.pack(side=RIGHT, fill=Y)

chat = Text(root, font=("Arial", 16), fg="black", yscrollcommand=scroll_chat.set)
chat.pack(fill=BOTH)
send_message("""
-Ведит "help" или "помощь" для вызова справки
-Введите "get_predict" для предсказания
-Для того чтобы выйти наберите "exit" или "выход"
""")


# Кнопка для отправки 
button = Button(root, font=("Arial", 16), text='Отправить', bg='gray', borderwidth=2, relief="groove", command=send)
button.bind('<Return>', send)
button.pack(side=RIGHT, fill=BOTH)


# Поле для ввода текста
scroll_input = Scrollbar(root)
scroll_input.pack(side=RIGHT, fill=Y)
input_field = Entry(root, font=("Arial", 24), fg="black", borderwidth=2, relief="groove", width=30)
input_field.bind('<Return>', send)
input_field.pack(side=LEFT, fill=BOTH)


root.mainloop()

