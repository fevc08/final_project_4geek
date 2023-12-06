import streamlit as st
from pickle import load
import numpy as np
import pandas as pd
import os

# Load the model
dt_wine_best = load(open("../models_fidel/dt_wine_best.pkl", "rb"))

# Load label encoders
with open('../models_fidel/label_encoders.pkl', 'rb') as f:
    label_encoders = load(f)
    
ordinal_mapping = {'18-24': 1, '25-34': 2, '35-44': 3, '45-54': 4, '55+': 5}

wine_data = pd.read_csv("wine_data.csv")

st.title('Wine Recommendation App')

# Create input widgets for user input
edad = st.selectbox('¿En cuál rango de edad te encuentras?', ["18-24", "25-34", "35-44", "45-54", "55+"])
genero = st.selectbox('Seleciona tu género:', label_encoders['genero'])
precio = st.slider('¿Cuanto tienes presupuestado para esta compra de vinos?', 4000, 25000)
maridajes = st.multiselect('¿Con qué deseas maridar este vino?', label_encoders['maridaje'])
categorias = st.multiselect('Selecciona el tipo de vino que más te gusta:', label_encoders['categorias'])

# Encode user inputs using label encoders
edad_n = ordinal_mapping[edad]
genero_n = np.where(label_encoders['genero'] == genero)[0][0]

# Initialize a set to store unique predictions
unique_predictions = set()

# Make predictions for each selected combination of 'maridaje' and 'categorias'
if st.button('Recomendar'):
    for categoria in categorias:
        categoria_n = np.where(label_encoders['categorias'] == categoria)[0][0]
            
        for maridaje in maridajes:
            maridaje_n = np.where(label_encoders['maridaje'] == maridaje)[0][0]
        
            # Make a prediction
            prediction = dt_wine_best.predict([[categoria_n, precio, maridaje_n, genero_n, edad_n]])
            
            # Add the prediction to the set
            unique_predictions.add(label_encoders["productos"][prediction[0]])

st.subheader('Las mejores opciones para tu maridaje son:')
for i, prediction in enumerate(unique_predictions):
    # Get the image URL corresponding to the product
    image_url = wine_data.loc[wine_data['productos'] == prediction, 'url_imagen'].values[0]
    
    # Display the product name and image with a specific width
    st.write(f'Opción {i + 1}: {prediction}')
    st.image(image_url, width=100)