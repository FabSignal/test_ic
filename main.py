import streamlit as st
import pandas as pd
from datetime import datetime
import os
import locale
import gspread
from google.oauth2.service_account import Credentials

def enviar_a_google_sheets(resultado):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_dict = {
        "type": st.secrets["gcp_service_account"]["type"],
        "project_id": st.secrets["gcp_service_account"]["project_id"],
        "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
        "private_key": st.secrets["gcp_service_account"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["gcp_service_account"]["client_email"],
        "client_id": st.secrets["gcp_service_account"]["client_id"],
        "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
        "token_uri": st.secrets["gcp_service_account"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
    }
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(credentials)

    # Abre la hoja de cálculo
    sh = gc.open("resultados_test_ic")
    worksheet = sh.worksheet("Respuestas")

    # Agrega los datos
    worksheet.append_row([
        resultado["nombre"],
        resultado["evaluacion"],
        resultado["puntaje"],
        resultado["fecha"],
        resultado["hora"]
    ])

# Configurar locale para poder parsear meses en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Linux/macOS
except:
    locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Windows

# Inicializar el nombre en el estado de sesión si no existe
if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if not st.session_state.nombre:
    st.title("Identificación del Usuario")
    nombre_input = st.text_input("Por favor, ingrese su nombre para comenzar:")
    if st.button("Ingresar") and nombre_input.strip():
        st.session_state.nombre = nombre_input.strip()
        st.experimental_set_query_params(started="1")
        st.rerun()
else:
    st.title("Test IC")
    st.markdown(f"**Participante:** {st.session_state.nombre}")

    st.markdown("""
    **Instrucciones:**  
    1. Marque en la **columna 1** a la altura de cada seguro de incendios o accidentes, desde 150.000 a 450.000 pesos inclusive, contratado entre el 15 de marzo de 1975 y el 10 mayo de 1976.  
    2. Marque en la **columna 2** a la altura de cada seguro de vida o accidentes, hasta 300.000 pesos inclusive, contratado entre el 15 de octubre de 1975 y el 20 agosto de 1976.  
    3. Marque en la **columna 3** a la altura de cada seguro de incendios o de vida, desde 200.000 a 500.000 pesos inclusive, contratado entre el 10 de febrero de 1975 y el 15 de junio de 1976.  
    """)

    st.subheader("Complete las respuestas")

    # Encabezado visual de columnas
    header_cols = st.columns([2, 2, 2, 1, 1, 1])
    header_cols[0].markdown("**CANTIDAD ASEGURADA**")
    header_cols[1].markdown("**CLASES DE SEGURO**")
    header_cols[2].markdown("**FECHA**")
    header_cols[3].markdown("**1**")
    header_cols[4].markdown("**2**")
    header_cols[5].markdown("**3**")

    preguntas = [
        {"monto": 300000, "seguro": "Incendios", "fecha": "2 enero 1976"},
        {"monto": 100000, "seguro": "Vida", "fecha": "22 octubre 1975"},
        {"monto": 400000, "seguro": "Accidentes", "fecha": "14 septiembre 1975"},
        {"monto": 200000, "seguro": "Vida", "fecha": "13 noviembre 1976"},
        {"monto": 400000, "seguro": "Incendios", "fecha": "17 mayo 1976"},
        {"monto": 300000, "seguro": "Accidentes", "fecha": "12 octubre 1975"},
        {"monto": 500000, "seguro": "Vida", "fecha": "16 febrero 1976"},
        {"monto": 100000, "seguro": "Incendios", "fecha": "3 agosto 1976"},
        {"monto": 400000, "seguro": "Incendios", "fecha": "11 agosto 1976"},
        {"monto": 200000, "seguro": "Accidentes", "fecha": "21 mayo 1975"},
        {"monto": 500000, "seguro": "Vida", "fecha": "9 marzo 1975"},
        {"monto": 300000, "seguro": "Incendios", "fecha": "17 julio 1976"},
        {"monto": 100000, "seguro": "Accidentes", "fecha": "4 junio 1976"},
        {"monto": 100000, "seguro": "Vida", "fecha": "23 noviembre 1976"},
        {"monto": 500000, "seguro": "Vida", "fecha": "18 abril 1975"},
        {"monto": 200000, "seguro": "Accidentes", "fecha": "24 diciembre 1976"},
        {"monto": 500000, "seguro": "Accidentes", "fecha": "19 abril 1975"},
        {"monto": 200000, "seguro": "Vida", "fecha": "7 diciembre 1976"},
        {"monto": 400000, "seguro": "Incendios", "fecha": "25 mayo 1975"},
        {"monto": 300000, "seguro": "Accidentes", "fecha": "6 enero 1976"},
        {"monto": 500000, "seguro": "Vida", "fecha": "29 marzo 1975"},
        {"monto": 300000, "seguro": "Vida", "fecha": "28 junio 1975"},
        {"monto": 400000, "seguro": "Accidentes", "fecha": "8 febrero 1976"},
        {"monto": 100000, "seguro": "Incendios", "fecha": "27 julio 1975"},
        {"monto": 200000, "seguro": "Accidentes", "fecha": "21 enero 1976"},
    ]

    def respuesta_correcta(p):
        monto = p["monto"]
        tipo = p["seguro"]
        fecha = datetime.strptime(p["fecha"], "%d %B %Y")
        r1 = (tipo in ["Incendios", "Accidentes"] and
              150000 <= monto <= 450000 and
              datetime(1975, 3, 15) <= fecha <= datetime(1976, 5, 10))
        r2 = (tipo in ["Vida", "Accidentes"] and
              monto <= 300000 and
              datetime(1975, 10, 15) <= fecha <= datetime(1976, 8, 20))
        r3 = (tipo in ["Incendios", "Vida"] and
              200000 <= monto <= 500000 and
              datetime(1975, 2, 10) <= fecha <= datetime(1976, 6, 15))
        return [r1, r2, r3]

    respuestas = []
    for i, p in enumerate(preguntas):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 1, 1, 1])
        with col1:
            st.markdown(f"**{p['monto']:,} pesos**")
        with col2:
            st.markdown(f"**{p['seguro']}**")
        with col3:
            st.markdown(f"**{p['fecha']}**")
        with col4:
            r1 = st.checkbox("", key=f"{i}_r1")
        with col5:
            r2 = st.checkbox("", key=f"{i}_r2")
        with col6:
            r3 = st.checkbox("", key=f"{i}_r3")
        respuestas.append([r1, r2, r3])

    # ✅ Este bloque debe ir FUERA del for
    if st.button("Enviar respuestas"):
        incorrectas = 0
        for i, p in enumerate(preguntas):
            correctas = respuesta_correcta(p)
            for j in range(3):
                if respuestas[i][j] != correctas[j]:
                    incorrectas += 1

        def evaluar(incorrectas):
            if incorrectas <= 1:
                return "Muy alto", 6
            elif incorrectas <= 4:
                return "Alto", 5
            elif incorrectas <= 7:
                return "Medio alto", 4
            elif incorrectas <= 12:
                return "Medio", 3
            elif incorrectas <= 17:
                return "Medio bajo", 2
            else:
                return "Bajo", 1

        evaluacion, puntuacion = evaluar(incorrectas)

        resultado = {
            "nombre": st.session_state.nombre,
            "evaluacion": evaluacion,
            "puntaje": puntuacion,
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.now().strftime("%H:%M:%S")
        }

        enviar_a_google_sheets(resultado)


        st.success(f"¡Gracias {st.session_state.nombre}! Respuestas enviadas correctamente.")
        #st.info(f"Evaluación: **{evaluacion}**, Puntaje estándar: **{puntuacion}**")
