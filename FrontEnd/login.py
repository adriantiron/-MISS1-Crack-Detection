from tkinter import *
from tkinter import filedialog
from test_network import predict
from train_network import retrain_nn
import os


def retrain():
    global retrain_screen
    retrain_screen = Toplevel(main_screen)
    retrain_screen.title("Crack detection")
    retrain_screen.geometry("300x200")
    Label(retrain_screen, text="").pack()
    Button(retrain_screen, text="Retrain the network", height="2", width="30", command=retrain_nn).pack()


def upload():
    global upload_screen
    upload_screen = Toplevel(main_screen)
    upload_screen.title("Crack detection")
    upload_screen.geometry("300x200")
    Label(upload_screen, text="").pack()
    Button(upload_screen, text="Upload an image", height="2", width="30", command=upload_image).pack()


def upload_image():
    file_path = filedialog.askopenfilename()
    global info_label
    try:
        info_label.destroy()
    except:
        pass

    try:
        result = predict(file_path)
        info_label = Label(upload_screen, text=result, fg="green", font=("calibri", 11))
    except:
        info_label = Label(upload_screen, text="File is not image", fg="red", font=("calibri", 11))
    finally:
        info_label.pack()


def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x200")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, command=register_user).pack()


def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x200")
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="Password").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()


def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    global info_label
    try:
        info_label.destroy()
    except:
        pass
    info_label = Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11))
    info_label.pack()


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
            upload()
            retrain()
        else:
            password_not_recognised()
    else:
        user_not_found()


def login_sucess():
    global login_screen
    global info_label
    try:
        info_label.destroy()
    except:
        pass
    info_label = Label(login_screen, text="Login Success", fg="green", font=("calibri", 11))
    info_label.pack()


def password_not_recognised():
    global login_screen
    global info_label
    try:
        info_label.destroy()
    except:
        pass
    info_label = Label(login_screen, text="Invalid Password", fg="red", font=("calibri", 11))
    info_label.pack()


def user_not_found():
    global login_screen
    global info_label
    try:
        info_label.destroy()
    except:
        pass
    info_label = Label(login_screen, text="User Not Found", fg="red", font=("calibri", 11))
    info_label.pack()


def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x200")
    main_screen.title("Crack detection")
    Label(text="").pack()
    Button(text="Login with existing account", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register a new account", height="2", width="30", command=register).pack()

    main_screen.mainloop()


main_account_screen()
