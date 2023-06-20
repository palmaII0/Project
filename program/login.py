import pymysql
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
from register import RegisterWindow
from user import GuiWindowUser
from config import host, user, password, database

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.style = ttk.Style(theme='darkly')
        self.title('LoginWindow')
        width = 650 
        height = 500 

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.resizable(False,False)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

        def login():
            try:
                mydb = pymysql.connect(
                    host = host,
                    port = 3306,
                    user = user,
                    password = password,
                    database = database,
                    cursorclass = pymysql.cursors.DictCursor
                )

                try:
                    with mydb.cursor() as cursor:
                        username = username_entry.get()
                        passwords = password_entry.get()

                        cursor.execute(f"SELECT * FROM Users WHERE Login ='{username}' AND Password = '{passwords}'")
                        users = cursor.fetchone()

                        if users is not None:
                            login_status_label.config(text="Авторизация успешна")
                            gui = GuiWindowUser(self)
                            gui.grab_set()
                        else:
                            login_status_label.config(text="Ошибка авторизации")

                        cursor.close()
                        
                finally:
                    mydb.close()
                    print('База данных закрыта')
            except Exception as ex:
                print(ex)


        def RegistrationWindow():

            RegisterWindow()

        # ____________________LOGIN_____________________________
        LoginFrame = Frame(self)
        LoginFrame.pack(side=TOP, pady=40)

        lbl_username = Label(LoginFrame , text="Username:", font=('arial', 25), bd=18)
        lbl_username.grid(row=1)

        lbl_password = Label(LoginFrame , text="Password:", font=('arial', 25), bd=18)
        lbl_password.grid(row=2)

        username_entry = Entry(LoginFrame , font=('arial', 20), width=15)
        username_entry.grid(row=1, column=1)

        password_entry = Entry(LoginFrame , font=('arial', 20), width=15, show="*")
        password_entry.grid(row=2, column=1)

        btn_login = Button(LoginFrame , text="Login", font=('arial', 18), width=30, command=login)
        btn_login.grid(row=4, columnspan=2, pady=20)

        btn = Button(LoginFrame , text="Registration", font=('arial', 18), width=30, command=RegistrationWindow)
        btn.grid(row=5, columnspan=2, pady=20)

        login_status_label = tk.Label(LoginFrame, text='')
        login_status_label.grid(row=6, columnspan=2, pady=20)
        # _______________________________________________________

        self.mainloop()