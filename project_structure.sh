#!/bin/bash

# Crear directorios principales
mkdir -p app/{static,templates}
mkdir -p data/{raw,processed}
mkdir -p docs
mkdir -p models
mkdir -p notebooks
mkdir -p tests
mkdir -p .github/workflows

# Crear archivos iniciales
touch app/__init__.py app/main.py app/models.py app/views.py
touch data/README.md docs/installation.md docs/usage.md docs/api.md docs/README.md
touch models/train.py models/evaluate.py
touch notebooks/eda.ipynb notebooks/preprocessing.ipynb notebooks/examples.ipynb
touch tests/test_app.py tests/test_model.py tests/conftest.py
touch .github/ISSUE_TEMPLATE.md .github/workflows/ci.yml
touch .gitignore README.md requirements.txt environment.yml project_structure.sh Procfile

# Mensaje de finalización
echo "Project structure created"

# Opcional: Inicializar un repositorio Git
git add .
git commit -m "Repositorio estructurado"
echo "Repositorio Git actualizado."
cd 'C:/Users/fevc_/c18-61-m-data-bi'