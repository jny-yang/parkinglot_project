import psycopg2

class InteractWithDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="dpg-d38hk4fdiees73cja7d0-a",     # Render 提供的 Host
            database="parkinglot_db_hgx4",    # 例如 parkinglot_db
            user="parkinglot_db_hgx4_user",        # 例如 postgres
            password="wRM4JC6BG0NFvuJqFHFtlfu5m2DatiP7",          # Render 提供的密碼
            port=5432
        )
        if self.conn:
            print("連線成功")
        else:
            print("連線失敗")
        self.cursor = self.conn.cursor()

    # 新增停車場中的單筆資料
    def insert_data(self, plate_num_value, slot_num_value):
        cursor = self.conn.cursor()
        sqlStr = "INSERT INTO ParkingRecords (plate_num, slot_num) VALUES (%s, %s)"
        cursor.execute(sqlStr, (plate_num_value, slot_num_value))
        self.conn.commit()
        return

    # 新增停車場中的單筆資料（避免重複插入）
    def insert_data(self, plate_num_value, slot_num_value):
        cursor = self.conn.cursor()
        sqlStr = """
            INSERT INTO ParkingRecords (plate_num, slot_num)
            VALUES (%s, %s)
            ON CONFLICT (plate_num) DO UPDATE SET slot_num = EXCLUDED.slot_num;
        """
        cursor.execute(sqlStr, (plate_num_value, slot_num_value))
        self.conn.commit()
        return

    def add_single_data(self, state, plate_num_value):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == plate_num_value:
                    num = i * len(state[i]) + j
                    self.insert_data(plate_num_value, num)

    # 刪除停車場中的單筆資料
    def delete_data(self, plate_num_value):
        cursor = self.conn.cursor()
        sqlStr = "DELETE FROM ParkingRecords WHERE plate_num = %s"
        cursor.execute(sqlStr, (plate_num_value,))
        self.conn.commit()
        return

    # 更新停車場中的單筆資料
    def update_data(self, plate_num_value, slot_num_value):
        cursor = self.conn.cursor()
        sqlStr = "UPDATE ParkingRecords SET slot_num = %s WHERE plate_num = %s"
        cursor.execute(sqlStr, (slot_num_value, plate_num_value))
        self.conn.commit()
        return

    # 最初將未寫入過的停車場狀態整個寫入資料庫
    def initialize_data_in_db(self, state):
        cursor = self.conn.cursor()
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != ' ':
                    num = i * len(state[i]) + j
                    # 呼叫 PostgreSQL 版 insert
                    self.insert_data(state[i][j], num)
        return

    # 將停車場移動後的狀態更新進資料庫
    def transfer_data_to_db(self, state):
        cursor = self.conn.cursor()
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != ' ':
                    num = i * len(state[i]) + j
                    # 呼叫 PostgreSQL 版 update_data
                    self.update_data(state[i][j], num)
        return

    def arrange_the_car(self, state, plate_num_value, slot_num_value):
        width = len(state[0])
        i = slot_num_value // width
        j = slot_num_value % width
        state[i][j] = plate_num_value
        return state

    # 讀出資料庫中的停車場資料並還原成二維陣列形式
    def read(self, state):
        cursor = self.conn.cursor()
        sqlStr = "SELECT * FROM ParkingRecords"
        cursor.execute(sqlStr)
        rows = cursor.fetchall()  # 取得所有資料
        for row in rows:
            plate_num_value = row[0]  # 第一欄是 plate_num
            slot_num_value = row[1]  # 第二欄是 slot_num
            state = self.arrange_the_car(state, plate_num_value, slot_num_value)
        return state

    # 將資料庫內所有停車資料刪除
    def clear_all_data(self):
        cursor = self.conn.cursor()
        sqlStr = "TRUNCATE TABLE ParkingRecords RESTART IDENTITY"
        cursor.execute(sqlStr)
        self.conn.commit()
        return

    # 關閉資料庫連線
    def close_connection(self):
        self.conn.close()
