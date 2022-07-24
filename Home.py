from aqualog import Aqualog #testing-testing
import streamlit as st
import pandas as pd

aql = Aqualog()

if 'login' not in st.session_state:
    st.session_state['login'] = False

st.title("Aqualog")

str = """

## What is Aqualog?
AquaLog is a community-based water inventory. Individuals from a community input their monthly water charge, and AquaLog shows them how much water they've been using above the recommended amount, and how much money they could have saved.

We use a suite of formulae designed by us to reverse engineer the monthly overage of both the individual house and the apartment as a whole.
To raise awareness about how we waste the precious and scarce resource that is water.

__To begin, go to "Your Data" and enter your community's username and password to access its database.__

"""

st.markdown(str)

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
        