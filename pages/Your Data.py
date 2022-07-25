from numpy import disp
import streamlit as st
import mysql.connector
import pandas as pd
from pandas import DataFrame
from aqualog import Aqualog
from Home import querydatabase, login
import matplotlib.pyplot as plt
import altair


login()

aql = Aqualog()

aql.authenticate()

if st.session_state['login']:    
    st.header("AquaData Handling")

    data_menu = ["Add Data", "Display Data", "Update Data"]
    data_choice = st.selectbox('Choose operation.', data_menu)

# Add Data
    if data_choice == 'Add Data':    
        apt_name = (st.text_input("Enter Apartment name: "))
        house_list = st.text_input("Enter House IDs separated by a space: ").split()
        if st.button("Begin"):
            aql.create_aptmt(apt_name, house_list)
            st.info("Data Added. Use the Data Display options to see the information.")

# Display Data    
    elif data_choice == 'Display Data':
        st.header("Data Display")

        disp_menu = ["Apartment", "Amount per House"]
        disp_choice = st.selectbox('Choose option to display', disp_menu)

        if disp_choice == "Apartment":
            aptname = st.text_input("Enter Apartment Name: ")
            st.info("Available apartments: "+str(aql.get_apt_names()))
            if st.button("Display"):
                df = aql.info_extract_aptmt(aptname)
                st.table(df)

        elif disp_choice == "Amount per House":
            
            aptname = st.text_input("Enter Apartment Name: ")
            st.info("Available apartments: "+str(aql.get_apt_names()))
            homename = st.text_input("Enter House ID: ")
            if aptname != "":
                st.info("Available Home IDs: "+str(aql.get_home_names(aptname)))

            if st.button("Show Amount"):
                st.subheader("Amount: "+str(aql.amt_wtr(aptname, homename)))
    
                

# Update Data
    elif data_choice == 'Update Data':
        
        update_menu = ["Update Number of People", "Update Water Charge"]
        update_choice = st.selectbox('Choose updating option.', update_menu)

        if update_choice == "Update Number of People":
            aptname = st.text_input("Enter Apartment Name: ")
            st.info("Available apartments: "+str(aql.get_apt_names()))
            homename = st.text_input("Enter House ID: ")
            if aptname != "":
                st.info("Available Home IDs: "+str(aql.get_home_names(aptname)))

            numpeople = st.text_input("Enter Number of people in the house: ")
            
            if numpeople != "":
                aql.insert_into_house(aptname, homename, int(numpeople))
                st.success("Number of people updated.")

        elif update_choice == "Update Water Charge":
            aptname = st.text_input("Enter Apartment Name: ")
            st.info("Available apartments: "+str(aql.get_apt_names()))
            homename = st.text_input("Enter House ID: ")
            if aptname != "":
                st.info("Available Home IDs: "+str(aql.get_home_names(aptname)))

            watercharge = st.text_input("Enter Amount spent on water: ")
            if watercharge != "":
                aql.update_into_house(aptname, homename, watercharge)

else:
    st.error("Please sign in.")

