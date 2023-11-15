# app.py
import streamlit as st
from recommender import get_recommendations_by_pairings_gender_and_ses

st.title('Recomendador de Vinos')

# Formulario de entrada para los parámetros de recomendación
with st.form('input_form'):
    pairing_inputs = st.multiselect('Seleccione los maridajes:', ['Cheddar','Gruyere','Brie','Feta','Stilton','Gouda','Comte','Camembert','Cotija','Queso Azul','Colby','Provolone','Epoisses','Queso Fresco','Roquefort','Ossau-Iraty','Edamental','Burrata','Halloumi','Gorgonzola','Muenster','Mozzarela','Delicede Bougorgne','Mizithra','Brie','Carne de Res','Scamorza','Gruyere','Crema Agria','Pollo','Cordero','Cheddar','Queso Crema','Cerdo','Venado','Ricotta','Chuleta','Judía Pinta','Havarti','Tofu','Frijoles Negos','Chevre','Seitan','Frijoles Blancos','Cottage','Salami','Lenteja','Parmesano','Langosta','Cebolla','Tocineta','Cilantro','GradaPadano','Cangrejo','Ajo','Charcuteria','Comino','Pecorino','Camarones','Chalota','Jamon','Curcuma','Asiago','Hongos','Batata','Manchego','Zanahoria','Calabaza','Nabo','Zapallo','Menta','Basil','Cebollin','Shiso','Perejil','Almeja','Barbecue','Halibut','Pimiento','Ostra','Teriyaki','Bacalao','Tomate','Vieira','Vinagreta','Salmon','Berenjena','Marinado','Bass','Guisantes','Trucha','Col','Lechuga','Palta','Aguacate','Oregano','Escarola','Tomillo','Pimiento Verde','Eneldo','Anis','Cardamomo','Gengibre','Canela','Albahaca','Pimienta','Vainilla','Clavo','Fenogreco','Nuez Moscada','Cayena','Mejorana','Pimenton','Chipotle'])
    gender_input = st.selectbox('Género', ['HOMBRE', 'MUJER'])
    age_input = st.selectbox('Rango de Edad', ['25-34', '35-44', '45-54', '55-75'])
    ses_input = st.selectbox('NSE', ['ABC1', 'C2', 'C3', 'D/E'])
    submit_button = st.form_submit_button('Obtener Recomendaciones')

if submit_button:
    recommendations = get_recommendations_by_pairings_gender_and_ses(pairing_inputs, gender_input, ses_input, age_input)
    if recommendations:
        st.write('Recomendaciones:', recommendations)
    else:
        st.write('No se encontraron recomendaciones.')