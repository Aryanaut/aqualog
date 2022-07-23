from aqualog import Aqualog #testing-testing
import streamlit as st

aql = Aqualog()

st.title("Aqualog")

menu = ["Home", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home page")

elif choice == "Login":
    if aql.connected:
        st.info("Already connected to community.")
    else:
        ID = st.text_input("Enter Community ID: ")
        CODE = st.text_input("Enter Community password: ", type="password")

        if st.button("Login"):
            if CODE != 'bWw2vluRxM':
                st.error("Incorrect password.")

            else:
                aql.authenticate()
                st.info("Connection established.")

    if st.button("End Connection"):
        aql.clean_up()
        st.info("Connection closed.")