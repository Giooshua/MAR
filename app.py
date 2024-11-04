import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import missingno as msno

# Titolo dell'applicazione
st.set_page_config(page_title="MAR Algorithm", page_icon="🧐")

# Titolo e logo dell'applicazione
st.image("https://i.ibb.co/g6k3gvC/mar-high-resolution-logo-4.png", width=200)
st.title("Interfaccia")

# Inizializza lo stato della sessione
if 'proceed_to_step_2' not in st.session_state:
    st.session_state['proceed_to_step_2'] = False
if 'selected_variable' not in st.session_state:
    st.session_state['selected_variable'] = None
if 'raggruppate_altro' not in st.session_state:
    st.session_state['raggruppate_altro'] = {}
if 'proceed_to_step_3' not in st.session_state:
    st.session_state['proceed_to_step_3'] = False
if 'dataset' not in st.session_state:
    st.session_state['dataset'] = None
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

# Funzione per categorizzare le variabili
def categorize_variable(dataset, column):
    if dataset[column].dtype in ['float64', 'float32']:
        return 'Quantitativa - Continua'
    elif dataset[column].dtype in ['int64', 'int32']:
        if dataset[column].nunique() > 20:
            return 'Quantitativa - Continua'
        else:
            return 'Quantitativa - Discreta'
    elif dataset[column].nunique() == 2:
        return 'Binaria'
    else:
        return 'Categorica - Nominale'

# STEP 1: Caricamento del Dataset
# ----------------------------------------
with st.expander("Step 1: Caricamento del Dataset", expanded=True):
    uploaded_file = st.file_uploader("Carica il tuo dataset (.csv, .txt)", type=["csv", "txt"])
    
    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file  # Salva il file in session_state

    def load_dataset(uploaded_file, delimiter=','):
        try:
            if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
            else:
                return None
            return df
        except Exception as e:
            st.error(f"Errore nel caricamento del file: {str(e)}")
            return None

    if st.session_state['uploaded_file'] is not None:
        if st.session_state['dataset'] is None:
            dataset = load_dataset(st.session_state['uploaded_file'])
            if dataset is not None:
                st.session_state['dataset'] = dataset  # Salva il dataset in session_state
                st.success(f"Dataset caricato con successo! Righe: {dataset.shape[0]}, Colonne: {dataset.shape[1]}")
                st.write(dataset.head())

                # Chiedi se l'utente vuole passare allo Step 2
                if st.button("Panoramica Esplorativa del Dataset"):
                    st.session_state['proceed_to_step_2'] = True
            else:
                st.error("Caricamento del dataset fallito. Verifica il file e riprova.")
        else:
            dataset = st.session_state['dataset']
            st.success(f"Dataset già caricato! Righe: {dataset.shape[0]}, Colonne: {dataset.shape[1]}")
            st.write(dataset.head())

            # Chiedi se l'utente vuole passare allo Step 2
            if st.button("Panoramica Esplorativa del Dataset"):
                st.session_state['proceed_to_step_2'] = True
    else:
        st.info("Per favore, carica un dataset per procedere.")

# STEP 2: Panoramica Esplorativa del Dataset
# ----------------------------------------
if st.session_state['proceed_to_step_2'] and not st.session_state['proceed_to_step_3'] and st.session_state['dataset'] is not None:
    dataset = st.session_state['dataset']  # Recupera il dataset da session_state
    with st.expander("Step 2: Panoramica Esplorativa del Dataset", expanded=True):
        with st.spinner('Caricamento in corso...'):
            time.sleep(2)  # Simulazione del tempo di caricamento

        # Creazione della dashboard interattiva
        tab1, tab2, tab3, tab4 = st.tabs(["Tipologia delle Variabili", "Statistiche Descrittive", "Visualizzazioni", "Heatmap delle Correlazioni"])

        with tab1:
            variable_types = pd.DataFrame({
                'Colonna': dataset.columns,
                'Tipo': dataset.dtypes,
                'Categoria': [categorize_variable(dataset, col) for col in dataset.columns]
            })
            st.write(variable_types.drop(columns=['Tipo']))

        with tab2:
            descriptive_stats = dataset.describe()
            descriptive_stats.index = descriptive_stats.index.str.capitalize()
            st.write(descriptive_stats)

        with tab3:
            selected_variable = st.selectbox("Seleziona una variabile da visualizzare:", options=["Seleziona una variabile"] + list(dataset.columns), index=0, key='selected_variable')
            if selected_variable != "Seleziona una variabile" an
