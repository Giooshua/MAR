import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import missingno as msno

# Titolo dell'applicazione
st.set_page_config(page_title="MAR Algorithm", page_icon="🤔")

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
if 'exclude_variables' not in st.session_state:
    st.session_state['exclude_variables'] = []
if 'exclude_observations' not in st.session_state:
    st.session_state['exclude_observations'] = []

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
            st.write(variable_types.drop(columns=['Tipo']))

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
                        sns.barplot(x=dataset[selected_variable].value_counts().index, y=dataset[selected_variable].value_counts().values, ax=ax)
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
                    sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax)
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

        # Creazione di una copia del dataset originale
        filtered_dataset = dataset.copy()

        # Creazione della dashboard interattiva per l'analisi dei dati mancanti
        tab1, tab2, tab3 = st.tabs(["Quantificazione dei Dati Mancanti", "Visualizzazioni dei Dati Mancanti", "Pattern di Missingness"])

        with tab1:
            missing_summary = pd.DataFrame({
                'Variabile': filtered_dataset.columns,
                'Valori Mancanti': filtered_dataset.isnull().sum(),
                'Percentuale Mancante (%)': filtered_dataset.isnull().mean() * 100,
                'Tipo Variabile': filtered_dataset.columns.map(lambda col: categorize_variable(col))
            }).reset_index(drop=True)
            st.write(missing_summary)

        with tab2:
            missing_values = filtered_dataset.isnull().sum()
            missing_values = missing_values[missing_values > 0]

            if not missing_values.empty:
                plt.figure(figsize=(10, 6))
                sns.barplot(x=missing_values.index, y=missing_values.values, palette="viridis")
                plt.xticks(rotation=45)
                plt.xlabel('Variabile')
                plt.ylabel('Numero di Valori Mancanti')
                plt.title('Valori Mancanti per Variabile')
                st.pyplot(plt)

                msno.matrix(filtered_dataset)
                plt.title('Matrice dei Valori Mancanti nel Dataset')
                st.pyplot(plt)
            else:
                st.write("Non ci sono valori mancanti nel dataset.")

        with tab3:
            if filtered_dataset.isnull().sum().sum() > 0:
                msno.heatmap(filtered_dataset)
                plt.title('Correlazione dei Valori Mancanti tra le Variabili')
                st.pyplot(plt)
            else:
                st.write("Non ci sono abbastanza dati mancanti per analizzare i pattern di missingness.")

        # Selezione delle variabili da escludere dall'analisi dei dati mancanti
        st.markdown("### Selezione delle Variabili da Escludere")
        st.session_state['exclude_variables'] = st.multiselect("Seleziona variabili da escludere dall'analisi dei dati mancanti:", options=dataset.columns)
        filtered_dataset = filtered_dataset.drop(columns=st.session_state['exclude_variables'], errors='ignore')

        # Selezione delle osservazioni da escludere
        st.markdown("### Selezione delle Osservazioni da Escludere")
        st.markdown("Inserisci un criterio per escludere le osservazioni dal dataset. Puoi usare condizioni come `colonna == valore`, `colonna > valore`, etc. Ad esempio: `Age > 30` per escludere tutte le osservazioni con `Age` maggiore di 30.")
        st.session_state['exclude_observations'] = st.text_input("Inserisci il criterio per escludere le osservazioni:")
        if st.session_state['exclude_observations']:
            try:
                filtered_dataset = filtered_dataset.query(f"{st.session_state['exclude_observations']}")
                st.write("Osservazioni escluse in base al criterio specificato.")
            except Exception as e:
                st.error(f"Errore nel criterio di esclusione: {str(e)}")

        # Imputazione o analisi successiva da effettuare solo su filtered_dataset
        # Successivamente, il dataset originale rimane intatto e possiamo riutilizzarlo
        # Il dataset con imputazioni può essere unito al dataset originale, se necessario
