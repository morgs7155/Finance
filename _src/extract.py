import customtkinter as ctk
import tkinter as tk
from PIL import Image
import sqlite3
from tkinter import messagebox
from datetime import datetime

class Extract():
    def __init__(self, master):
        self.master = master
        self.Setup()

    def Setup(self):
        self.Frames()
        self.Icons()
        self.Labels()
        self.Combo_box()
        self.Buttons()

    def Frames(self):
        # Frame principal
        self.f_extrato = ctk.CTkFrame(self.master, width=800, height=600, fg_color='white')
        self.f_extrato.pack(side=tk.TOP)

        # Frame de lista com Canvas para rolagem
        self.canvas = tk.Canvas(self.f_extrato, bg="white", width=800, height=600)
        self.scrollbar = tk.Scrollbar(self.f_extrato, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Frame para adicionar os itens dentro do canvas
        self.f_list = ctk.CTkFrame(self.canvas, width=800, height=600, fg_color='white')
        self.canvas.create_window((0, 0), window=self.f_list, anchor="nw")

        # Atualizando a região visível da tela
        self.f_list.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Vincula o evento do scroll do mouse ao Canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        # Ajusta a rolagem com o movimento do mouse
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def Icons(self):
        self.icon_search_open = Image.open('icons/search.png')
        self.icon_search_resize = self.icon_search_open.resize((50, 50), Image.Resampling.LANCZOS)
        self.icon_search_ofc = ctk.CTkImage(self.icon_search_resize, size=(30, 30))

    def Labels(self):
        pass

    def Buttons(self):
        self.btn_search_month = ctk.CTkButton(self.f_extrato, text='', fg_color='white', text_color='white', hover_color='#f4f4f4', width=50, height=25, image=self.icon_search_ofc, command=self.Load_Extract)
        self.btn_search_month.place(x=730, y=10)

    def Combo_box(self):
        self.months = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        
        self.cb_box = ctk.CTkComboBox(self.f_extrato, width=300, font=('Arial', 15, 'bold'), values=self.months)
        self.cb_box.place(x=420, y=15)

    def Load_Extract(self):
        # Limpa os extratos anteriores
        for widget in self.f_list.winfo_children():
            widget.destroy()

        selected_month = self.cb_box.get()

        if not selected_month:
            messagebox.showwarning("Selecione o mês", "Por favor, selecione um mês.")
            return
        
        # Mapeando os meses para o datetime conseguir pesquisar os meses
        months_mapping = {
            'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5,
            'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10,
            'novembro': 11, 'dezembro': 12
        }
        
        month_number = months_mapping[selected_month]

        self.conn_p = sqlite3.connect('database/money_positive.db')
        self.conn_n = sqlite3.connect('database/money_negative.db')

        self.cursor_p = self.conn_p.cursor()
        self.cursor_n = self.conn_n.cursor()

        query_p = f"SELECT name_value_saldo, value_positive, created_at FROM cash WHERE strftime('%m', created_at) = '{month_number:02d}'"
        self.cursor_p.execute(query_p)
        positive_records = self.cursor_p.fetchall()

        query_n = f"SELECT name_value_gast, value_negative, created_at FROM cash WHERE strftime('%m', created_at) = '{month_number:02d}'"
        self.cursor_n.execute(query_n)
        negative_records = self.cursor_n.fetchall()

        self.Display_Extracts(positive_records, 'Recebido', 'green')
        self.Display_Extracts(negative_records, 'Gasto', 'red')

        self.conn_p.close()
        self.conn_n.close()

    def Display_Extracts(self, records, type_label, color):
        for record in records:
            # Puxando os dados do banco
            if type_label == 'Recebido':
                name = record[0]  # name_value_saldo
                value = record[1]  # value_positive
            else:
                name = record[0]  # name_value_gast
                value = record[1]  # value_negative
            
            created_at = record[2]
            date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            formatted_date = date.strftime("%d/%m/%Y %H:%M")

            # Cria um novo frame para o extrato
            extract_frame = ctk.CTkFrame(self.f_list, fg_color='white', border_width=1, corner_radius=10, height=80)
            extract_frame.pack(fill=tk.X, pady=5)

            label_type = ctk.CTkLabel(extract_frame, text=type_label, font=('Arial', 12, 'bold'), text_color=color)
            label_type.pack(side=tk.LEFT, padx=10, pady=10)

            label_name = ctk.CTkLabel(extract_frame, text=name, font=('Arial', 12, 'bold'), text_color='black')
            label_name.pack(side=tk.LEFT, padx=10, pady=10)

            label_value = ctk.CTkLabel(extract_frame, text=f"R$ {value:.2f}", font=('Arial', 12, 'bold'))
            label_value.pack(side=tk.LEFT, padx=10, pady=10)

            label_date = ctk.CTkLabel(extract_frame, text=formatted_date, font=('Arial', 12))
            label_date.pack(side=tk.LEFT, padx=10, pady=10)


if __name__ == '__main__':
    screen = ctk.CTk()
    screen.title('Extrato')
    screen.configure(fg_color='white')

    screen.geometry(f'800x600')
    
    app = Extract(screen)
    
    screen.mainloop()
