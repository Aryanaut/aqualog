import streamlit as st
import mysql.connector
import pandas as pd
from pandas import DataFrame
from aqualog import Aqualog
from Home import querydatabase, login
import matplotlib.pyplot as plt


login()

aql = Aqualog()

aql.authenticate()

if st.session_state['login']:    
    st.header("Data Creation")

    data_menu = ["Choose Operation", "Add Data", "Display Data", "Update Data"]
    data_choice = st.selectbox('Choose operation.', data_menu)

    if data_choice == 'Add Data':    
        apt_name = (st.text_input("Enter Apartment name: "))
        house_list = st.text_input("Enter House IDs separated by a space: ").split()
        if st.button("Begin"):
            aql.create_aptmt(apt_name, house_list)
            st.info("Data Added. Use the Data Display options to see the information.")
    
    elif data_choice == 'Display Data':
        st.header("Data Display")

        disp_menu = ["Independant Home", "Apartment", "Amount per House"]
        disp_choice = st.selectbox('Choose option to display', disp_menu)

        if disp_choice == "Independant Home":
            
            aptname = st.text_input("Enter Apartment name: ")            
            homename = st.text_input("Enter House ID: ")
            if aptname != "":
                st.info("Available Home IDs: "+str(aql.get_home_names(aptname)))

            if st.button("Display"):
                st.table(aql.info_extract_house(aptname, homename))

        elif disp_choice == "Apartment":
            aptname = st.text_input("Enter Apartment Name: ")
            st.info("Available apartments: "+str(aql.get_apt_names()))
            if st.button("Display"):
                df = aql.info_extract_aptmt(aptname)
                st.table(df)

        elif disp_choice == "Amount per House":
            aptname = st.text_input("Enter Apartment Name: ")
            st.info("Available apartments: "+str(aql.get_apt_names()))
            homename = st.text_input("Enter House ID: ")
            st.info("Available Home IDs: "+str(aql.get_home_names(aptname)))

            if st.button("Show Amount"):
                st.subheader(aql.amt_wtr(aptname, homename))

    elif data_choice == 'Update Data':
        st.info("Still being worked on.")

else:
    st.error("Please sign in.")

