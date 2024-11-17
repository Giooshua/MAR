import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import missingno as msno
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Titolo dell'applicazione
st.set_page_config(page_title="MAR Algorithm", page_icon="🤔")

# Titolo e logo dell'applicazione
try:
    st.image("https://i.ibb.co/g6k3gvC/mar-high-resolution-logo-4.png", width=200)
except Exception as e:
    st.warning("Non è stato possibile caricare l'immagine del logo.")

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
if 'exclude_variables' not in st.session_state:
    st.session_state['exclude_variables'] = []
if 'exclude_observations' not in st.session_state:
    st.session_state['exclude_observations'] = []
if 'imputation_strategy' not in st.session_state:
    st.session_state['imputation_strategy'] = 'mean'

# STEP 1: Caricamento del Dataset
# ----------------------------------------
with st.expander("Step 1: Caricamento del Dataset", expanded=True):
    uploaded_file = st.file_uploader("Carica il tuo dataset (.csv, .txt)", type=["csv", "txt"])

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

    if uploaded_file is not None:
        dataset = load_dataset(uploaded_file)
        if dataset is not None:
            st.success(f"Dataset caricato con successo! Righe: {dataset.shape[0]}, Colonne: {dataset.shape[1]}")
            st.write(dataset.head())

            # Chiedi se l'utente vuole passare allo Step 2
            if st.button("Panoramica Esplorativa del Dataset"):
                st.session_state['proceed_to_step_2'] = True
        else:
            st.error("Caricamento del dataset fallito. Verifica il file e riprova.")

# STEP 2: Panoramica Esplorativa del Dataset
# ----------------------------------------
if st.session_state['proceed_to_step_2'] and uploaded_file is not None:
    with st.expander("Step 2: Panoramica Esplorativa del Dataset", expanded=True):
        with st.spinner('Caricamento in corso...'):
            time.sleep(2)  # Simulazione del tempo di caricamento

        # Creazione della dashboard interattiva
        tab1, tab2, tab3, tab4 = st.tabs(["Tipologia delle Variabili", "Statistiche Descrittive", "Visualizzazioni", "Heatmap delle Correlazioni"])

        with tab1:
            def categorize_variable(column):
                if pd.api.types.is_numeric_dtype(dataset[column]):
                    return 'Quantitativa - Continua' if dataset[column].nunique() > 20 else 'Quantitativa - Discreta'
                elif dataset[column].nunique() == 2:
                    return 'Binaria'
                else:
                    return 'Categorica - Nominale'

            variable_types = pd.DataFrame({
                'Colonna': dataset.columns,
                'Categoria': dataset.columns.map(categorize_variable)
            })
            st.write(variable_types)

        with tab2:
            descriptive_stats = dataset.describe()
            descriptive_stats.index = descriptive_stats.index.str.capitalize()
            st.write(descriptive_stats)

        with tab3:
            selected_variable = st.selectbox("Seleziona una variabile da visualizzare:", options=["Seleziona una variabile"] + list(dataset.columns), index=0, key='selected_variable')
            if selected_variable != "Seleziona una variabile" and selected_variable in dataset.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                if dataset[selected_variable].dtype in ['int64', 'int32']:
                    if variable_types.loc[variable_types['Colonna'] == selected_variable, 'Categoria'].values[0] == 'Quantitativa - Discreta':
                        sns.barplot(x=dataset[selected_variable].value_counts().index.astype(str), y=dataset[selected_variable].value_counts().values, ax=ax)
                        ax.set_title(f"Barplot di {selected_variable}")
                    else:
                        sns.histplot(dataset[selected_variable], kde=True, ax=ax, bins=15)
                        ax.set_title(f"Distribuzione di {selected_variable}")
                elif dataset[selected_variable].dtype in ['float64', 'float32']:
                    sns.histplot(dataset[selected_variable], kde=True, ax=ax, bins=15)
                    ax.set_title(f"Distribuzione di {selected_variable}")
                else:
                    value_counts = dataset[selected_variable].value_counts()
                    if len(value_counts) > 15:
                        top_categories = value_counts.nlargest(15).index
                        altre_categorie = set(value_counts.index) - set(top_categories)
                        if altre_categorie:  # Se ci sono categorie da raggruppare
                            dataset[selected_variable] = dataset[selected_variable].apply(lambda x: x if x in top_categories else 'Altro')
                            value_counts = dataset[selected_variable].value_counts()
                            st.session_state['raggruppate_altro'][selected_variable] = altre_categorie
                    sns.barplot(x=value_counts.index.astype(str), y=value_counts.values, ax=ax)
                    ax.set_title(f"Conteggio di {selected_variable}")
                    if (any(len(str(label)) > 4 and label != 'Altro' for label in value_counts.index) or len(value_counts) > 10) and len(value_counts) > 4:
                        plt.xticks(rotation=90, fontsize=10)
                st.pyplot(fig)

                if selected_variable in st.session_state['raggruppate_altro'] and st.session_state['raggruppate_altro'][selected_variable]:
                    with st.expander(f"Visualizza le categorie raggruppate in 'Altro' per la variabile '{selected_variable}'"):
                        st.write(f"Le categorie raggruppate in 'Altro' per la variabile {selected_variable} sono:")
                        st.write(st.session_state['raggruppate_altro'][selected_variable])
            elif selected_variable == "Seleziona una variabile":
                st.info("Seleziona una variabile per visualizzare il grafico.")

        with tab4:
            numeric_columns = dataset.select_dtypes(include=['int64', 'int32', 'float64', 'float32']).columns
            if len(numeric_columns) > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(dataset[numeric_columns].corr() * 100, annot=True, cmap='crest', ax=ax, fmt='.0f')
                st.pyplot(fig)
                plt.close()
            else:
                st.write("Non ci sono abbastanza variabili numeriche per generare una heatmap delle correlazioni.")

        # Pulsante per passare allo Step 3
        if st.button("Analisi dell'Entità dei Dati Mancanti", key='step_3_button'):
            st.session_state['proceed_to_step_3'] = True

# STEP 3: Analisi dell'Entità dei Dati Mancanti
# ----------------------------------------
if st.session_state['proceed_to_step_3'] and uploaded_file is not None:
    with st.expander("Step 3: Analisi dell'Entità dei Dati Mancanti", expanded=True):
        with st.spinner('Analisi dei dati mancanti in corso...'):
            time.sleep(2)  # Simulazione del tempo di caricamento

        # Creazione della dashboard interattiva per l'analisi dei dati mancanti
        tab1, tab2, tab3 = st.tabs(["Quantificazione dei Dati Mancanti", "Visualizzazioni dei Dati Mancanti", "Pattern di Missingness"])

        with tab1:
            missing_summary = pd.DataFrame({
                'Variabile': dataset.columns,
                'Valori Mancanti': dataset.isnull().sum(),
                'Percentuale Mancante (%)': dataset.isnull().mean() * 100,
                'Tipo Variabile': dataset.columns.map(lambda col: categorize_variable(col))
            }).reset_index(drop=True)
            st.write(missing_summary)

        with tab2:
            missing_values = dataset.isnull().sum()
            missing_values = missing_values[missing_values > 0]

            if not missing_values.empty:
                plt.figure(figsize=(10, 6))
                sns.barplot(x
