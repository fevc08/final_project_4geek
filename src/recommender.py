# recommender.py
import sqlite3
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.neighbors import NearestNeighbors
import joblib

# Cargar del modelo entrenado
knn = joblib.load('../models/wine_pairing_recommendation_knn.joblib')

# Conexión a la base de datos
conn = sqlite3.connect('../data/wine_db.db')
query = "SELECT * FROM wine_database;"
df = pd.read_sql_query(query, conn)
conn.close()


# Filtrando las columnas relevantes
df = df[['product_name', 'price', 'pairing', 'gender', 'age', 'ses', 'rank']]

# Manejo de valores faltantes
imputer = SimpleImputer(strategy='most_frequent')
df[['gender', 'age', 'ses', 'rank']] = imputer.fit_transform(df[['gender', 'age', 'ses', 'rank']])

# Codificación One-Hot para variables categóricas
one_hot_encoder = OneHotEncoder(sparse=False)
categorical_columns = ['gender', 'ses', 'age']
df_encoded = pd.DataFrame(one_hot_encoder.fit_transform(df[categorical_columns]))
df_encoded.columns = one_hot_encoder.get_feature_names_out(categorical_columns)

# Normalización de variables numéricas
scaler = MinMaxScaler()
numeric_columns = ['price', 'rank']
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Combinar las columnas codificadas y normalizadas
df = pd.concat([df, df_encoded], axis=1).drop(categorical_columns, axis=1)

# Limpieza final
df = df.dropna()

# Agrupar datos por nombre de producto y maridajes
df_agrupado = df.groupby('product_name')['pairing'].apply(lambda x: ', '.join(set(x))).reset_index()

# Función de recomedación
def get_recommendations_by_pairings_gender_and_ses(pairing_inputs, gender_input, ses_input, age_input, k=5):
    # Identificar las columnas de género y SES después del one-hot encoding
    gender_column = f'gender_{gender_input}'
    ses_column = f'ses_{ses_input}'
    age_column = f'age_{age_input}'


    # Verificar si las columnas existen
    if gender_column not in df.columns or ses_column not in df.columns or age_column not in df.columns:
        return "Género, Rango etario o NSE especificado no se encuentra disponible en los datos."

    # Pre-filtrado basado en maridajes, género y SES
    df_filtrado = df[df['product_name'].isin(df_agrupado[df_agrupado['pairing'].apply(lambda x: all(pairing in x for pairing in pairing_inputs))]['product_name'])]
    df_filtrado = df_filtrado[(df_filtrado[gender_column] == 1) & (df_filtrado[ses_column] == 1) & (df_filtrado[age_column] == 1)]

    if df_filtrado.empty:
        return []

    # Inicializar el modelo k-NN
    knn = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(df_filtrado.drop(['product_name', 'pairing'], axis=1))

    recommendations = []
    for product_name in df_filtrado['product_name'].unique():
        # Obtener las características del producto
        product_features = df_filtrado[df_filtrado['product_name'] == product_name].drop(['product_name', 'pairing'], axis=1)

        if not product_features.empty:
            # Utilizar la media de las características si hay múltiples filas para el mismo producto
            product_feature_avg = product_features.mean().values.reshape(1, -1)

            # Obtener recomendaciones utilizando k-NN
            distances, indices = knn.kneighbors(product_feature_avg, n_neighbors=k)
            for idx in indices[0]:
                recommended_product_name = df_filtrado.iloc[idx]['product_name']
                recommendations.append(recommended_product_name)

    return list(set(recommendations))  # Eliminar duplicados