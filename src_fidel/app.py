import streamlit as st
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Function to load data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"Error: File not found at {file_path}")
        st.stop()  # Stop the script if the file is not found
    return pd.read_csv(file_path)

# Load the trained model and scaler
model_path = "../models_fidel/best_knn.plk"
knn_model = joblib.load(model_path)
scaler = joblib.load('../models_fidel/scaler.pkl')

# Load pairing data
data_folder = os.path.join(os.path.dirname(__file__), 'data_fidel/processed/')
pairing_df = load_data(os.path.join(data_folder, 'pairing_df.csv'))
pairing_agrupado_df = load_data(os.path.join(data_folder, 'paring_agrupado.csv'))

# Recommendation function
def get_recommendations(pairing_inputs, category_input, price_input, gender_input, age_input):
    # Inverse transform age and price
    scaled_age = scaler.fit_transform([[age_input]])
    scaled_price = scaler.fit_transform([[price_input]])

    # Identify columns
    category_column = f'category_{category_input}'
    price_column = f'price_{scaled_price[0][0]}'
    gender_column = f'gender_{gender_input}'
    age_column = f'age_{scaled_age[0][0]}'

    # Check if columns exist
    if not all(col in pairing_df.columns for col in [category_column, price_column, gender_column, age_column]):
        return "Lo sentimos, no encontramos el vino perfecto para ti"

    # Pre-filter based on pairings, gender, and SES
    filtered_df = pairing_df[
        pairing_df['product_name'].isin(
            pairing_agrupado_df[
                pairing_agrupado_df['pairing'].apply(lambda x: all(pairing in x for pairing in pairing_inputs))
            ]['product_name']
        )
    ]
    filtered_df = filtered_df[(filtered_df[gender_column] == 1) & (filtered_df[age_column] == 1)]

    if filtered_df.empty:
        return []

    recommendations = []
    for product_name in filtered_df['product_name'].unique():
        product_features = filtered_df[filtered_df['product_name'] == product_name].drop(
            ['product_name', 'pairing', 'image_url'], axis=1
        )

        if not product_features.empty:
            product_feature_avg = product_features.mean().values.reshape(1, -1)
            distances, indices = knn_model.kneighbors(product_feature_avg)
            for idx in indices[0]:
                recommended_product = filtered_df.iloc[idx]
                recommended_product_name = recommended_product['product_name']
                recommended_image_url = recommended_product['image_url']
                recommendations.append((recommended_product_name, recommended_image_url))

    return list(set(recommendations))

# Streamlit app
st.title('Recomendador de Vinos')

# Input form
with st.form('input_form'):
    pairing_inputs = st.multiselect('Seleccione los maridajes:', pairing_df["pairing"].unique().values())  # List of pairings
    category_input = st.selectbox("Select product category:", ["Tinto", "Blanco", "Espumoso"])
    price_input = st.slider("Select price:", 0, 100000, 0, step=0)
    gender_input = st.selectbox('Género', ['HOMBRE', 'MUJER', 'OTRO'])
    age_input = st.slider("Edad:", 18.0, 75.0, 18.0, step=0.5)
    submit_button = st.form_submit_button('Obtener Recomendaciones')

if submit_button:
    recommendations = get_recommendations(pairing_inputs, category_input, price_input, gender_input, age_input)
    if recommendations:
        st.write('Recomendaciones:')
        recommendations.sort(key=lambda x: x[1], reverse=True)
        top_recommendations = recommendations[:3]
        
        # Display recommendations
        num_products_per_row = 5
        num_recommendations = len(top_recommendations)
        cols = st.columns(num_products_per_row)
        for i in range(0, num_recommendations, num_products_per_row):
            for j in range(num_products_per_row):
                idx = i + j
                if idx < num_recommendations:
                    product_name, image_url = top_recommendations[idx]
                    col = cols[j]
                    
                    # Center image vertically using HTML
                    with col:
                        col.markdown(f'<p style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;"><img src="{image_url}" alt="{product_name}" style="max-height: 200px;">{product_name}</p>', unsafe_allow_html=True)
    else:
        st.write('No se encontraron recomendaciones.')
