import streamlit as st
import pandas as pd
import sqlite3
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load the trained model
model_path = "../models_fidel/best_knn.plk"
knn_model = joblib.load(model_path)

# Function to preprocess input data
def preprocess_input(data):
    # Your preprocessing steps here
    one_hot_encoder = OneHotEncoder(sparse=False)
    categorical_columns = ['product_category', 'gender']
    pairing_encoded_df = pd.DataFrame(one_hot_encoder.fit_transform(data[categorical_columns]))
    pairing_encoded_df.columns = one_hot_encoder.get_feature_names_out(categorical_columns)

    scaler = MinMaxScaler()
    numeric_columns = ['price', 'age']
    data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

    data = pd.concat([data, pairing_encoded_df], axis=1).drop(categorical_columns, axis=1)
    data = data.dropna()

    return data

# Streamlit app
# Dataframe pairing
con = sqlite3.connect("../data_fidel/interim/wine_products.db")

query = "SELECT * FROM pairing;"

pairing_df = pd.read_sql_query(query, con=con)
con.close()

# Dataframe paring_agrupado
pairing_df_agrupado = pd.read_csv("../data_fidel/processed/paring_agrupado.csv")

def main():
    st.title("Wine Recommender App")

    # Get user input
    product_category = st.selectbox("Select product category:", ["Category_A", "Category_B", "Category_C"])
    price = st.slider("Select price:", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
    age = st.slider("Select age:", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
    gender = st.selectbox("Select gender:", ["Male", "Female"])

    # Create a DataFrame with user input
    user_data = pd.DataFrame({
        'product_category': [product_category],
        'price': [price],
        'age': [age],
        'gender': [gender],
    })

    # Preprocess user input
    user_data_processed = preprocess_input(user_data)

    # Make predictions
    prediction = knn_model.predict(user_data_processed)

    # Display recommended product_name and corresponding image_url
    recommended_product_name = prediction[0]
    recommended_product_row = pairing_df_agrupado[pairing_df_agrupado['product_name'] == recommended_product_name].iloc[0]
    recommended_image_url = pairing_df[pairing_df['product_name'] == recommended_product_name]['image_url'].iloc[0]

    st.subheader("Recommended Wine:")
    st.write(recommended_product_name)

    # Display the image
    st.image(recommended_image_url, caption='Recommended Wine Image', use_column_width=True)

if __name__ == "__main__":
    main()
