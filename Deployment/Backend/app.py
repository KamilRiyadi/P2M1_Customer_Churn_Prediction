from os import access
from flask import Flask, jsonify, request
import pickle
from tensorflow import keras
import pandas as pd
import numpy as np

app = Flask(__name__)

with open("pipe_FE.pkl", "rb") as f:
    pipe_FE = pickle.load(f)

model = keras.models.load_model('model.h5')

columns = [
    'tenure','gender',
    'SeniorCitizen', 'Partner',
    'Dependents','MultipleLines', 
    'InternetService', 'OnlineSecurity',
    'OnlineBackup','DeviceProtection',
    'TechSupport', 'StreamingMovies', 
    'Contract','PaperlessBilling', 
    'PaymentMethod'
]

classes = ['No', 'Yes']

@app.route("/")
def home():
    return "<h1>Welcome!</h1>"

@app.route("/predict", methods=['GET','POST'])
def model_prediction():
    if request.method == "POST":
        content = request.json
        try:
            data= [content['tenure'],
                   content['gender'],
                   content['SeniorCitizen'],
                   content['Partner'],
                   content['Dependents'],
                   content['MultipleLines'],
                   content['InternetService'],
                   content['OnlineSecurity'],
                   content['OnlineBackup'],
                   content['DeviceProtection'],
                   content['TechSupport'],
                   content['StreamingMovies'],
                   content['Contract'],
                   content['PaperlessBilling'],
                   content['PaymentMethod']
                   ]
            data = pd.DataFrame([data], columns=columns)
            data = pipe_FE.transform(data)
            pred = model.predict(data)
            pred = np.where(pred > 0.5, 1, 0)

            response = {"code": 200, "status":"OK", 
                        "result":{"prediction":str(pred[0].item()),
                                    "description":classes[pred[0].item()]}} 
            return jsonify(response)

        except Exception as e:

            response = {"code":500, "status":"ERROR", 
                        "result":{"error_msg":str(e)}}
            return jsonify(response)
    return "<p>Please access the API at https://kamil-churn-p2m1.herokuapp.com/</p>"