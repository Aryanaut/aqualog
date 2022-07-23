from aqualog import Aqualog #testing-testing
import streamlit as st
import pandas as pd

aql = Aqualog()

st.title("Aqualog")

menu = ["Home", "Login", "Your Data"]
choice = st.sidebar.selectbox("Menu", menu)
connected = False

if choice == "Home":
    st.subheader("Home page")

elif choice == "Login":
    if connected:
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
                connected = True

        if st.button("End Connection"):
            aql.clean_up()
            st.info("Connection closed.")
            connected = False

elif choice == "Your Data":
    if connected:
        st.title("Data Creation")
        
        creation_menu = ["Independant Home", "Apartment"]
        creation_choice = st.radio('Choose type of data to add', creation_menu)

        if creation_choice == "Apartment":
            num_houses = int(st.text_input("Enter number of houses in the apartment: "))
            apt_name = (st.text_input("Enter Apartment name: "))
            aql.create_aptmt(apt_name, num_houses)
        else:
            st.info("This section is still being worked on.")

    else:
        st.info("Use the login page first.")