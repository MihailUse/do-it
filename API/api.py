#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# импорт необходимых библиотек
import pickle
import pandas as pd
from flask import Flask, request, render_template, send_file

# загружаем необходимые модули
with open('encoder.pcl', 'rb') as f:
    encoder = pickle.load(f)
    
with open('model.pcl', 'rb') as f:
    model = pickle.load(f)
# # Разработка API

# Определю команды(функции), которые будут доступны в API

# In[ ]:


app = Flask(__name__)

@app.route('/')
def check_server():
    return '''
    Сервер успешно запущен<br>
    Доступные команды:<br>
        /model/prediction/(file_name)/ - (file_name) имя файля по которому нужно сделать предсказание, формат файла должен быть .csv<br>
    '''

@app.route('/model/prediction_from_file/', methods = ['POST', 'GET'])  
def upload():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save('data/' + f.filename)  
        return get_predict(f.filename)
    else:
        return render_template("file_upload_form.html")  
    

@app.route('/model/prediction/<string:file_name>/')
def get_predict(file_name):
    print('файл загружен', 'data/'+ file_name)
    
    X_df = pd.read_csv('data/'+ file_name)
    
    send_file('data/'+file_name, as_attachment=True) # автоматическая загрузка файла
    return 'success'


# ### Запуск сервера

# Чтобы перейти на гл. страницу перейдите по ссылке ниже.

# In[ ]:


app.run()


# Для проверки роботоспособности API можно перейти по ссылке: http://127.0.0.1:5000/model/prediction/example.csv/

# In[ ]:





# In[ ]:




