import pandas as pd
from pathlib import Path
import sqlite3
from sqlite3 import Connection
import streamlit as st

URI_SQLITE_DB = "test1.db"

def main():
    st.title("My Database")
    st.markdown("Enter data in database from sidebar, then SUBMIT")

    conn = get_connection(URI_SQLITE_DB)
    init_db(conn)

    build_sidebar(conn)
    display_data(conn)


def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS test
            (
                ULB_NAME VARCHAR2(30),
                INPUT1 INT,
                INPUT2 INT
            );"""
    )
    conn.commit()

def build_sidebar(conn: Connection):
    st.sidebar.header("Configuration")
    ulb = st.sidebar.selectbox(
        "Name of the ULB",
        ('Keelakarai', 'Paramakudi', 'Ramanathapuram', 'Rameswaram'))
    input1 = st.sidebar.text_input("Input 1", 0, 100)
    input2 = st.sidebar.text_input("Input 2", 0, 100)
    if st.sidebar.button("Save to database"):
        conn.execute(f"INSERT INTO test (ULB_NAME, INPUT1, INPUT2) VALUES ('{ulb}', {input1}, {input2})")
        conn.commit()

def display_data(conn: Connection):
    if st.checkbox("Display data in sqlite database"):
        st.dataframe(get_data(conn))

def run_calculator(conn: Connection):
    if st.button("Run Calculator"):
        st.info("Run your function")
        df = get_data(conn)
        st.write(df.sum())

def get_data(conn: Connection):
    df = pd.read_sql("SELECT * FROM test", con=conn)
    return df

@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit
    NB: https://stackoverflow.com/questions/48218065/programmingerro-sqlite-object
    """
    return sqlite3.connect(path, check_same_thread=False)

if __name__ == "__main__":
    main()
