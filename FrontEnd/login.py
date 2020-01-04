from tkinter import *
from tkinter import filedialog
import test_network as tn
from train_network import retrain_nn, train_nn, data_prep, model_init
from dl import csv_dl, xml_dl, json_dl
import os, db, decorators, validators


def retrain():
    global retrain_screen, batches, epochs
    retrain_screen = Toplevel(main_screen)
    retrain_screen.title("Crack detection")
    retrain_screen.geometry("300x200")
    Label(retrain_screen, text="").pack()
    Label(retrain_screen, text="Number batches:").pack()
    batches = Entry(retrain_screen)
    batches.pack()
    Label(retrain_screen, text="Number epochs:").pack()
    epochs = Entry(retrain_screen)
    epochs.pack()
    Label(retrain_screen, text="").pack()
    Button(retrain_screen, text="Retrain the network", height="2", width="30", command=retrain_do).pack()


def retrain_do():
    global info_label
    try:
        info_label.destroy()
    except:
        pass
    try:
        if int(batches.get()) < 1 or int(epochs.get()) < 1:
            raise Exception()
        try:
            info_label.destroy()
        except:
            pass
        retrain_nn(int(batches.get()), int(epochs.get()))
    except:
        info_label = Label(retrain_screen, text="Batches and epochs must be integers > 0", fg="red", font=("calibri", 11))
        info_label.pack()
        return 1


def upload():
    global upload_screen, upload_frame, canvas, info_labels
    info_labels = list()
    upload_screen = Toplevel(main_screen)
    upload_screen.title("Crack detection")
    upload_screen.geometry("300x200")

    canvas = Canvas(upload_screen)
    vscrollbar = Scrollbar(upload_screen)
    vscrollbar.config(command=canvas.yview)
    vscrollbar.pack(side=LEFT, fill=Y)

    upload_frame = Frame(canvas)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window(0, 0, window=upload_frame, anchor='nw')

    Label(upload_frame, text="").pack()
    Button(upload_frame, text="Upload an image", height="2", width="30", command=upload_image).pack()
    Button(upload_frame, text="Upload a folder", height="2", width="30", command=upload_folder).pack()


@decorators.fe_decorator
def upload_image():
    tn.images = list()
    tn.predictions = list()
    file_path = filedialog.askopenfilename()
    global info_labels
    try:
        for label in info_labels:
            label.destroy()
    except:
        pass
    try:
        # Manually emulated MOP
        if not validators.valid_image(file_path):
            raise Exception("File is not image")
        result = tn.predict(file_path)
        label = Label(upload_frame, text=result, fg="green", font=("calibri", 11))
        label.pack()
        info_labels.append(label)

        create_downloaders()

        upload_screen.update()
        canvas.config(scrollregion=canvas.bbox("all"))
        return 1
    except Exception as e:
        label = Label(upload_frame, text=str(e), fg="red", font=("calibri", 11))
        label.pack()
        info_labels.append(label)
        upload_screen.update()
        canvas.config(scrollregion=canvas.bbox("all"))


@decorators.fe_decorator
def upload_folder():
    tn.images = list()
    tn.predictions = list()
    folder_path = filedialog.askdirectory()
    global info_labels
    try:
        for label in info_labels:
            label.destroy()
    except:
        pass
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            # Manually emulated MOP
            if not validators.valid_image(file_path):
                raise Exception("File is not image")
            result = tn.predict(file_path)
            label = Label(upload_frame, text=result, fg="green", font=("calibri", 11))
            label.pack()
            info_labels.append(label)

        create_downloaders()

        upload_screen.update()
        canvas.config(scrollregion=canvas.bbox("all"))
        return 1
    except Exception as e:
        label = Label(upload_frame, text=str(e), fg="red", font=("calibri", 11))
        label.pack()
        info_labels.append(label)
        upload_screen.update()
        canvas.config(scrollregion=canvas.bbox("all"))


def create_downloaders():
    dl1 = Button(upload_frame, text="Download csv", height="2", width="30", command=csv_form)
    dl1.pack()
    info_labels.append(dl1)
    dl2 = Button(upload_frame, text="Download xml", height="2", width="30", command=xml_form)
    dl2.pack()
    info_labels.append(dl2)
    dl3 = Button(upload_frame, text="Download json", height="2", width="30", command=json_form)
    dl3.pack()
    info_labels.append(dl3)


def get_test_data():
    data = tn.get_nn_data()
    path = filedialog.askdirectory()
    return data, path


def csv_form():
    data, path = get_test_data()
    csv_dl(data, path)


def xml_form():
    data, path = get_test_data()
    xml_dl(data, path)


def json_form():
    data, path = get_test_data()
    json_dl(data, path)


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
    elif login_check == 0:
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
