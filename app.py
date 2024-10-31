import streamlit as st
import pandas as pd

# Titolo dell'applicazione
st.set_page_config(page_title="MAR Algorithm", page_icon="🧠")

# Titolo e logo dell'applicazione
st.image("https://via.placeholder.com/150", width=150)
st.title("MAR Algorithm - Caricamento Dataset")
st.title("MAR Algorithm - Caricamento Dataset")

# Caricamento del file

delimiter_option = st.selectbox(
    "Seleziona il delimitatore per i file di testo:",
    options=["Tab (	)", "Virgola (,)", "Punto e virgola (;)", "Spazio ( )"],
    index=0
)

if delimiter_option == "Tab (	)":
    delimiter = '	'
elif delimiter_option == "Virgola (,)":
    delimiter = ','
elif delimiter_option == "Punto e virgola (;)":
    delimiter = ';'
elif delimiter_option == "Spazio ( )":
    delimiter = ' '


delimiter_option = st.selectbox(
    "Seleziona il delimitatore per i file di testo:",
    options=["Tab (	)", "Virgola (,)", "Punto e virgola (;)", "Spazio ( )"],
    index=0
)

if delimiter_option == "Tab (	)":
    delimiter = '	'
elif delimiter_option == "Virgola (,)":
    delimiter = ','
elif delimiter_option == "Punto e virgola (;)":
    delimiter = ';'
elif delimiter_option == "Spazio ( )":
    delimiter = ' '

uploaded_file = st.file_uploader("Carica il tuo dataset (.csv, .xls, .xlsx, .txt)", type=["csv", "xls", "xlsx", "txt"])

def load_dataset(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, delimiter=delimiter)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file, engine='openpyxl')  # Supporto per xlsx
    if delimiter != '':
        st.warning("Delimitatore selezionato non applicabile ai file Excel, ma viene comunque mostrato il dataset caricato correttamente.")
        elif uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_file, delimiter=delimiter)
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
