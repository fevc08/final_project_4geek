# **Wine Pairing Recommender App**

## **Introducción**
En Chile, se ha registrado un incremento de consumo de vino pasando de un 15 litros a 22 litros per capita. Esto es atribuido a muchos factores, entre ellos la pandemia y además el crecimiento del enoturismo en el país despues de la pandemia. De esta forma, los consumidores cada vez se adentran más a la cultura del vino y buscan de diferentes forma aprender sobre ello y conocer más sobre los vinos que esta consumiendo.
Una de las principales preguntas en el mercado es ¿Con cuál vino puedo acompañar mi comida?, y en un restaurant es muy fácil que un Sommelier conteste a esta pregunta y puedas acompañar tu comida con un vino que te haga disfrutar de ese momento. Pero, ¿Qué pasa en el caso de estar en tu casa y no tienes acceso a un sommelier o algun otro experto en el área?, y deseas disfrutar de tu comida con un buen vino.
Para esos momento, se pensó está aplicación, para ofrecer a muchos la opción de poder obtener un vino que los acompañe en esas cenas y momentos donde degustar y comer sean las principales actividades.

## **Estructura del Proyecto**
- `app/`: Aplicación Flask
- `data/`: Datos crudos y preprocesados
- `docs/`: Documentación del proyecto
- `models/`: Modelos de Machine Learning y scripts de entrenamiento
- `notebooks/`: Notebooks de análisis y ejemplos
- `tests/`: Pruebas unitarias
- `.github/`: Configuración de GitHub Actions y plantillas de issues

## **Recolección de la Data**
Entre muchas páginas de que visitamos la CAV era una de las cuales poseia la mayor cantidad de datos vinos Chilenos que se encuentran en el mercado, para lo cual empleamos el uso de Web Scraping con Python, empleando librerias como Selenium y BeautifulSoup. Esto lo hizimos en dos pasos donde primero extragimos las urls de cada uno de los vinmos que encontramos en la tienda y un segundo paso en donde extrajimos uno a uno la información que requeriamos de cada uno de los vinos.

## **Algoritmo Empleado**
Para este trabajo, empleamos K-Nearest Neighbor (knn), para clasificar cada uno de los vinos encontrados, según el mejor maridaje para cada uno, dependiendo de otras variables como categoria (Blanco, Tinto o Espumoso), genero, precio y edad. Para ello empleamos la libreria Scikit-Learn.

![scikit-learn](https://scikit-learn.org/stable/_static/scikit-learn-logo-small.png)

## **Demo**
- *Versión 1:* https://wine-pairing-recommender.onrender.com/
- *Versión 2:* https://wine-n7jy.onrender.com
- +Versión 3:* https://wine-app-recommender.onrender.com

## **Instalación**
Ver [installation.md](docs/installation.md) para más detalles.

## **Uso**
Ver [usage.md](docs/usage.md) para más detalles.

## **Contribución**
Ver [CONTRIBUTING.md](docs/contributing.md) para más detalles.
