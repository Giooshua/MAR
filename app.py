import streamlit as st
import pandas as pd

# Titolo dell'applicazione
st.set_page_config(page_title="MAR Algorithm", page_icon="🧠")

# Titolo e logo dell'applicazione
st.image("https://via.placeholder.com/150", width=150)
st.title("MAR Algorithm - Caricamento Dataset")

# Caricamento del file
uploaded_file = st.file_uploader("Carica il tuo dataset (.csv, .xls, .xlsx, .txt)", type=["csv", "xls", "xlsx", "txt"])

def load_dataset(uploaded_file, delimiter=None):
    try:
        if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
            if delimiter:
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
            else:
                df = pd.read_csv(uploaded_file)  # Tentativo di auto-detection del delimitatore
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file, engine='openpyxl')  # Supporto per xlsx
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

        # Mostra i bottoni per selezionare il delimitatore manualmente
        st.subheader("Seleziona un delimitatore per modificare la visualizzazione del dataset:")
        if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
            delimiters = {
                "Tab (\t)": '\t',
                "Virgola (,)": ',',
                "Punto e virgola (;)": ';',
                "Spazio ( )": ' '
            }
            for label, delim in delimiters.items():
                if st.button(label):
                    dataset = load_dataset(uploaded_file, delimiter=delim)
                    if dataset is not None:
                        st.write(dataset.head())
    else:
        st.error("Caricamento del dataset fallito. Verifica il file e riprova.")
