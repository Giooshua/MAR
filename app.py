import streamlit as st
import pandas as pd

# Titolo dell'applicazione
st.set_page_config(page_title="MAR Algorithm", page_icon="🧠")

# Titolo e logo dell'applicazione
st.image("https://via.placeholder.com/150", width=150)
st.title("MAR Algorithm")

# Caricamento del file
uploaded_file = st.file_uploader("Carica il tuo dataset (.csv, .txt)", type=["csv", "txt"])

def load_dataset(uploaded_file, delimiter=None):
    try:
        if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
            if delimiter:
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
            else:
                df = pd.read_csv(uploaded_file)  # Tentativo di auto-detection del delimitatore
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
