import sqlite3


class Database():
    def __init__(self):
        self.Data_cash_saldo()
        self.Data_values()
        self.Data_cash_gast()
        
    def Data_cash_saldo(self):
        self.conn_p = sqlite3.connect("database/money_positive.db")
        self.cursor_p = self.conn_p.cursor()
        
        self.cursor_p.execute(
            """CREATE TABLE IF NOT EXISTS cash(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_value_saldo TEXT, 
                value_positive REAL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );"""
                )
        
        self.conn_p.commit()
        self.conn_p.close()
        
    def Data_cash_gast(self):
        self.conn_n = sqlite3.connect("database/money_negative.db")
        self.cursor_n = self.conn_n.cursor()
        
        self.cursor_n.execute(
            """CREATE TABLE IF NOT EXISTS cash(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_value_gast TEXT,
                type_transation TEXT,
                value_negative REAL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );"""
                )
        
        self.conn_n.commit()
        self.conn_n.close()
        
        
if __name__ == '__main__':
    Database()