import streamlit as st
import requests
import numpy as np
from PIL import Image

st.set_page_config(layout="centered", page_icon="🪣", page_title="Churn Predictor")

st.title(" Churn Predictor 🚶‍♂️🚶‍♀️🚶")
st.subheader('This app predict wether customer will stay or go')

image = Image.open('CustomerChurn.png')
st.image(image, use_column_width=True)
########################################################################################################################

Demo, Account = st.columns(2)
with Demo:
    st.header("Demographic Information")
    gender = st.selectbox("Select customer gender", ['Male', 'Female'])
    Partner = st.selectbox("Does the customer have partner?", ['No', 'Yes'])
    SeniorCitizen = st.selectbox("Is customer senior citizen? (0 for No, 1 for Yes)", [0, 1])
    Dependents = st.selectbox("Does the customer have any dependents?", ['No', 'Yes'])

with Account:
    st.header("Customer Account Information")
    tenure = st.number_input('How long have the customer stayed with us? (in months)', min_value=0, step=1)
    Contract = st.selectbox("Select Customer Contract Type?", ['Month-to-month', 'One year', 'Two year'])
    PaperlessBilling = st.selectbox("Does the Customer Choose Paperless Billings?", ['No', 'Yes'])
    PaymentMethod = st.selectbox("Choose Customer Payment Method", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])

########################################################################################################################


st.header("Service Information")
MultipleLines = st.selectbox("Does the Customer have Multiple Phone Lines?", ['No phone service', 'No', 'Yes'])
InternetService = st.selectbox("Does the Customer Subscribe to Internet Service?", ['No', 'DSL', 'Fiber optic'])
if InternetService == 'No':
    OnlineSecurity = st.selectbox("Does the customer have Online Security?", ['No internet service'])
    OnlineBackup = st.selectbox("Does the customer have Online Backup?", ['No internet service'])
    DeviceProtection = st.selectbox("Does the customer have their device protected?", ['No internet service'])
    TechSupport = st.selectbox("Does the customer have Tech Support?", ['No internet service'])
    StreamingMovies = st.selectbox("Does the customer have subscribed to Movie Streaming?", ['No internet service'])
else:
    OnlineSecurity = st.selectbox("Does the customer have Online Security?", ['No', 'Yes'])
    OnlineBackup = st.selectbox("Does the customer have Online Backup?", ['No', 'Yes'])
    DeviceProtection = st.selectbox("Does the customer have their device protected?", ['No', 'Yes'])
    TechSupport = st.selectbox("Does the customer have Tech Support?", ['No', 'Yes'])
    StreamingMovies = st.selectbox("Does the customer have subscribed to Movie Streaming?", ['No', 'Yes'])

########################################################################################################################

# inference
data = {
    'tenure' : tenure,
    'gender' : gender,
    'SeniorCitizen' : SeniorCitizen,
    'Partner' : Partner,
    'Dependents' : Dependents,
    'MultipleLines' : MultipleLines,
    'InternetService' : InternetService,
    'OnlineSecurity' : OnlineSecurity,
    'OnlineBackup' : OnlineBackup,
    'DeviceProtection' : DeviceProtection,
    'TechSupport' : TechSupport,
    'StreamingMovies' : StreamingMovies,
    'Contract' : Contract,
    'PaperlessBilling' : PaperlessBilling,
    'PaymentMethod' : PaymentMethod
    }

URL = "https://kamil-ftds-009-p2m1.herokuapp.com/predict"

########################################################################################################################

# Communication
r = requests.post(URL, json=data)

Predict =  st.button('Predict Customer Churn')
if Predict:

    res = r.json()

    if res['code'] == 200:
        st.balloons()
        st.title('The customer churned or not? :')
        st.title(res['result']['description'])
    else:
        st.write("Whoops, something went wrong")
        st.write(f"description : {res['result']['error_msg']}")