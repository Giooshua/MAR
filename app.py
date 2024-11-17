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
if 'proceed_to_step_4' not in st.session_state:
    st.session_state['proceed_to_step_4'] = False

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
                sns.barplot(x=missing_values.index, y=missing_values.values, palette="viridis")
                plt.xticks(rotation=45)
                plt.xlabel('Variabile')
                plt.ylabel('Numero di Valori Mancanti')
                plt.title('Valori Mancanti per Variabile')
                st.pyplot(plt)
                plt.close()

                msno.matrix(dataset)
                plt.title('Matrice dei Valori Mancanti nel Dataset')
                st.pyplot(plt)
                plt.close()
            else:
                st.write("Non ci sono valori mancanti nel dataset.")
                if st.button("Passa allo Step 4 - Analisi Successiva", key='step_4_button_no_missing'):
                    st.session_state['proceed_to_step_4'] = True

        with tab3:
            if dataset.isnull().sum().sum() > 0:
                msno.heatmap(dataset)
                plt.title('Correlazione dei Valori Mancanti tra le Variabili')
                st.pyplot(plt)
                plt.close()
            else:
                st.write("Non ci sono abbastanza dati mancanti per analizzare i pattern di missingness.")

        # Selezione delle variabili da escludere dall'analisi dei dati mancanti
        st.markdown("### Selezione delle Variabili da Escludere")
        st.session_state['exclude_variables'] = st.multiselect("Seleziona variabili da escludere dall'analisi dei dati mancanti:", options=dataset.columns)
        filtered_dataset = dataset.drop(columns=st.session_state['exclude_variables'], errors='ignore')

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

        # Analisi successiva da effettuare solo su filtered_dataset senza modificare il dataset originale
        # Il dataset con imputazioni può essere unito al dataset originale, se necessario, per ripristinare le variabili e osservazioni escluse

        # Selezione della Strategia di Imputazione
        st.markdown("### Seleziona la Strategia di Imputazione")
        st.session_state['imputation_strategy'] = st.selectbox("Seleziona la strategia di imputazione:", options=['Media', 'Mediana', 'Più frequente', 'Iterative Imputer', 'KNN Imputer'], index=0)
        
        # Suggerimento per l'Imputazione dei Dati Mancanti
        if st.button("Suggerimento per l'Imputazione"):
            suggestion = ""
            if missing_summary['Percentuale Mancante (%)'].max() > 30:
                suggestion = "MAR ha trovato una percentuale elevata di valori mancanti. Suggerisce di utilizzare 'KNN Imputer' o 'Iterative Imputer' per ottenere imputazioni più accurate."
            elif dataset.corr().abs().max().max() > 0.7:
                suggestion = "I dati sono altamente correlati. MAR suggerisce di utilizzare 'Iterative Imputer' per mantenere la coerenza tra le variabili."
            elif missing_summary['Percentuale Mancante (%)'].mean() < 10:
                suggestion = "La percentuale media di valori mancanti è bassa. Potrebbe essere sufficiente utilizzare 'Media' o 'Mediana' per l'imputazione."
            else:
                suggestion = "Considera l'utilizzo di 'Iterative Imputer' o 'KNN Imputer' per migliorare l'accuratezza delle imputazioni."
            
            st.info(suggestion)

        # Imputazione dei Dati Mancanti
        if st.button("Applica Imputazione"):
            imputation_strategy = st.session_state['imputation_strategy']
            if imputation_strategy == 'Media':
                imputer = SimpleImputer(strategy='mean')
            elif imputation_strategy == 'Mediana':
                imputer = SimpleImputer(strategy='median')
            elif imputation_strategy == 'Più frequente':
                imputer = SimpleImputer(strategy='most_frequent')
            elif imputation_strategy == 'Iterative Imputer':
                imputer = IterativeImputer()
            elif imputation_strategy == 'KNN Imputer':
                imputer = KNNImputer()
            
            imputed_data = imputer.fit_transform(filtered_dataset.select_dtypes(include=['int64', 'int32', 'float64', 'float32']))
            filtered_dataset.loc[:, filtered_dataset.select_dtypes(include=['int64', 'int32', 'float64', 'float32']).columns] = imputed_data

            # Ripristina le variabili e osservazioni escluse
            excluded_variables = dataset[st.session_state['exclude_variables']] if st.session_state['exclude_variables'] else pd.DataFrame()
            final_dataset = pd.concat([filtered_dataset, excluded_variables], axis=1)

            if st.session_state['exclude_observations']:
                excluded_observations = dataset.query(f"not ({st.session_state['exclude_observations']})")
                final_dataset = pd.concat([final_dataset, excluded_observations], axis=0).drop_duplicates()

            st.write("Dati mancanti imputati con successo utilizzando la strategia selezionata.")
            st.write(final_dataset.head())

        # Pulsante per passare allo Step 4 dopo imputazione completata
        if st.button("Passa allo Step 4 - Gestione degli Outlier", key='step_4_button_after_imputation'):
            st.session_state['proceed_to_step_4'] = True

# STEP 4: Gestione degli Outlier
# ----------------------------------------
if st.session_state['proceed_to_step_4']:
    st.header("Step 4: Gestione degli Outlier")
    st.write("In questa sezione verrà affrontata la gestione degli outlier nel final_dataset pulito.")

    # Seleziona le variabili numeriche per la gestione degli outlier
    numeric_columns = final_dataset.select_dtypes(include=['int64', 'int32', 'float64', 'float32']).columns
    selected_outlier_variable = st.selectbox("Seleziona una variabile per gestire gli outlier:", options=numeric_columns, index=0)

    if selected_outlier_variable:
        st.write(f"Analisi degli outlier per la variabile: {selected_outlier_variable}")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x=final_dataset[selected_outlier_variable], ax=ax)
        st.pyplot(fig)

        # Definizione del metodo per gestire gli outlier
        outlier_method = st.selectbox("Seleziona il metodo per gestire gli outlier:", options=["Rimuovi outlier", "Sostituisci con la mediana", "Winsorize"], index=0)

        if st.button("Applica Gestione degli Outlier"):
            if outlier_method == "Rimuovi outlier":
                Q1 = final_dataset[selected_outlier_variable].quantile(0.25)
                Q3 = final_dataset[selected_outlier_variable].quantile(0.75)
                IQR = Q3 - Q1
                filtered_dataset = final_dataset[~((final_dataset[selected_outlier_variable] < (Q1 - 1.5 * IQR)) | (final_dataset[selected_outlier_variable] > (Q3 + 1.5 * IQR)))]
                st.write("Outlier rimossi con successo.")
            elif outlier_method == "Sostituisci con la mediana":
                Q1 = final_dataset[selected_outlier_variable].quantile(0.25)
                Q3 = final_dataset[selected_outlier_variable].quantile(0.75)
                IQR = Q3 - Q1
                median_value = final_dataset[selected_outlier_variable].median()
                final_dataset[selected_outlier_variable] = final_dataset[selected_outlier_variable].apply(lambda x: median_value if (x < (Q1 - 1.5 * IQR)) or (x > (Q3 + 1.5 * IQR)) else x)
                st.write("Outlier sostituiti con la mediana con successo.")
            elif outlier_method == "Winsorize":
                from scipy.stats.mstats import winsorize
                final_dataset[selected_outlier_variable] = winsorize(final_dataset[selected_outlier_variable], limits=[0.05, 0.05])
                st.write("Outlier winsorizzati con successo.")

            st.write(final_dataset.head())
