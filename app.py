import streamlit as st
import pandas as pd

# Titolo dell'applicazione
st.set_page_config(page_title="MAR Algorithm", page_icon="🧠")

# Titolo e logo dell'applicazione
st.image("https://via.placeholder.com/150", width=150)
st.title("MAR Algorithm")

# STEP 1: Caricamento del Dataset
# ----------------------------------------
uploaded_file = st.file_uploader("Carica il tuo dataset (.csv, .txt)", type=["csv", "txt"])

def load_dataset(uploaded_file, delimiter=None):
    try:
        if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_file)  # Tentativo di auto-detection del delimitatore
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
        proceed_to_step_2 = st.button("Passa allo Step 2: Data Quality Check")

        # STEP 2: Data Quality Check
        # ----------------------------------------
        if proceed_to_step_2:
            st.info("Passaggio allo Step 2: Controllo Qualità dei Dati...")
            st.subheader("Step 2: Data Quality Check")

            # Controllo dei dati mancanti
            st.markdown("**Controllo dei Valori Mancanti**")
            missing_data = dataset.isnull().sum()
            total_missing = missing_data.sum()
            if total_missing > 0:
                st.warning(f"Il dataset contiene {total_missing} valori mancanti.")
                st.write(missing_data[missing_data > 0])
                if total_missing / dataset.size > 0.3:
                    st.error("La qualità del dataset è troppo bassa a causa dell'elevata percentuale di valori mancanti. Si consiglia di interrompere l'analisi.")
                elif total_missing / dataset.size > 0.1:
                    st.warning("I dati mancanti non sono uniformemente distribuiti. Si consiglia l'uso di tecniche avanzate di imputazione come l'imputazione iterativa.")
                elif total_missing / dataset.size > 0.05:
                    st.info("L'imputazione con media o mediana potrebbe essere sufficiente per gestire i dati mancanti.")
                st.markdown("**Distribuzione dei Valori Mancanti**")
                st.bar_chart(missing_data[missing_data > 0])
            else:
                st.success("Non ci sono valori mancanti nel dataset.")

            # Controllo delle righe duplicate
            st.markdown("**Controllo delle Righe Duplicate**")
            duplicate_rows = dataset.duplicated().sum()
            if duplicate_rows > 0:
                st.warning(f"Il dataset contiene {duplicate_rows} righe duplicate.")
                st.info("Si consiglia di rimuovere le righe duplicate per migliorare la qualità del dataset.")
            else:
                st.success("Non ci sono righe duplicate nel dataset.")

            # Informazioni generali sul dataset
            st.subheader("Informazioni Generali del Dataset")
            st.write(dataset.describe())
    else:
        st.error("Caricamento del dataset fallito. Verifica il file e riprova.")
