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

    try:

        df.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

    finally:

        connection.close()


# ==================================================
# LOAD DATASET FROM DATABASE
# ==================================================

def load_dataset(table_name="uploaded_data"):

    connection = get_connection()

    try:

        # Check whether table exists first
        table_exists = pd.read_sql(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?
            """,
            connection,
            params=(table_name,)
        )

        if table_exists.empty:
            return pd.DataFrame()

        df = pd.read_sql(
            f'SELECT * FROM "{table_name}"',
            connection
        )

        return df

    finally:

        connection.close()


# ==================================================
# GET TABLE INFORMATION
# ==================================================

def get_table_info(table_name="uploaded_data"):

    connection = get_connection()

    try:

        query = """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """

        result = pd.read_sql(
            query,
            connection,
            params=(table_name,)
        )

        return result

    finally:

        connection.close()


# ==================================================
# DELETE TABLE SAFELY
# ==================================================

def delete_table(table_name="uploaded_data"):

    connection = get_connection()

    try:

        connection.execute(
            f'DROP TABLE IF EXISTS "{table_name}"'
        )

        connection.commit()

    finally:

        connection.close()