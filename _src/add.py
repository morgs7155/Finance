import customtkinter as ctk
import tkinter as tk
import sqlite3
from tkinter import messagebox

class AddValue():
    def __init__(self, master):
        self.master = master
        self.Setup()
        
    def Setup(self):
        self.Frames()
        self.Labels()
        self.Buttons()
    
    def Frames(self):
        self.f_select_opcion = ctk.CTkFrame(self.master, width=500, height=500, fg_color='white')
        self.f_select_opcion.pack(side=tk.TOP, expand=True)
        
        self.f_add_value = ctk.CTkFrame(self.master, width=500, height=500, fg_color='white')

    def Labels(self):
        self.l_title = ctk.CTkLabel(self.f_select_opcion, text='Finances\n\n', font=('fixedsys', 30, 'bold'), fg_color='white', text_color='black')
        self.l_title.pack(pady=5)
        
        self.l_info = ctk.CTkLabel(self.f_select_opcion, text='para adicionar um débito selecione o botão "+ gasto\n\npara adicionar um saldo selecione o botão "+ valor"\n\n\n\n', font=('Times', 20, 'bold'), fg_color='white', text_color='black')
        self.l_info.pack(pady=5)
    
    def Buttons(self):
        self.btn_add_gasto = ctk.CTkButton(self.f_select_opcion, text='+ gasto', command=self.Add_gasto, font=('Times', 15, 'bold'), fg_color='#E4080A', text_color='white', hover_color='#F57778', width=150, height=45)
        self.btn_add_gasto.pack(pady=15)
        
        self.btn_add_saldo = ctk.CTkButton(self.f_select_opcion, text='+ valor', command=self.Add_saldo, font=('Times', 15, 'bold'), fg_color='#E4080A', text_color='white', hover_color='#F57778', width=150, height=45)
        self.btn_add_saldo.pack(pady=15)
        
    def Add_gasto(self):
        self.f_select_opcion.pack_forget()
        
        self.l_name_gasto = ctk.CTkLabel(self.f_add_value, text='nome', font=('fixedsys', 15, 'bold'), fg_color='white', text_color='black')
        self.l_name_gasto.pack(side=tk.TOP, padx=5)
        
        self.e_name_g = ctk.CTkEntry(self.f_add_value, width=300, font=('Arial', 15, 'bold'))
        self.e_name_g.pack(side=tk.TOP, padx=5)
        
        self.l_valor_gasto = ctk.CTkLabel(self.f_add_value, text='Gasto a ser adicionado', font=('fixedsys', 15, 'bold'), fg_color='white', text_color='black')
        self.l_valor_gasto.pack(side=tk.TOP, padx=5)
        
        self.e_gasto = ctk.CTkEntry(self.f_add_value, width=100, font=('Arial', 15, 'bold'))
        self.e_gasto.pack(side=tk.TOP, padx=5)
        
        self.l_type_transation = ctk.CTkLabel(self.f_add_value, text='tipo de transação', font=('fixedsys', 15, 'bold'), fg_color='white', text_color='black')
        self.l_type_transation.pack(side=tk.TOP, padx=5)
        
        self.e_type_transation = ctk.CTkEntry(self.f_add_value, width=300, font=('Arial', 15, 'bold'))
        self.e_type_transation.pack(side=tk.TOP, padx=5)
        
        self.btn_add_gasto = ctk.CTkButton(self.f_add_value,command=self.Insert_values_gasto, text='Adicionar gasto', font=('Times', 15, 'bold'), fg_color='#E4080A', text_color='white', hover_color='#F57778', width=150, height=45)
        self.btn_add_gasto.pack(side=tk.TOP, pady=15)
        
        self.btn_voltar = ctk.CTkButton(self.f_add_value, text='Voltar', command=self.voltar, font=('Times', 15, 'bold'), fg_color='#E4080A', text_color='white', hover_color='#F57778', width=150, height=45)
        self.btn_voltar.pack(side=tk.TOP, pady=15)
        
        self.f_add_value.pack(side=tk.TOP, expand=True)

    def Add_saldo(self):
        self.f_select_opcion.pack_forget() 
        
        self.l_name_saldo = ctk.CTkLabel(self.f_add_value, text='nome', font=('fixedsys', 15, 'bold'), fg_color='white', text_color='black')
        self.l_name_saldo.pack(side=tk.TOP, padx=5)
        
        self.e_name_s = ctk.CTkEntry(self.f_add_value, width=300, font=('Arial', 15, 'bold'))
        self.e_name_s.pack(side=tk.TOP, padx=5)
        
        self.l_valor_saldo = ctk.CTkLabel(self.f_add_value, text='Saldo a ser adicionado', font=('fixedsys', 15, 'bold'), fg_color='white', text_color='black')
        self.l_valor_saldo.pack(side=tk.TOP, padx=5)
        
        self.e_saldo = ctk.CTkEntry(self.f_add_value, width=300, font=('Arial', 15, 'bold'))
        self.e_saldo.pack(side=tk.TOP, padx=5)
        
        self.btn_add_saldo = ctk.CTkButton(self.f_add_value, text='Adicionar saldo', command=self.Insert_values_saldo, font=('Times',  15, 'bold'), fg_color='#E4080A', text_color='white', hover_color='#F57778', width=150, height=45)
        self.btn_add_saldo.pack(side=tk.TOP, pady=15)
        
        self.btn_voltar = ctk.CTkButton(self.f_add_value, text='Voltar', command=self.voltar, font=('Times', 15, 'bold'), fg_color='#E4080A', text_color='white', hover_color='#F57778', width=150, height=45)
        self.btn_voltar.pack(side=tk.TOP, pady=15)
        
        self.f_add_value.pack(side=tk.TOP, expand=True)

    def voltar(self):
        self.f_add_value.pack_forget() 
        self.f_select_opcion.pack(side=tk.TOP, expand=True)
        
    def Insert_values_saldo(self):
        self.name_s = self.e_name_s.get().upper()
        self.saldo = self.e_saldo.get().strip()
       
        
        try:
            self.conn_p = sqlite3.connect("database/money_positive.db")
            self.cursor_p = self.conn_p.cursor()
            
            self.cursor_p.execute("INSERT INTO cash(name_value_saldo, value_positive) VALUES(?,?)",
                                (self.name_s, self.saldo))
            
            self.conn_p.commit()
            self.conn_p.close()
            
            messagebox.showinfo("saldo atualizado", "atualize a pagina para verificar o saldo atual")
        
        except sqlite3.Error as e:
            messagebox.showerror("Erro ao inserir dados", f"{e}")
    
    def Insert_values_gasto(self):
        self.name_g = self.e_name_g.get().upper()
        self.transation = self.e_type_transation.get().upper()
        self.gasto = self.e_gasto.get().strip()
       
        try:
            self.conn_p = sqlite3.connect("database/money_negative.db")
            self.cursor_p = self.conn_p.cursor()
            
            self.cursor_p.execute("INSERT INTO cash(name_value_gast, type_transation, value_negative) VALUES(?,?,?)",
                                (self.name_g, self.transation, self.gasto))
            
            self.conn_p.commit()
            self.conn_p.close()
            
            messagebox.showinfo("saldo atualizado", "atualize a pagina para verificar o saldo atual")
        
        except sqlite3.Error as e:
            messagebox.showerror("Erro ao inserir dados", f"{e}")
    


if __name__ == '__main__':
    screen = ctk.CTk()
    screen.title('Adicionar')
    screen.configure(fg_color='white')

    screen.geometry(f'500x500')
    
    app = AddValue(screen)
    
    screen.mainloop()