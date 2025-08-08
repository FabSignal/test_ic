# test_ic

Este proyecto es una aplicación web desarrollada con Streamlit que permite evaluar a estudiantes mediante un formulario interactivo. Las respuestas se procesan automáticamente y los resultados se almacenan en una hoja de cálculo de Google Sheets para su posterior análisis.

## 🚀 Funcionalidades

- Formulario de evaluación con selección múltiple.
- Corrección automática de respuestas.
- Registro del nombre del evaluado, fecha, hora y cantidad de respuestas incorrectas.
- Almacenamiento de resultados en Google Sheets.
- Interfaz simple, accesible desde cualquier dispositivo.

## 🛠️ Tecnologías

- [Streamlit](https://streamlit.io/)
- [Python 3.10+](https://www.python.org/)
- [gspread](https://gspread.readthedocs.io/) + Google Sheets API
- [pandas](https://pandas.pydata.org/)

## ▶️ Cómo ejecutarlo localmente

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/test_ic.git
   cd test_ic
   ```

2. Instala las dependencias:
    ```bash

   pip install -r requirements.txt

   ```

3. Ejecutá la app:

   ```
   streamlit run main.py

   ```

Asegurate de tener configuradas tus credenciales de Google Sheets (service_account.json) y de compartir la hoja con el correo de servicio.

## ☁️ Despliegue en Streamlit Cloud
1. Subí este repositorio a GitHub.

2. Ingresá a https://streamlit.io/cloud y conectá tu cuenta de GitHub.

3. Seleccioná el archivo main.py como punto de entrada.

4. Definí las variables de entorno si es necesario (por ejemplo, claves de acceso si usás Google Drive API).

5. Compartí el link público con los estudiantes.

## 📁 Estructura del proyecto

```
test_ic/
│
├── main.py                  # App principal de Streamlit
├── requirements.txt         # Librerías necesarias
└── README.md

```


## 🔒 Importante
Este repositorio es privado. No compartir las credenciales (service_account.json) públicamente.

