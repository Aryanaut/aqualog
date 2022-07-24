from aqualog import Aqualog #testing-testing
import streamlit as st
import pandas as pd

aql = Aqualog()

if 'login' not in st.session_state:
    st.session_state['login'] = False

st.title("Aqualog")

def querydatabase():
    st.session_state['login'] = True
    aql.authenticate()

def login():
    if st.session_state['login'] == False:
        ID = st.sidebar.text_input("Enter Community ID: ")
        CODE = st.sidebar.text_input("Enter Community password: ", type="password")

        if st.sidebar.button("Login"):
            if CODE != 'bWw2vluRxM':
                st.sidebar.error("Incorrect password.")

            else:

                querydatabase()
                st.sidebar.info("Connection established.")
    else:

        if st.sidebar.button("End Connection"):
            aql.clean_up()
            st.sidebar.info("Connection ended.")
            st.session_state['login'] = False
        