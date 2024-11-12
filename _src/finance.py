import customtkinter as ctk
from PIL import Image
import subprocess as sb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import sqlite3 as sq
from datetime import datetime

class Finance():
    def __init__(self, master):
        self.master = master
        self.Setup()
        
    def Setup(self):
        self.Frames()
        self.Icons()
        self.Labels()
        self.Buttons()
        self.Saldo()
        self.Graficos()
        self.auto_update() #atualização automática do saldo
        self.Mouth_atual()
    
    def Frames(self):
        self.f_left = ctk.CTkFrame(self.master, width=self.master.winfo_screenwidth(), height=self.master.winfo_screenheight(), fg_color='white')
        self.f_left.pack(side=tk.TOP, expand=True)
        
    def auto_update(self):
        self.Saldo()  #atualiza o saldo
        self.master.after(10000, self.auto_update)
        
    def Icons(self):
        self.icon_coin_open = Image.open('icons/dollar.png')
        self.icon_coin_resize = self.icon_coin_open.resize((50, 50), Image.Resampling.LANCZOS)
        self.icon_coin_ofc = ctk.CTkImage(self.icon_coin_resize, size=(50, 50))
        
        self.l_icon_coin = ctk.CTkLabel(self.f_left, image=self.icon_coin_ofc, text='')
        self.l_icon_coin.place(x=1180, y=20) 
    
    def Labels(self):
        self.l_title = ctk.CTkLabel(self.f_left, text='F I N A N C E\n𝓜𝓪𝓻𝓺𝓾𝓮𝓼', font=('Fixedsys', 32, 'bold'), fg_color='white', text_color='black')
        self.l_title.place(x=600, y=50)
        
        self.l_month = ctk.CTkLabel(self.f_left, text='agosto', font=('Times', 20, 'bold'), fg_color='white', text_color='black')
        self.l_month.place(x=200, y=110)
        
        self.l_cash_atual = ctk.CTkLabel(self.f_left, text='', font=('Times', 20, 'bold'), fg_color='white', text_color='black')
        self.l_cash_atual.place(x=1250, y=30)
        
    def Buttons(self):
        self.btn_extract = ctk.CTkButton(self.f_left, text='extrato',command=self.Open_extract, font=('Times', 15, 'bold'), fg_color='#E4080A', text_color='white', hover_color='#F57778', width=150, height=45)
        self.btn_extract.place(x=1150, y=590)
        
        self.btn_add = ctk.CTkButton(self.f_left, text='adicionar', command=self.Open_Add, font=('Times', 15, 'bold'), fg_color='#E4080A', text_color='white', hover_color='#F57778', width=150, height=45)
        self.btn_add.place(x=1150, y=640)
        
    def Graficos(self):
        total_recebido = sum(self.value_positive)
        total_gasto = sum(self.value_negative)
        
        labels = ["Total Recebido", "Total Gasto"]
        sizes = [total_recebido, total_gasto]  #dados do gráfico
        colors = ['lightblue', 'lightcoral']
        
        #gráfico de pizza
        fig, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  #manter o gráfico circular

        canvas = FigureCanvasTkAgg(fig, master=self.f_left)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=150)


    def Open_Add(self):
        sb.Popen(["python", "_src/add.py"])
        
    def Open_extract(self):
        sb.Popen(["python", "_src/extract.py"])
        
    def Saldo(self):
        self.conn_p = sq.connect('database/money_positive.db')
        self.conn_n = sq.connect('database/money_negative.db')
        
        self.cursor_p = self.conn_p.cursor()
        self.cursor_n = self.conn_n.cursor()  
        
        # Valores positivos
        self.cursor_p.execute("SELECT value_positive FROM cash")
        self.value_positive = [value[0] for value in self.cursor_p.fetchall()]
        
        # Valores negativos
        self.cursor_n.execute("SELECT value_negative FROM cash")
        self.value_negative = [value[0] for value in self.cursor_n.fetchall()]
        
        saldo_total = sum(self.value_positive) - sum(self.value_negative)
        
        self.value_txt = f'{saldo_total:.2f}'  #formatar para decimal
        self.l_cash_atual.configure(text=f'{self.value_txt} R$')
        
        self.conn_p.close()
        self.conn_n.close()
        
    def Mouth_atual(self):
        self.date_atual = datetime.now()
        
        self.month_atual = self.date_atual.strftime("%B")
        
        self.l_month.configure(text=f'{self.month_atual}')

 

if __name__ == '__main__':
    screen = ctk.CTk()
    screen.title('Finance App')
    screen.tk.call('tk', 'scaling', 1.0)

    screen.geometry(f'{screen.winfo_screenwidth()}x{screen.winfo_screenheight()}')
    
    app = Finance(screen)
    
    screen.mainloop()