from .functions.aqualog import Aqualog
import streamlit as st

aql = Aqualog()

st.title("Test.")

ID = st.text_input("Enter Community ID: ")
CODE = st.text_input("Enter Community password: ")

if CODE != 'bWw2vluRxM':
    st.error("Incorrect password.")

else:
    aql.authenticate(ID, CODE)
    st.info("Connection established.")
