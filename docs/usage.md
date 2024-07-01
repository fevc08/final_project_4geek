# usage.md

# Guía de Uso

## Ejecutar la Aplicación
1. Asegúrate de que el entorno virtual esté activado:
    ```bash
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

2. Ejecuta la aplicación:
    ```bash
    flask run
    ```

3. Abre tu navegador web y ve a `http://127.0.0.1:5000`.

## Ejemplos de Uso
1. **Endpoint para predecir**:
    ```bash
    curl -X POST http://127.0.0.1:5000/predict -d '{"input": "value"}' -H "Content-Type: application/json"
    ```

2. **Interfaz Web**:
    - Navega a la página principal y utiliza la interfaz para realizar predicciones.

## Ejecutar el Script de Web Scraping
1. Asegúrate de que el entorno virtual esté activado:
    ```bash
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

2. Ejecuta el script de web scraping:
    ```bash
    python scripts/web_scraping.py
    ```

3. Los datos se guardarán en `data/raw/datos_scrapeados.csv`.