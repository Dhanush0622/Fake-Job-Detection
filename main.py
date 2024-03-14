from flask import Flask, render_template, request,redirect, flash, url_for
import mysql.connector
import pickle
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
from jinja2 import TemplateNotFound
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=11)
df = pd.read_csv('fake_job_postings.csv')
df.dropna(inplace=True)

app = Flask(__name__)
app.secret_key=b'codegnas$#@key^*^&*^&*^&7e63463ruwyasgdjs*^*^&^&'

mydb = mysql.connector.connect(host='localhost',user='root',password='admin',db='project')

@app.route('/',methods=['POST','GET'])
def create():
    if request.method == 'POST':
        #print(request.form)
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        #cpassword=request.form['CPassword']
        print(name,email,password)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into users (name,Email,password) values(%s,%s,%s)',(name,email,password))
        cursor.close()
        mydb.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email=request.form['Email']
        password=request.form['Password']
        #print(email,password)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select email,password from users where Email=%s',[email])
        user,pwd= cursor.fetchone()
        cursor.close()
        #print(user,pwd)
        if user == email and pwd == password:
            flash('Login successfull...!')
            return render_template('index.html')
            #return redirect(url_for('index'))
        else:
            flash('Invalide user or password...!')
            return render_template('login.html')
    return render_template('login.html')

# Load the trained machine learning model
model = pickle.load(open('models/RFC_MODEL.pkl', 'rb'))
#vectorizer = pickle.load(open('models/vectorizer.pkl','rb'))


# Define a simple tokenizer function
def tokenize(text):
    text = re.sub(r'\W', ' ', text)
    tokens = text.lower().split()
    return tokens

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        description = request.form['description']
        #description = input("Enter the value:")
        input_data = [description]
        encoded_input = vectorizer.transform([' '.join(input_data)])

        # Make predictions using the trained model
        predict = model.predict(encoded_input)
        print(predict)
        '''
        try:
            # Pad sequences to fixed length
            max_sequence_length = 250  # Assuming a maximum sequence length of 40
            padded_input = pad_sequences([tokenized_input], maxlen=max_sequence_length, padding='post')
            print(padded_input)
        except ValueError:
            return render_template('error.html', message='Input text is too long. Please provide a shorter text.')
        
        # Make predictions
        prediction = model.predict(padded_input)
        print(prediction)
        '''
        # Convert prediction to text label
        result = "Fake" if predict[0] == 1 else "Real"
        
        return render_template('result.html', prediction=result)
        
       # return render_template('result.html', prediction=result)

@app.errorhandler(TemplateNotFound)
def template_not_found(e):
    return render_template('error.html', message='Template not found.')

if __name__ == '__main__':
    app.run(debug=True)
