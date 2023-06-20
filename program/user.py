import requests
import sqlite3
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
from config import host


class GuiWindowUser(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.style = ttk.Style(theme='darkly')
        self.title('title')
        width = 1060
        height = 700

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.resizable(False,False)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        # _________________________________________________
        conn = sqlite3.connect('./db/AccessLogi.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM files")
        conn.commit()

        response = requests.get(f'http://{host}:5000/logs')
        file_json = response.json()

        ip = []
        time = []

        for i in file_json:
            ip.append(i['ip_address'])
            time.append(i['request_time'])


        for i in range(len(ip)):
            cursor.execute('INSERT INTO files (ip, time) VALUES (?, ?)', (ip[i], time[i]))

        conn.commit()

        # _________________________________________________
        notebook = ttk.Notebook(self, bootstyle='success')
        notebook.pack(expand=True, fill=BOTH)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        tab1.pack(fill=BOTH, expand=True)
        tab2.pack(fill=BOTH, expand=True)
        # _________________________________________________
        notebook_filtr = ttk.Notebook(tab2, bootstyle='success')
        notebook_filtr.pack(expand=True, fill=BOTH)

        tab_filtr1 = ttk.Frame(notebook_filtr)
        tab_filtr2 = ttk.Frame(notebook_filtr)
        tab_filtr3 = ttk.Frame(notebook_filtr)

        tab_filtr1.pack(fill=BOTH, expand=True)
        tab_filtr2.pack(fill=BOTH, expand=True)
        tab_filtr3.pack(fill=BOTH, expand=True)


        # treeview________________________________________
        columns = ('ip','times')

        treeview = ttk.Treeview(tab1, bootstyle="success",columns=columns,show='headings')
        treeview.pack(pady=10)

        for c in columns:
            treeview.heading(c, text=c)

        # наполняем treeview данными
        cursor.execute("""SELECT ip, time FROM files""")
        values = cursor.fetchall()

        for value in values:
            treeview.insert('', END, values=value)

        # update___________________________________________
        def update():
            cursor.execute("DELETE FROM files")
            conn.commit()

            response = requests.get(f'http://{host}:5000/logs')
            file_json = response.json()

            ip = []
            time = []

            for i in file_json:
                ip.append(i['ip_address'])
                time.append(i['request_time'])


            for i in range(len(ip)):
                cursor.execute('INSERT INTO files (ip, time) VALUES (?, ?)', (ip[i], time[i]))

            treeview.delete(*treeview.get_children()) 

            cursor.execute("""SELECT ip, time FROM files""")
            values = cursor.fetchall()

            for value in values:
                treeview.insert('',END,values=value)

            status_label.config(text="success")

            conn.commit()

        # Фильтр_по_ip_____________________________________
        def filtr_ip():

            ip = ip_entry.get()

            if not ip:
                ip_status_label.config(text="IP-адрес не указан")
                return

            try:
                response = requests.get(f'http://{host}:5000/logs?ip={ip}')
                response.raise_for_status()  # Проверка на успешный запрос
                file_json = response.json()
            except requests.exceptions.HTTPError as error:
                # Обработка ошибки запроса
                print(error)
                return
            except ValueError as error:
                # Обработка ошибки JSON-ответа
                print(error)
                return

            cursor.execute("DELETE FROM files")
            conn.commit()

            ip = []
            time = []

            for i in file_json:
                ip.append(i['ip_address'])
                time.append(i['request_time'])


            for i in range(len(ip)):
                cursor.execute('INSERT INTO files (ip, time) VALUES (?, ?)', (ip[i], time[i]))

            treeview.delete(*treeview.get_children()) 

            cursor.execute("""SELECT ip, time FROM files""")
            values = cursor.fetchall()

            for value in values:
                treeview.insert('',END,values=value)

            ip_status_label.config(text="success")

            conn.commit()

        # Фильтр_по_start_date_and_end_date_________________
        def start_date_and_end_date():

            day = day_entry.get()
            month = combo_month.get()
            year = year_entry.get()

            end_day = day_entry_end.get()
            end_month = combo_month_end.get()
            end_year = year_entry_end.get()

            if not all([day, month, year, end_day, end_month, end_year]):
            # Обработка пустых полей
                info2.config(text="Все поля должны быть заполнены")
                return


            try:
                response = requests.get(f'http://{host}:5000/logs?start_date={day}/{month}/{year}&end_date={end_day}/{end_month}/{end_year}')
                response.raise_for_status()  # Проверка на успешный запрос
                file_json = response.json()
            except requests.exceptions.HTTPError as error:
                # Обработка ошибки запроса
                info2.config(text="error")
                print(error)
                return
            except ValueError as error:
                # Обработка ошибки JSON-ответа
                info2.config(text="error")
                print(error)
                return

            cursor.execute("DELETE FROM files")
            conn.commit()

            ip = []
            time = []

            for i in file_json:
                ip.append(i['ip_address'])
                time.append(i['request_time'])


            for i in range(len(time)):
                cursor.execute('INSERT INTO files (ip, time) VALUES (?, ?)', (ip[i], time[i]))

            treeview.delete(*treeview.get_children()) 

            cursor.execute("""SELECT ip, time FROM files""")
            values = cursor.fetchall()

            for value in values:
                treeview.insert('',END,values=value)

            info2.config(text="success")

            conn.commit()

        # Фильтр_по_всем___________________________________
        def filter_all():

            day2 = day_entry2.get()
            month2 = combo_month2.get()
            year2 = year_entry2.get()

            end_day2 = day_entry_end2.get()
            end_month2 = combo_month_end2.get()
            end_year2 = year_entry_end2.get()

            ip2 = ip_entry2.get()

            if not all([day2, month2, year2, end_day2, end_month2, end_year2, ip2]):
                info3.config(text="Все поля должны быть заполнены")
                return


            try:
                response = requests.get(f'http://{host}:5000/logs?start_date={day2}/{month2}/{year2}&end_date={end_day2}/{end_month2}/{end_year2}&ip={ip2}')
                file_json = response.json()
            except requests.exceptions.HTTPError as error:
                # Обработка ошибки запроса
                info3.config(text="error")
                print(error)
                return
            except ValueError as error:
                # Обработка ошибки JSON-ответа
                info3.config(text="error")
                print(error)
                return
            
            cursor.execute("DELETE FROM files")
            conn.commit()

            ip = []
            time = []

            for i in file_json:
                ip.append(i['ip_address'])
                time.append(i['request_time'])


            for i in range(len(time)):
                cursor.execute('INSERT INTO files (ip, time) VALUES (?, ?)', (ip[i], time[i]))

            treeview.delete(*treeview.get_children()) 

            cursor.execute("""SELECT ip, time FROM files""")
            values = cursor.fetchall()

            for value in values:
                treeview.insert('',END,values=value)

            info3.config(text="success")

            conn.commit()

        # _________________________________________________

        but = Button(tab1 , text="update", font=('arial', 15), width=30, command=update)
        but.pack(pady=10)

        status_label = tk.Label(tab1, text='')
        status_label.pack(pady=10)

        # _________________________________________________tab_filtr1
        lbl_ip = Label(tab_filtr1 , text="Напишите ip", font=('arial', 25), bd=18)
        lbl_ip.pack(pady=10)

        ip_entry = Entry(tab_filtr1 , font=('arial', 20), width=15)
        ip_entry.pack(pady=10)

        btn1 = Button(tab_filtr1 , text="Выполнить", font=('arial', 15), width=30, command=filtr_ip)
        btn1.pack(pady=10)

        ip_status_label = tk.Label(tab_filtr1, text='')
        ip_status_label.pack(pady=10)

        # _________________________________________________tab_filtr2

        label_start_date = Label(tab_filtr2 , text="start_date", font=('arial', 25), bd=18)
        label_start_date.pack(pady=10)
        label_start_date.place(x=80, y=60)

        lbl_day = Label(tab_filtr2 , text="Напишите день", font=('arial', 25), bd=18)
        lbl_day.pack(pady=10)
        lbl_day.place(x=80, y=120)

        day_entry = Entry(tab_filtr2 , font=('arial', 20), width=15)
        day_entry.pack(pady=10)
        day_entry.place(x=100, y=180)

        lbl_month = Label(tab_filtr2 , text="Выберите месяц", font=('arial', 25), bd=18)
        lbl_month.pack(pady=10)
        lbl_month.place(x=80, y=240)

        monthID = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        combo_month = ttk.Combobox(tab_filtr2, font=('arial', 15), values=monthID)
        combo_month.pack(pady=10)
        combo_month.place(x=100, y=300)

        lbl_year = Label(tab_filtr2 , text="Напишите год", font=('arial', 25), bd=18)
        lbl_year.pack(pady=10)
        lbl_year.place(x=80, y=340)

        year_entry = Entry(tab_filtr2 , font=('arial', 20), width=15)
        year_entry.pack(pady=10)
        year_entry.place(x=100, y=420)

        # _________________________________________________tab_filtr2

        label_end_date = Label(tab_filtr2 , text="end_date", font=('arial', 25), bd=18)
        label_end_date.pack(pady=10)
        label_end_date.place(x=680, y=60)

        lbl_day_end = Label(tab_filtr2 , text="Напишите день", font=('arial', 25), bd=18)
        lbl_day_end.pack(pady=10)
        lbl_day_end.place(x=680, y=120)

        day_entry_end = Entry(tab_filtr2 , font=('arial', 20), width=15)
        day_entry_end.pack(pady=10)
        day_entry_end.place(x=700, y=180)

        lbl_month_end = Label(tab_filtr2 , text="Выберите месяц", font=('arial', 25), bd=18)
        lbl_month_end.pack(pady=10)
        lbl_month_end.place(x=680, y=240)

        monthID_end = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        combo_month_end = ttk.Combobox(tab_filtr2, font=('arial', 15), values=monthID_end)
        combo_month_end.pack(pady=10)
        combo_month_end.place(x=700, y=300)

        lbl_year_end = Label(tab_filtr2 , text="Напишите год", font=('arial', 25), bd=18)
        lbl_year_end.pack(pady=10)
        lbl_year_end.place(x=680, y=340)

        year_entry_end = Entry(tab_filtr2 , font=('arial', 20), width=15)
        year_entry_end.pack(pady=10)
        year_entry_end.place(x=700, y=420)

        btn2 = Button(tab_filtr2 , text="Выполнить", font=('arial', 18), width=30, command=start_date_and_end_date)
        btn2.pack(pady=10)
        btn2.place(x=300, y=500)

        
        info2 = tk.Label(tab_filtr2, text='')
        info2.pack(pady=10)
        info2.place(x=420, y=580)

        # _________________________________________________tab_filtr3

        lbl_ip2 = Label(tab_filtr3 , text="Напишите ip", font=('arial', 25), bd=18)
        lbl_ip2.pack(pady=10)
        lbl_ip2.place(x=400, y=240)

        ip_entry2 = Entry(tab_filtr3 , font=('arial', 20), width=15)
        ip_entry2.pack(pady=10)
        ip_entry2.place(x=400, y=300)

        # _________________________________________________

        label_start_date2 = Label(tab_filtr3 , text="start_date", font=('arial', 25), bd=18)
        label_start_date2.pack(pady=10)
        label_start_date2.place(x=80, y=60)

        lbl_day2 = Label(tab_filtr3 , text="Напишите день", font=('arial', 25), bd=18)
        lbl_day2.pack(pady=10)
        lbl_day2.place(x=80, y=120)

        day_entry2 = Entry(tab_filtr3 , font=('arial', 20), width=15)
        day_entry2.pack(pady=10)
        day_entry2.place(x=100, y=180)

        lbl_month2 = Label(tab_filtr3 , text="Выберите месяц", font=('arial', 25), bd=18)
        lbl_month2.pack(pady=10)
        lbl_month2.place(x=80, y=240)

        monthID2 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        combo_month2 = ttk.Combobox(tab_filtr3, font=('arial', 15), values=monthID2)
        combo_month2.pack(pady=10)
        combo_month2.place(x=100, y=300)

        lbl_year2 = Label(tab_filtr3 , text="Напишите год", font=('arial', 25), bd=18)
        lbl_year2.pack(pady=10)
        lbl_year2.place(x=80, y=340)

        year_entry2 = Entry(tab_filtr3 , font=('arial', 20), width=15)
        year_entry2.pack(pady=10)
        year_entry2.place(x=100, y=420)

        # _________________________________________________

        label_end_date2 = Label(tab_filtr3 , text="end_date", font=('arial', 25), bd=18)
        label_end_date2.pack(pady=10)
        label_end_date2.place(x=680, y=60)

        lbl_day_end2 = Label(tab_filtr3 , text="Напишите день", font=('arial', 25), bd=18)
        lbl_day_end2.pack(pady=10)
        lbl_day_end2.place(x=680, y=120)

        day_entry_end2 = Entry(tab_filtr3 , font=('arial', 20), width=15)
        day_entry_end2.pack(pady=10)
        day_entry_end2.place(x=700, y=180)

        lbl_month_end2 = Label(tab_filtr3 , text="Выберите месяц", font=('arial', 25), bd=18)
        lbl_month_end2.pack(pady=10)
        lbl_month_end2.place(x=680, y=240)

        monthID_end2 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        combo_month_end2 = ttk.Combobox(tab_filtr3, font=('arial', 15), values=monthID_end2)
        combo_month_end2.pack(pady=10)
        combo_month_end2.place(x=700, y=300)

        lbl_year_end2 = Label(tab_filtr3 , text="Напишите год", font=('arial', 25), bd=18)
        lbl_year_end2.pack(pady=10)
        lbl_year_end2.place(x=680, y=340)

        year_entry_end2 = Entry(tab_filtr3 , font=('arial', 20), width=15)
        year_entry_end2.pack(pady=10)
        year_entry_end2.place(x=700, y=420)

        btn3 = Button(tab_filtr3 , text="Выполнить", font=('arial', 18), width=30, command=filter_all)
        btn3.pack(pady=10)
        btn3.place(x=300, y=500)

        info3 = tk.Label(tab_filtr3, text='')
        info3.pack(pady=10)
        info3.place(x=420, y=580)

        # _________________________________________________

        notebook_filtr.add(tab_filtr1,text='Фильтр по ip')
        notebook_filtr.add(tab_filtr2,text='Фильтр по start_date и end_date')
        notebook_filtr.add(tab_filtr3,text='Фильтр по всем')

        # _________________________________________________
        notebook.add(tab1,text='База данных')
        notebook.add(tab2,text='Фильтр')