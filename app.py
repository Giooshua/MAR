
import streamlit as st
import pandas as pd

# Titolo dell'applicazione
st.title("MAR Algorithm - Caricamento Dataset")

# Caricamento del file
uploaded_file = st.file_uploader("Carica il tuo dataset (.csv, .xls, .xlsx, .txt)", type=["csv", "xls", "xlsx", "txt"])

def load_dataset(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_file, delimiter='	')
        else:
            st.error("Formato del file non supportato. Supportati: .csv, .xls, .xlsx, .txt")
            return None
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {str(e)}")
        return None

# Mostra il dataset caricato
if uploaded_file is not None:
    dataset = load_dataset(uploaded_file)
    if dataset is not None:
        st.success(f"Dataset caricato con successo! Righe: {dataset.shape[0]}, Colonne: {dataset.shape[1]}")
        st.write(dataset.head())
    else:
        st.error("Caricamento del dataset fallito. Verifica il file e riprova.")
    