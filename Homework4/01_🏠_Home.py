import streamlit as st
from utils.utils import *
import pymysql,cryptography

if __name__ == "__main__":
    st.set_page_config(
        page_title="Business Analytics",
        layout="wide",
        page_icon="🗂",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# *Introduction to Databases* course"
        }
    )


    col1,col2=st.columns([3,2])
    with col1:
        st.title("Student: _Edoardo Silvio Gribaldo_")
        st.title(":red[s295616]")
        st.title("Homework 4")
        st.title("Introduction to databases 2022/2023")
    with col2:
        st.image("images/polito_white.png")
    st.header(":red[Goal]")
    st.write("The goal of this homework is to learn how to connect a database to a simple web app and make some requests to retrieve data from the database")
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    check_connection()
