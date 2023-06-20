import pymysql
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
from config import host, user, password, database

class RegisterWindow(tk.Tk):
    def __init__(self):
        super().__init__()


        self.style = ttk.Style(theme='darkly')
        self.title('RegisterWindow')
        self.geometry('550x400')

        self.resizable(False,False)

        def register():
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
                        username = username_entry_reg.get()
                        passwords = password_entry_reg.get()
                        
                        # Проверяем заполненность полей регистрации
                        if username and passwords:
                            # Проверяем, что пользователь не зарегистрирован ранее
                            sql = "SELECT * FROM Users WHERE Login=%s"
                            val = (username,)
                            cursor.execute(sql, val)
                            result = cursor.fetchone()
                            if result:
                                label_status.config(text="Пользователь уже зарегистрирован")
                            else:
                                # Регистрируем нового пользователя
                                sql = "INSERT INTO Users (Login, Password) VALUES (%s, %s)"
                                val = (username, passwords)
                                cursor.execute(sql, val)
                                mydb.commit()
                                label_status.config(text='Новый пользователь зарегистрирован')
                        else:
                            # Обрабатываем пустые поля регистрации
                            label_status.config(text='Поля регистрации должны быть заполнены')
                                                    
                except Exception as ex:
                    # Обрабатываем исключительные ситуации
                    print(f"Ошибка при регистрации: {ex}")
                finally:
                    mydb.close()
                    print('База данных закрыта')
            except Exception as ex:
                print(ex)

        # ____________________REGISTER___________________________
        RegisterFrame = Frame(self)
        RegisterFrame.pack(side=TOP, pady=40)

        lbl_username = Label(RegisterFrame , text="Username:", font=('arial', 25), bd=18)
        lbl_username.grid(row=1)

        lbl_password = Label(RegisterFrame , text="Password:", font=('arial', 25), bd=18)
        lbl_password.grid(row=2)

        username_entry_reg = Entry(RegisterFrame , font=('arial', 20), width=15)
        username_entry_reg.grid(row=1, column=1)

        password_entry_reg = Entry(RegisterFrame , font=('arial', 20), width=15, show="*")
        password_entry_reg.grid(row=2, column=1)

        btn_reg = Button(RegisterFrame , text="Register", font=('arial', 18), width=35, command=register)
        btn_reg.grid(row=4, columnspan=2, pady=20)

        label_status = tk.Label(RegisterFrame, text='')
        label_status.grid(row=5, columnspan=2, pady=20)
        # _______________________________________________________

        self.mainloop()
        