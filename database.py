import sqlite3
import pandas as pd


# ==================================================
# DATABASE CONNECTION
# ==================================================

DATABASE_NAME = "data_analysis.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    return connection


# ==================================================
# SAVE DATASET TO DATABASE
# ==================================================

def save_dataset(df, table_name="uploaded_data"):

    connection = get_connection()

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()


# ==================================================
# LOAD DATASET FROM DATABASE
# ==================================================

def load_dataset(table_name="uploaded_data"):

    connection = get_connection()

    df = pd.read_sql(
        f"SELECT * FROM {table_name}",
        connection
    )

    connection.close()

    return df


# ==================================================
# GET TABLE INFORMATION
# ==================================================

def get_table_info(table_name="uploaded_data"):

    connection = get_connection()

    query = f"""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name='{table_name}'
    """

    result = pd.read_sql(
        query,
        connection
    )

    connection.close()

    return result