import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

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

# STEP 1: Caricamento del Dataset
# ----------------------------------------

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
    with st.spinner('Caricamento in corso...'):
        time.sleep(2)  # Simulazione del tempo di caricamento

    st.subheader("Panoramica Esplorativa")

    # Creazione della dashboard interattiva
    tab1, tab2, tab3, tab4 = st.tabs(["Tipologia delle Variabili", "Statistiche Descrittive", "Visualizzazioni", "Heatmap delle Correlazioni"])

    with tab1:
        def categorize_variable(column):
            if dataset[column].dtype in ['float64', 'float32']:
                return 'Quantitativa - Continua'
            elif dataset[column].dtype in ['int64', 'int32']:
                if dataset[column].nunique() > 20:  # Se il numero di valori unici è alto, consideriamola continua
                    return 'Quantitativa - Continua'
                else:
                    return 'Quantitativa - Discreta'
            elif dataset[column].nunique() == 2:
                return 'Binaria'
            else:
                return 'Categorica - Nominale'

        variable_types = pd.DataFrame({
            'Colonna': dataset.columns,
            'Tipo': dataset.dtypes,
            'Categoria': dataset.columns.map(categorize_variable)
        })
        st.write(variable_types)

    with tab2:
        descriptive_stats = dataset.describe()
        st.write(descriptive_stats)

    with tab3:
        selected_variable = st.selectbox("Seleziona una variabile da visualizzare:", options=["Seleziona una variabile"] + list(dataset.columns), index=0, key='selected_variable')
        if selected_variable != "Seleziona una variabile" and selected_variable in dataset.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            if dataset[selected_variable].dtype in ['int64', 'int32']:
                if variable_types.loc[variable_types['Colonna'] == selected_variable, 'Categoria'].values[0] == 'Quantitativa - Discreta':
                    sns.barplot(x=dataset[selected_variable].value_counts().index, y=dataset[selected_variable].value_counts().values, ax=ax)
                    ax.set_title(f"Barplot di {selected_variable}")
                else:
                    sns.histplot(dataset[selected_variable], kde=True, ax=ax, bins=15)
                    ax.set_title(f"Distribuzione di {selected_variable}")
            elif dataset[selected_variable].dtype in ['float64', 'float32']:
                sns.histplot(dataset[selected_variable], kde=True, ax=ax, bins=15)
                ax.set_title(f"Distribuzione di {selected_variable}")
            else:
                sns.countplot(x=dataset[selected_variable], ax=ax)
                ax.set_title(f"Conteggio di {selected_variable}")
            st.pyplot(fig)
        elif selected_variable == "Seleziona una variabile":
            st.info("Seleziona una variabile per visualizzare il grafico.")

    with tab4:
        numeric_columns = dataset.select_dtypes(include=['int64', 'int32', 'float64', 'float32']).columns
        if len(numeric_columns) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(dataset[numeric_columns].corr() * 100, annot=True, cmap='crest', ax=ax, fmt='.0f')
            st.pyplot(fig)
        else:
            st.write("Non ci sono abbastanza variabili numeriche per generare una heatmap delle correlazioni.")
