import pyodbc
import pymssql

class InteractWithDatabase:
    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\MSSQLSERVER_1024;'
            'DATABASE=parking_lot;'
            'Trusted_Connection=yes;')
        if self.conn:
            print("連線成功")
        else:
            print("連線失敗")
        self.cursor = self.conn.cursor()

    # 新增停車場中的單筆資料
    def insert_data(self, plate_num_value, slot_num_value):
        cursor = self.conn.cursor()
        sqlStr = "insert into ParkingRecords (plate_num, slot_num) values (?, ?)"
        cursor.execute(sqlStr, (plate_num_value, slot_num_value))
        self.conn.commit()
        return

    def add_single_data(self, state, plate_num_value):
        cursor = self.conn.cursor()
        for i in range(0, len(state)):
            for j in range(0, len(state[i])):
                if state[i][j] == plate_num_value:
                    num = i * len(state[i]) + j
                    self.insert_data(plate_num_value, num)


    # 刪除停車場中的單筆資料
    def delete_data(self, plate_num_value):
        cursor = self.conn.cursor()
        sqlStr = "delete from ParkingRecords where plate_num = ?"
        cursor.execute(sqlStr, (plate_num_value))
        self.conn.commit()
        return

    # 更新停車場中的單筆資料
    def update_data(self, plate_num_value, slot_num_value):
        cursor = self.conn.cursor()
        sqlStr = "update ParkingRecords set slot_num = ? where plate_num = ?"
        cursor.execute(sqlStr, (slot_num_value, plate_num_value))
        self.conn.commit()
        return

    # 最初將未寫入過的停車場狀態整個寫入資料庫
    def initialize_data_in_db(self, state):
        for i in range(0, len(state)):
            for j in range(0, len(state[i])):
                if state[i][j] != ' ':
                    num = i * len(state[i]) + j
                    self.insert_data(state[i][j], num)
        return

    # 將停車場移動後的狀態更新進資料庫
    def transfer_data_to_db(self, state):
        for i in range(0, len(state)):
            for j in range(0, len(state[i])):
                if state[i][j] != ' ':
                    num = i * len(state[i]) + j
                    self.update_data(state[i][j], num)
        return

    # 將單筆停車場資料寫入至相對的二維陣列上
    def arrange_the_car(self, state, plate_num_value, slot_num_value):
        width = len(state[0])
        i = slot_num_value // width
        j = slot_num_value % width
        state[i][j] = plate_num_value
        return state

    # 讀出資料庫中的停車場資料並還原成二維陣列形式
    def read(self, state):
        cursor = self.conn.cursor()
        sqlStr = "select * from ParkingRecords"
        cursor.execute(sqlStr)
        for row in cursor:
            state = self.arrange_the_car(state, row.plate_num, row.slot_num)
        return state

    # 將資料庫內所有停車資料刪除
    def clear_all_data(self):
        cursor = self.conn.cursor()
        sqlStr = "TRUNCATE TABLE ParkingRecords"
        cursor.execute(sqlStr)
        self.conn.commit()
        return

    # 關閉資料庫連線
    def close_cursor(self):
        self.cursor.close()
        self.conn.close()
