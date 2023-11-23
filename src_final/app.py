import streamlit as st
import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Function to load data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"Error: File not found at {file_path}")
        st.stop()  # Stop the script if the file is not found
    return pd.read_csv(file_path)

# Load the trained model and scaler
model_path = "../models_final/best_knn.pkl"
knn_model = joblib.load(model_path)


# Load pairing data
data_folder = os.path.join(os.path.dirname(__file__), 'data_final/processed/')
pairing_df = load_data(os.path.join(data_folder, 'pairing.csv'))

# Codificación One-Hot para variables categóricas
one_hot_encoder = OneHotEncoder(sparse=False)
categorical_columns = ['product_category', 'gender', 'age']
pairing_encoded_df = pd.DataFrame(one_hot_encoder.fit_transform(pairing_df[categorical_columns]))
pairing_encoded_df.columns = one_hot_encoder.get_feature_names_out(categorical_columns)

# Normalización de variables numéricas
scaler = MinMaxScaler()
numeric_columns = ['price']
pairing_df[numeric_columns] = scaler.fit_transform(pairing_df[numeric_columns])

# Combinar las columnas codificadas y normalizadas
pairing_df = pd.concat([pairing_df, pairing_encoded_df], axis=1).drop(categorical_columns, axis=1)

# Limpieza final
pairing_df = pairing_df.dropna()

# Agrupar datos por nombre de producto y maridajes
pairing_agrupado_df = pairing_df.groupby('product_name')['pairing'].apply(lambda x: ', '.join(set(x))).reset_index()

# Recommendation function
def get_recommendations_by_pairings_gender_and_ses(pairing_inputs, gender_input, age_input, product_category_input, price_input, k=3):

    # Identificar las columnas 
    gender_column = f'gender_{gender_input}'
    age_column = f'age_{age_input}'
    category_column = f'product_category_{product_category_input}'
    price_column = 'price'

    # Verificar si las columnas existen
    if (
        gender_column not in pairing_df.columns or
        age_column not in pairing_df.columns or
        category_column not in pairing_df.columns or
        price_column not in pairing_df.columns
    ):
        return "Alguno de los atributos especificados no se encuentra disponible en los datos."

    # Pre-filtrado basado en maridajes, género, SES, product_category, y price
    df_filtrado = pairing_df[
        pairing_df['product_name'].isin(pairing_agrupado_df[pairing_agrupado_df['pairing'].apply(lambda x: all(pairing in x for pairing in pairing_inputs))]['product_name'])
    ]
    df_filtrado = df_filtrado[
        (df_filtrado[gender_column] == 1) &
        (df_filtrado[age_column] == 1) &
        (df_filtrado[category_column] == 1) &
        (df_filtrado[price_column] <= price_input)
    ]

    if df_filtrado.empty:
        return []

    # Inicializar el modelo k-NN
    knn = KNeighborsClassifier(n_neighbors=12, weights='uniform').fit(
        df_filtrado.drop(['product_name', 'pairing', 'image_url'], axis=1),
        df_filtrado['product_name']  # Replace 'target_column' with the actual column you're trying to predict
    )

    recommendations = []
    for product_name in df_filtrado['product_name'].unique():
        # Obtener las características del producto
        product_features = df_filtrado[df_filtrado['product_name'] == product_name].drop(['product_name', 'pairing', 'image_url'], axis=1)

        if not product_features.empty:
            # Utilizar la media de las características si hay múltiples filas para el mismo producto
            product_feature_avg = product_features.mean().values.reshape(1, -1)

            # Obtener recomendaciones utilizando k-NN
            predicted_rating = knn.predict(product_feature_avg)
            recommendations.append((product_name, tuple(predicted_rating)))  # Convert NumPy array to tuple

    return list(set(recommendations))  # Eliminar duplicados

# Streamlit app
st.title('Recomendador de Vinos')

# Input form
with st.form('input_form'):
    pairing_inputs = st.multiselect('Seleccione los maridajes:', pairing_df["pairing"].unique())  # List of pairings
    category_input = st.selectbox("Select product category:", ["Tinto", "Blanco", "Espumoso"])
    price_input = st.slider("Seleccionar precio:", 0, 50000, 0, step=100)
    gender_input = st.selectbox('Género', ['HOMBRE', 'MUJER', 'OTRO'])
    age_input = st.selectbox('Rango de Edad', ['18-24', '25-34', '35-44', '45-54', '55-75'])
    submit_button = st.form_submit_button('Obtener Recomendaciones')

if submit_button:
    recommendations = get_recommendations_by_pairings_gender_and_ses(pairing_inputs, gender_input, age_input, category_input, price_input)
    if recommendations:
        st.write('Recomendaciones:')
        recommendations.sort(key=lambda x: x[1], reverse=True)
        top_recommendations = recommendations[:3]
        
        # Display recommendations
        num_products_per_row = 3
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
