import mysql.connector
import streamlit as st
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

class Aqualog:

    def __init__(self):
        self.wtr_tax = 7 # Bangalore water charge is Rs. 7 per kilolitre. This may change.
        self.ideal_wtr = 4050
        self.ideal_wtr_tax = 4.05 * self.wtr_tax
        self.connected = False
        self.datacon = None
        self.cursor = None
        self.li_house_id, self.li_numlitres = [], []
        self.li_house_id, self.li_money = [], []
    
    @st.experimental_singleton
    def start_connection(_self):
        return mysql.connector.connect(**st.secrets["mysql"])

    @st.experimental_memo(ttl=60)
    def query(_self, query):
        with _self.datacon.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def authenticate(self):
        self.datacon = self.start_connection()
        self.cursor = self.datacon.cursor()
        self.connected = True

    def create_aptmt(self, aptmtnm, house_list):
        command_create='create table if not exists '+ aptmtnm +' (HouseId Varchar(10) Primary Key, NumPpl Int, WaterCharge Int, NumLitres Int, OverageLitres Int)'
        self.query(command_create)
        for i in house_list:
            # UniqueHousePwd=input('Input the unique house password: ')
            command_insert='insert into '+ aptmtnm +' values (\''+ i +'\', 0, 1, 0, 0)'
            self.query(command_insert)

    def get_apt_names(self):
        return(self.query('Show Tables'))

    def get_home_names(self, aptname):
        command = "select houseid from {name}".format(name=aptname)
        return(self.query(command))

    def info_extract_aptmt(self, aptmt, returnDF=False):
        command="select * from {name}".format(name = aptmt)
        return DataFrame(self.query(command), columns=['HouseID', 'Residents', 'Water Charge', 'Water Usage (Liters)', 'Overage (Liters)'])

    def info_extract_house(self, aptmt, houseid, returnDF=False):
        command='select * from '+ aptmt +' where HouseId like \''+ houseid +'\''
        output = self.query(command)
        if returnDF:
            return DataFrame(self.query(command), columns=['HouseID', 'Residents', 'Water Charge', 'Water Usage (Liters)', 'Overage (Liters)'])
        else:
            return output
        
    def amt_wtr(self, aptmt, houseid):
        house = self.info_extract_house(aptmt, houseid)
        peppl=int(house[2])/house[1]
        amt=0
        if peppl>56:
            if peppl-56>187:
                if peppl-187-56>625:
                    amt+=int(((peppl-625-187-56)*1000)/45)+int(((625)*1000)/25)+int(((187)*1000)/11)+int(((56)*1000)/7)
                else:
                    amt+=int(((peppl-187-56)*1000)/25)+int(((187)*1000)/11)+int(((56)*1000)/7)
            else:
                amt+=int(((peppl-56)*1000)/11)+int(((56)*1000)/7)
        else:
            amt+=int((peppl)*1000)/7
        return int(amt)

    def redctn_factor_house(self, aptmt, houseid):
        house = self.info_extract_house(aptmt, houseid, returnDF=False)
        return int(house[0][3] - self.ideal_wtr)

    def redctn_factor_aptmt(self, aptmt):
        aptmt_table = self.info_extract_aptmt(aptmt)
        no_people = 0
        tot_wtr = 0
        for house in aptmt_table:
            no_people+=1
            tot_wtr+=house[3]

        avg_wtr=tot_wtr/no_people
        return int(avg_wtr - self.ideal_wtr)

    def insert_into_house(self, aptmt, houseid, numppl):
        command = "update "+ aptmt +' set NumPpl = '+ str(numppl) +" WHERE HouseId like \'" + houseid + '\''
        self.query(command)
        self.datacon.commit()

    def update_into_house(self, aptmt, houseid, watercharge):
        command_update_1='update '+ aptmt +' set WaterCharge='+ str(watercharge) +' where HouseId like \''+ houseid +'\''
        self.query(command_update_1)
        self.datacon.commit()
        house = self.info_extract_house(aptmt, houseid)
        peppl=int(watercharge)/house[1]
        amt=0
        if peppl>56:
            if peppl-56>187:
                if peppl-187-56>625:
                    amt+=int(((peppl-625-187-56)*1000)/45)+int(((625)*1000)/25)+int(((187)*1000)/11)+int(((56)*1000)/7)
                else:
                    amt+=int(((peppl-187-56)*1000)/25)+int(((187)*1000)/11)+int(((56)*1000)/7)
            else:
                amt+=int(((peppl-56)*1000)/11)+int(((56)*1000)/7)
        else:
            amt+=int((peppl)*1000)/7
        command_update_2='update '+ aptmt +' set NumLitres='+ str(amt) +' where HouseId like \''+ houseid +'\''
        self.query(command_update_2)
        self.datacon.commit()
        overagelitres=int(amt - self.ideal_wtr)
        command_update_3='update '+ aptmt +' set OverageLitres='+ str(overagelitres) +' where HouseId like \''+ houseid +'\''
        self.query(command_update_3)
        self.datacon.commit()

    def money_spent_extra(self, aptmt, houseid):
        house = self.info_extract_house(aptmt, houseid)
        return house[2] - self.ideal_wtr_tax

# Display Functions 
    def disp_litres_house(self, aptmt, houseid):
        house=self.info_extract_house(aptmt, houseid)
        x = np.array([houseid, 'Ideal House'])
        y = np.array([house[3], self.ideal_water])
        df = pd.DataFrame({"Ideal":x, "Liters":y})
        return df

    def disp_money_house(self, aptmt, houseid):
        house=self.info_extract_house(aptmt, houseid)
        x = np.array([houseid, 'Ideal House'])
        y = np.array([house[2], self.ideal_wtr_tax])
        df = pd.DataFrame({"HouseID":x, "Amount":y})
        return df

    def disp_litres_apartment(self, aptmt):
        aptmt_table=self.info_extract_aptmt(aptmt)
        
        for house in aptmt_table:
            self.li_house_id.append(house[0])
            self.li_numlitres.append(int(house[3]))
        df = pd.DataFrame(list(zip(self.li_house_id, self.li_numlitres)), 
                            columns=['HouseID', 'Water Usage'])
        df.set_index('HouseID')
        return df
        
    def disp_money_apartment(self, aptmt):
        aptmt_table=self.info_extract_aptmt(aptmt)
        
        for house in aptmt_table:
            self.li_house_id.append(house[0])
            self.li_numlitres.append(house[2])
        df = pd.DataFrame(list(zip(self.li_house_id, self.li_money)), 
                            columns=['HouseID', 'Water Usage'])
        df.set_index('HouseID')
        return df

    def clean_up(self):
        if self.connected:
            self.datacon.close()
