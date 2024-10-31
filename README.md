<p align="center">
  <img width="605" height="196" src="https://i.ibb.co/g6k3gvC/mar-high-resolution-logo-4.png">
</p>

# **MAR Interface**

The *MAR (Method-Approach-Recommendation) interface* is a [Streamlit](//) Python-based web application meant to provide a preliminary statistical overview on a given dataset. The primary goal is to assist users in selecting the most appropriate machine learning method based on the provided data: the application analyzes the dataset, performs quality checks, identifies variable types, and provides recommendations on which statistical method is the most appropriate to conduct an analysis with. Each algorithmic step is treated as an easily editable block, in order to further provide adjustments and fine-tuning on thresholds and criterias chosen for this project.

## **Features**

- **Dataset Upload**: Supports uploading `.csv`, `.xls`, `.xlsx`, or `.txt` files.
- **Data Quality Check**: Checks the dataset quality, including missing data analysis.
- **Variable Recognition**: Recognizes the types of variables present (continuous, categorical, boolean).
- **Outlier Handling**: Identifies outliers and provides recommendations for their handling.
- **ML Algorithm Recommendation**: Provides recommendations on suitable classification methods.

## **Installation**

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/username/mar-algorithm-app.git
   ```
2. Navigate to the project folder:
   ```bash
   cd mar-algorithm-app
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## **Usage**

TBD

## **Dependencies**

TBD


