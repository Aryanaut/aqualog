import mysql.connector
import streamlit as st

class Aqualog:

    def __init__(self):
        self.wtr_tax = 7 # Bangalore water charge is Rs. 7 per kilolitre. This may change.
        self.ideal_wtr = 4050
        self.ideal_wtr_tax = 4.05 * self.wtr_tax
        self.connected = False
    
    @st.experimental_singleton
    def start_connection():
        return mysql.connector.connect(**st.secrets["mysql"])

    def authenticate(self, userid, code):
        self.datacon = self.start_connection()
        self.cursor = self.datacon.cursor()

    @st.experimental_memo()
    def query(self, query):
        with self.datacon.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def create_aptmt(self, aptmtnm, num_houses):
        command_create='create table '+ aptmtnm +' (HouseId Varchar(10) Primary Key, NumPpl Int Default 0, WaterCharge Int Default 0, NumLitres Int Default 0, OverageLitres Int Default 0)'
        self.cursor.execute(command_create)
        for i in range(num_houses):
            HouseId=input('Input the unique HouseId: ')
            # UniqueHousePwd=input('Input the unique house password: ')
            command_insert='insert into '+ aptmtnm +' (HouseId) values (\''+ HouseId +'\')'
            self.cursor.execute(command_insert)

    def info_extract_aptmt(self, aptmt):
        command='select * from '+ aptmt
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def info_extract_house(self, aptmt, houseid):
        command='select * from '+ aptmt +' where HouseId like \''+ houseid +'\''
        self.cursor.execute(command)
        return self.cursor.fetone()

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
        command='update table '+ aptmt +' set WaterCharge='+ str(watercharge) +', NumLitres='+ str(amt_wtr(house)) +', OverageLitres='+ str(redctn_factor_house(house)) +' where HouseId like \''+ houseid +'\''
        self.cursor.execute(command)

    def money_spent_extra(self, aptmt, houseid):
        house = self.info_extract_house(aptmt, houseid)
        return house[2] - self.ideal_wtr_tax

    def clean_up(self):
        if self.connected:
            self.datacon.close()
