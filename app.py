import streamlit as st
import pandas as pd
import sweetviz as sv

# Titolo dell'applicazione
st.set_page_config(page_title="MAR Algorithm", page_icon="🧐")

# Titolo e logo dell'applicazione
st.image("https://i.ibb.co/g6k3gvC/mar-high-resolution-logo-4.png", width=200)
st.title("Interfaccia")

# STEP 1: Caricamento del Dataset
# ----------------------------------------

uploaded_file = st.file_uploader("Carica il tuo dataset (.csv, .txt, .xlsx)", type=["csv", "txt", "xlsx"])

def load_dataset(uploaded_file, delimiter=','):
    try:
        if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_file, delimiter=delimiter)  # Tentativo di auto-detection del delimitatore
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            return None
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {str(e)}")
        return None

if uploaded_file is not None:
    # Opzione per specificare il delimitatore
    delimiter = st.text_input("Inserisci il delimitatore (es. ',' o ';') se necessario", value=",")
    dataset = load_dataset(uploaded_file, delimiter)
    if dataset is not None:
        st.success(f"Dataset caricato con successo! Righe: {dataset.shape[0]}, Colonne: {dataset.shape[1]}")
        st.write(dataset.head())

        # Chiedi se l'utente vuole passare allo Step 2
        proceed_to_step_2 = st.button("Panoramica Esplorativa del Dataset")

        # STEP 2: Panoramica Esplorativa del Dataset
        # ----------------------------------------
        if proceed_to_step_2:
            st.info("Passaggio allo Step 2: Panoramica Esplorativa del Dataset...")
            st.subheader("Step 2: Panoramica Esplorativa del Dataset")

            # Panoramica esplorativa usando Sweetviz
            st.write("**Generazione del Report Esplorativo con Sweetviz:**")
            report = sv.analyze(dataset)
            report_path = "sweetviz_report.html"
            report.show_html(report_path)
            st.markdown(f"[Clicca qui per visualizzare il report completo]({report_path})", unsafe_allow_html=True)

            st.write("**Tipologia delle variabili:**")
            variable_types = dataset.dtypes
            st.write(variable_types)

            st.write("**Statistiche descrittive del dataset:**")
            descriptive_stats = dataset.describe()
            st.write(descriptive_stats)

            st.write("**Valori mancanti per ciascuna colonna:**")
            missing_values = dataset.isnull().sum()
            st.write(missing_values)
    else:
        st.error("Caricamento del dataset fallito. Verifica il file e riprova.")
