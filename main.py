from aqualog import Aqualog
import streamlit as st

aql = Aqualog()

st.title("Test.")

if aql.connected:
    st.info("Already connected to community.")
else:
    if st.button("Connect to Community"):
        ID = st.text_input("Enter Community ID: ")
        CODE = st.text_input("Enter Community password: ")

        if CODE != 'bWw2vluRxM':
            st.error("Incorrect password.")

        else:
            aql.authenticate(ID, CODE)
            st.info("Connection established.")

    if st.button("End Connection"):
        aql.clean_up()
        st.info("Connection closed.")