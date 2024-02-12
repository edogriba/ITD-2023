import streamlit as st
from sqlalchemy import create_engine,text

"""Collects the main functions shared by the various pages"""

def connect_db(dialect,username,password,host,dbname):
    try:
        engine = create_engine(f'{dialect}://{username}:{password}@{host}/{dbname}')
        conn = engine.connect()
        return conn
    except:
        return False

def execute_query(conn, query):
    return conn.execute(text(query))

def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    if st.sidebar.button("Connect to the database"):
        myconnection = connect_db(dialect="mysql+pymysql", username="root", password="mypassword", host="localhost", dbname="gym")
        if myconnection is not False:
            st.session_state["connection"] = myconnection
        else:
            st.session_state["connection"] = False
            st.sidebar.error("Error connecting to the db")

    if st.session_state["connection"]:
        st.sidebar.success("Connected to the db")
        return True

def compact_format(num):
    num=float(num)
    if abs(num) >= 1e9:
        return "{:.2f}B".format(num / 1e9)
    elif abs(num) >= 1e6:
        return "{:.2f}M".format(num / 1e6)
    elif abs(num) >= 1e3:
        return "{:.2f}K".format(num / 1e3)
    else:
        return "{:.0f}".format(num)

def get_list(attribute, table):
    query = f"SELECT DISTINCT {attribute} FROM {table}"
    result = execute_query(st.session_state["connection"], query)
    result_list = []
    for row in result.mappings():
        result_list.append(row[attribute])
    return result_list

def get_list_where(attribute, table):
    query = f"SELECT CId FROM {table} WHERE Day = '{attribute}'"
    result = execute_query(st.session_state["connection"], query)
    result_list = []
    for row in result.mappings():
        result_list.append(row["CId"])
    return result_list

def get_info(attribute, table):
    return get_list(attribute, table)


# check if all text fields have been filled
def check_info(prod_dict):
    for value in prod_dict.values():
        if value == '':
            return False
    return True


# insert the new product
def insert(prod_dict, table):
    if check_info(prod_dict):
        attributes = ", ".join(prod_dict.keys())
        values = tuple(prod_dict.values())
        query = f"INSERT INTO {table} ({attributes}) VALUES {values};"
        # try-except to verify that the MySQL operation was successful generate an error otherwise
        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
        except:
            st.error("Insertion not successful.", icon='⚠️')
            return False
        return True
    else:
        return False
