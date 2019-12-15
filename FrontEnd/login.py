from tkinter import *
from tkinter import filedialog
from test_network import predict
from train_network import retrain_nn
import os, db, decorators, validators


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


@decorators.fe_decorator
def upload_image():
    file_path = filedialog.askopenfilename()
    global info_label
    try:
        info_label.destroy()
    except:
        pass
    try:
        # Manually emulated MOP
        if not validators.valid_image(file_path):
            raise Exception("File is not image")
        result = predict(file_path)
        info_label = Label(upload_screen, text=result, fg="green", font=("calibri", 11))
        info_label.pack()
        return 1
    except Exception as e:
        info_label = Label(upload_screen, text=str(e), fg="red", font=("calibri", 11))
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


@decorators.fe_decorator
def register_user():
    username_info = username.get()
    password_info = password.get()

    db.add_user(username_info, password_info)

    global info_label
    try:
        info_label.destroy()
    except:
        pass
    info_label = Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11))
    info_label.pack()
    return 1


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()

    login_check = db.login_check(username1, password1)
    if login_check == 1:
        login_sucess()
        user_type = db.user_type_check(username1)
        if user_type == 0:
            upload()
        elif user_type == 1:
            retrain()
    elif login_check == -1:
        password_not_recognised()
    else:
        user_not_found()


@decorators.fe_decorator
def login_sucess():
    global login_screen
    global info_label
    try:
        info_label.destroy()
    except:
        pass
    info_label = Label(login_screen, text="Login Success", fg="green", font=("calibri", 11))
    info_label.pack()
    return 1


@decorators.fe_decorator
def password_not_recognised():
    global login_screen
    global info_label
    try:
        info_label.destroy()
    except:
        pass
    info_label = Label(login_screen, text="Invalid Password", fg="red", font=("calibri", 11))
    info_label.pack()
    return 1


@decorators.fe_decorator
def user_not_found():
    global login_screen
    global info_label
    try:
        info_label.destroy()
    except:
        pass
    info_label = Label(login_screen, text="User Not Found", fg="red", font=("calibri", 11))
    info_label.pack()
    return 1


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


# db.delete()
main_account_screen()
