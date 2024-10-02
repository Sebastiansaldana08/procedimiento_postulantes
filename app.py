import streamlit as st
import pandas as pd
import os
import base64
from io import BytesIO
from itertools import product

# Configuración de la página
st.set_page_config(initial_sidebar_state='collapsed', page_title="Sistema de Evaluación de Postulantes - UPCH", page_icon=":mortar_board:")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cargar el logo y convertir a base64
logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-upch.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
else:
    encoded_logo = None

# Usar HTML para el título y el logo
if encoded_logo:
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{encoded_logo}" width="80" style="margin-right: 20px;">
            <h1 style="margin: 0; font-size: 1.8em;">Calificación de Examen de Admisión - UPCH</h1>
        </div>
        """, unsafe_allow_html=True)
else:
    st.title('Calificación de Examen de Admisión - UPCH')

# Crear archivos de ejemplo para exportar
def crear_ejemplo_aciertos():
    df = pd.DataFrame({
        "pos_codigo": [],
        "tipo_documento": [],
        "per_num_doc": [],
        "per_apellido_pat": [],
        "per_apellido_mat": [],
        "pri_nombre": [],
        "seg_nombre": [],
        "periodo": [],
        "modalidad": [],
        "convocatoria": [],
        "facultad": [],
        "programa": [],
        "email": [],
        "telef_fijo": [],
        "celular": [],
        "rv": [],
        "cult": [],
        "rm": [],
        "total_aptitud": [],
        "biologia": [],
        "fisica": [],
        "maths": [],
        "quimica": [],
        "total_conocimiento": [],
        "nota_entre": [],
        "nota": []
    })
    return df

def crear_ejemplo_preseleccionados():
    df = pd.DataFrame({
        "N°": [],
        "MODALIDAD": [],
        "per_num_doc": [],
        "APELLIDOS Y NOMBRES": [],
        "REGIÓN": [],
        "PUNTAJE ENP": [],
        "CONDICIONES PRIORIZABLES": [],
        "PUNTAJE FINAL": [],
        "RESULTADO": []
    })
    return df

def crear_ejemplo_entrevista():
    df = pd.DataFrame({
        "pos_codigo": [],
        "tipo_documento": [],
        "per_num_doc": [],
        "per_apellido_pat": [],
        "per_apellido_mat": [],
        "pri_nombre": [],
        "seg_nombre": [],
        "periodo": [],
        "modalidad": [],
        "convocatoria": [],
        "facultad": [],
        "programa": [],
        "email": [],
        "telef_fijo": [],
        "celular": [],
        "rv": [],
        "cult": [],
        "rm": [],
        "total_aptitud": [],
        "biologia": [],
        "fisica": [],
        "maths": [],
        "quimica": [],
        "total_conocimiento": [],
        "nota_entre": [],
        "nota": []
    })
    return df

# Función para crear el archivo de descarga en formato Excel
def crear_download_link_excel(df, filename, text):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Descripción de la aplicación
st.markdown("""
    <div style="text-align: justify; font-size: 1.2em;">
        <h2 style="font-size: 1.3em;"><strong>Modalidad de Evaluación</strong></h2>
        <p>Este sistema está diseñado para procesar los aciertos de los postulantes en el examen de admisión a fin de poder determinar puntajes y orden de mérito por modalidad de admisión, carrera y periodo, determinando su elegibilidad para entrevistas y su estado final en el proceso de admisión.</p>
        <p><strong>Para utilizar el aplicativo, siga los siguientes pasos:</strong></p>
        <ol>
            <li>Cargue los archivos de Excel correspondientes en cada sección.</li>
            <li>Verifique los resultados obtenidos después del procesamiento.</li>
            <li>Descargue los resultados procesados para su análisis y seguimiento.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Exportables
st.markdown("### Exportables de Formatos de Archivos")
st.markdown("Descargue los formatos de los archivos que deben ser adjuntados:")

# Exportar ejemplo de aciertos en Excel
ejemplo_aciertos = crear_ejemplo_aciertos()
st.markdown(crear_download_link_excel(ejemplo_aciertos, "formato_aciertos.xlsx", "Descargar formato de aciertos"), unsafe_allow_html=True)

# Exportar ejemplo de preseleccionados en Excel
ejemplo_preseleccionados = crear_ejemplo_preseleccionados()
st.markdown(crear_download_link_excel(ejemplo_preseleccionados, "formato_preseleccionados.xlsx", "Descargar formato de preseleccionados"), unsafe_allow_html=True)

# Exportar ejemplo de entrevista en Excel
ejemplo_entrevista = crear_ejemplo_entrevista()
st.markdown(crear_download_link_excel(ejemplo_entrevista, "formato_entrevista.xlsx", "Descargar formato de entrevista"), unsafe_allow_html=True)

# Sección ESTADO_1
st.header('Sección ESTADO_1 (ESTADO INTERMEDIO)')
uploaded_file_1 = st.file_uploader("Cargar archivo Excel de aciertos:", type=["xlsx"], key="estado1_aciertos")
uploaded_file_2 = st.file_uploader("Cargar archivo Excel de preseleccionados:", type=["xlsx"], key="estado1_preseleccionados")

if st.button('Procesar ESTADO_1'):
    if uploaded_file_1 and uploaded_file_2:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file_1.name)
        preseleccionados_path = os.path.join(UPLOAD_FOLDER, uploaded_file_2.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file_1.getbuffer())
        with open(preseleccionados_path, "wb") as f:
            f.write(uploaded_file_2.getbuffer())
        
        datos = cargar_datos(file_path)
        preseleccionados_df = pd.read_excel(preseleccionados_path)
        preseleccionados = preseleccionados_df['per_num_doc'].astype(str).tolist()

        resultados = []
        for periodo, df in datos.items():
            df['per_num_doc'] = df['per_num_doc'].astype(str)
            df['pos_codigo'] = df['pos_codigo'].astype(str).str.zfill(8)
            df = calcular_notas(df)
            df['periodo'] = periodo

            modalidades = df['modalidad'].unique()
            programas = df['programa'].unique()
            combinaciones = list(product([periodo], modalidades, programas))

            for (periodo, modalidad, programa) in combinaciones:
                df_filtro = df[(df['modalidad'] == modalidad) & (df['programa'] == programa)]
                if not df_filtro.empty:
                    promedio_decil, decil = calcular_promedio_decil(df_filtro, programa)
                    df_filtro['PROMEDIO_DECIL'] = promedio_decil
                    df_filtro['DECIL'] = decil
                    df_filtro = determinar_estado_1(df_filtro, decil)
                    df_filtro = calcular_merito(df_filtro, 'NOTA_EXAMEN80')
                    resultados.append(df_filtro)

        resultado_final = pd.concat(resultados, ignore_index=True)
        columnas_orden = [
            'NOTA_APT', 'NOTA_CON', 'NOTA_EXAMEN100', 'NOTA_EXAMEN80', 'MERITO_NOTA_EXAMEN80',
            'PROMEDIO_DECIL', 'DECIL', 'ESTADO_1'
        ]
        otras_columnas = [col for col in resultado_final.columns if col not in columnas_orden]
        resultado_final = resultado_final[otras_columnas + columnas_orden]

        st.write(resultado_final)
        output_file = os.path.join(UPLOAD_FOLDER, 'resultado_estado1.xlsx')
        resultado_final.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="Descargar resultado ESTADO_1",
                data=f,
                file_name="resultado_estado1.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Sección ESTADO_2
st.header('Sección ESTADO_2 (ESTADO FINAL)')
uploaded_file_3 = st.file_uploader("Cargar archivo Excel de aciertos con notas de entrevista:", type=["xlsx"], key="estado2_aciertos")

if st.button('Procesar ESTADO_2'):
    if uploaded_file_3:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file_3.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file_3.getbuffer())

        datos = cargar_datos(file_path)
        preseleccionados_path = os.path.join(UPLOAD_FOLDER, uploaded_file_2.name)  # Usar archivo preseleccionados del estado 1
        if not os.path.exists(preseleccionados_path):
            st.error('Debe procesar primero los datos en la sección ESTADO_1.')
        else:
            preseleccionados_df = pd.read_excel(preseleccionados_path)
            preseleccionados = preseleccionados_df['per_num_doc'].astype(str).tolist()

            resultados = []
            for periodo, df in datos.items():
                df['per_num_doc'] = df['per_num_doc'].astype(str)
                df['pos_codigo'] = df['pos_codigo'].astype(str).str.zfill(8)
                df = calcular_notas(df)

                modalidades = df['modalidad'].unique()
                programas = df['programa'].unique()
                combinaciones = list(product([periodo], modalidades, programas))

                for (periodo, modalidad, programa) in combinaciones:
                    df_filtro = df[(df['modalidad'] == modalidad) & (df['programa'] == programa)]
                    if not df_filtro.empty:
                        promedio_decil, decil = calcular_promedio_decil(df_filtro, programa)
                        df_filtro['PROMEDIO_DECIL'] = promedio_decil
                        df_filtro['DECIL'] = decil
                        df_filtro = determinar_estado_1(df_filtro, decil)
                        df_filtro = calcular_merito(df_filtro, 'NOTA_EXAMEN80')

                        df_filtro['NOTA_FINAL'] = df_filtro['NOTA_EXAMEN80'] + df_filtro['nota_entre']
                        df_filtro = calcular_merito(df_filtro, 'NOTA_FINAL')

                        df_filtro = determinar_estado_2(df_filtro, preseleccionados)
                        df_filtro = determinar_pronabec_preseleccionado(df_filtro, preseleccionados)
                        resultados.append(df_filtro)

            resultado_final = pd.concat(resultados, ignore_index=True)
            columnas_orden = [
                'NOTA_APT', 'NOTA_CON', 'NOTA_EXAMEN100', 'NOTA_EXAMEN80', 'MERITO_NOTA_EXAMEN80',
                'NOTA_FINAL', 'MERITO_NOTA_FINAL', 'PROMEDIO_DECIL', 'DECIL',
                'ESTADO_1', 'ESTADO_2', 'pronabec PRESELECCIONADO'
            ]
            otras_columnas = [col for col in resultado_final.columns if col not in columnas_orden]
            resultado_final = resultado_final[otras_columnas + columnas_orden]

            st.write(resultado_final)
            output_file = os.path.join(UPLOAD_FOLDER, 'resultado_estado2.xlsx')
            resultado_final.to_excel(output_file, index=False)

            with open(output_file, "rb") as f:
                st.download_button(
                    label="Descargar resultado ESTADO_2",
                    data=f,
                    file_name="resultado_estado2.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
