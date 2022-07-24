import mysql.connector
import streamlit as st
import pandas as pd
from pandas import DataFrame

class Aqualog:

    def __init__(self):
        self.wtr_tax = 7 # Bangalore water charge is Rs. 7 per kilolitre. This may change.
        self.ideal_wtr = 4050
        self.ideal_wtr_tax = 4.05 * self.wtr_tax
        self.connected = False
        self.datacon = None
        self.cursor = None
    
    @st.experimental_singleton
    def start_connection(_self):
        return mysql.connector.connect(**st.secrets["mysql"])

    @st.experimental_memo(ttl=600)
    def query(_self, query):
        with _self.datacon.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def authenticate(self):
        self.datacon = self.start_connection()
        self.cursor = self.datacon.cursor()
        self.connected = True

    def create_aptmt(self, aptmtnm, house_list):
        command_create='create table if not exists '+ aptmtnm +' (HouseId Varchar(10) Primary Key, NumPpl Int Default 0, WaterCharge Int Default 0, NumLitres Int Default 0, OverageLitres Int Default 0)'
        self.query(command_create)
        for i in house_list:
            # UniqueHousePwd=input('Input the unique house password: ')
            command_insert='insert into '+ aptmtnm +' (HouseId) values (\''+ i +'\')'
            self.query(command_insert)

    def get_apt_names(self):
        return(self.query('Show Tables'))

    def get_home_names(self, aptname):
        command = "select houseid from {name}".format(name=aptname)
        return(self.query(command))

    def info_extract_aptmt(self, aptmt):
        command="select * from {name}".format(name = aptmt)
        return DataFrame(self.query(command), columns=['HouseID', 'Residents', 'Water Charge', 'Water Usage (Liters)', 'Overage (Liters)'])

    def info_extract_house(self, aptmt, houseid):
        command='select * from '+ aptmt +' where HouseId like \''+ houseid +'\''
        return DataFrame(self.query(command), columns=['HouseID', 'Residents', 'Water Charge', 'Water Usage (Liters)', 'Overage (Liters)'])

    def amt_wtr(self, aptmt, houseid):
        house = self.info_extract_house(aptmt, houseid)
        amt = ((house[2]/house[1])*1000) / self.wtr_tax
        return amt

    def redctn_factor_house(self, aptmt, houseid):
        house = self.info_extract_house(aptmt, houseid)
        return house[3] - self.ideal_wtr

    def redctn_factor_aptmt(self, aptmt):
        aptmt_table = self.info_extract_aptmt(aptmt)
        no_people = 0
        tot_wtr = 0
        for house in aptmt_table:
            no_people+=1
            tot_wtr+=house[3]

        avg_wtr=tot_wtr/no_people
        return avg_wtr - self.ideal_wtr

    def insert_into_house(self, aptmt, houseid, numppl):
        command='update table '+ aptmt +' set NumPpl='+ str(numppl) +' where HouseId like \''+ houseid +'\''
        self.cursor.execute(command)

    def update_into_house(self, aptmt, houseid, watercharge):
        house = self.info_extract_house(aptmt, houseid)
        command='update table '+ aptmt +' set WaterCharge='+ str(watercharge) +', NumLitres='+ str(self.amt_wtr(house)) +', OverageLitres='+ str(self.redctn_factor_house(house)) +' where HouseId like \''+ houseid +'\''
        self.cursor.execute(command)

    def money_spent_extra(self, aptmt, houseid):
        house = self.info_extract_house(aptmt, houseid)
        return house[2] - self.ideal_wtr_tax

    def clean_up(self):
        if self.connected:
            self.datacon.close()
