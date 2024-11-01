import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

            st.write("**Tipologia delle variabili:**")
            variable_types = dataset.dtypes
            st.write(variable_types)

            st.write("**Statistiche descrittive del dataset:**")
            descriptive_stats = dataset.describe()
            st.write(descriptive_stats)

            st.write("**Valori mancanti per ciascuna colonna:**")
            missing_values = dataset.isnull().sum()
            st.write(missing_values)

            # Visualizzazioni con Matplotlib
            st.write("**Visualizzazione delle Distribuzioni delle Variabili Numeriche:**")
            numeric_columns = dataset.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                fig, ax = plt.subplots(figsize=(10, 6))
                dataset[numeric_columns].hist(ax=ax, bins=15)
                st.pyplot(fig)
            else:
                st.write("Nessuna variabile numerica disponibile per la visualizzazione.")

            st.write("**Heatmap delle Correlazioni:**")
            if len(numeric_columns) > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(dataset[numeric_columns].corr(), annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)
            else:
                st.write("Non ci sono abbastanza variabili numeriche per generare una heatmap delle correlazioni.")
    else:
        st.error("Caricamento del dataset fallito. Verifica il file e riprova.")
