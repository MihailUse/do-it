#!/usr/bin/env python
# coding: utf-8

# In[2]:


# импорт необходимых библиотек
import pickle
import pandas as pd
from flask import Flask, request, render_template


# In[3]:


# загружаем необходимые модули
with open('encoder.pcl', 'rb') as f:
    encoder = pickle.load(f)
    
with open('model.pcl', 'rb') as f:
    model = pickle.load(f)


# # Разработка API

# Определю команды(функции), которые будут доступны в API

# In[4]:


app = Flask(__name__)

@app.route('/')
def check_server():
    return '''
    Сервер успешно запущен<br>
    Доступные команды:<br>
        /model/prediction/(file_name)/ - (file_name) имя файля по которому нужно сделать предсказание, формат файла должен быть .csv<br>
    '''

форма для заг
@app.route('/model/prediction_from_file/')  
def upload():  
    return render_template("file_upload_form.html")  

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save('data/' + f.filename)  
        get_predict(f.filename)
        

@app.route('/model/prediction/<string:file_name>/')
def get_predict(file_name):
    X_df = pd.read_csv('data/'+ file_name)
    
    X_df['age'] = encoder['age'].transform(X_df['age'])
    X_df['A1Cresult'] = encoder['A1Cresult'].transform(X_df['A1Cresult'])
    X_df['insulin'] = encoder['insulin'].transform(X_df['insulin'])
    
    pred = model.predict(X_df)
    res = encoder['readmitted'].inverse_transform(pred)[0] if encoder['readmitted'].inverse_transform(pred)[0] != 'NO' else '0'

    return f'Наиболее вероятно, что пациент будет повторно принят: {res} раз'


# ### Запуск сервера

# Чтобы перейти на гл. страницу перейдите по ссылке ниже.

# In[ ]:


app.run()


# Для проверки роботоспособности API можно перейти по ссылке: http://127.0.0.1:5000/model/prediction/example.csv/

# In[ ]:





# In[ ]:




