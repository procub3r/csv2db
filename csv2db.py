import glob
import sqlite3
import pandas as pd
import streamlit as st

con = sqlite3.connect('database.db')
cur = con.cursor()

st.markdown('# CSV 2 DB')
csvs = st.file_uploader('Upload CSV files', type='csv', accept_multiple_files=True)

for csv in csvs:
    df = pd.read_csv(csv)
    table_name = csv.name[:-4]
    try:
        df.to_sql(table_name, con, index=False)
    except ValueError as e:
        cur.execute(f'DROP TABLE {table_name};')
        df.to_sql(table_name, con, index=False)

    st.write(f'### table: {table_name}')
    st.write(df)

st.markdown('## Enter your query')
query = st.text_area('Enter your query')
if st.button('Execute'):
    try:
        result = pd.read_sql_query(query, con)
        st.markdown('### Result of query')
        result
    except Exception as e:
        st.error(f'Error executing query {e}')
