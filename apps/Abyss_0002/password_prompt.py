import tkinter as tk
from tkinter import messagebox

PASSWORD = "letmein"

def show_password_prompt():
    def check_password():
        entered = pw_entry.get()
        if entered == PASSWORD:
            root.destroy()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")
            root.destroy()
            exit()

    def toggle_password():
        if pw_entry.cget('show') == '':
            pw_entry.config(show='*')
        else:
            pw_entry.config(show='')

    root = tk.Tk()
    root.title("Enter Password")
    root.geometry("300x140")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')

    tk.Label(root, text="Password Required", font=("Segoe UI", 12)).pack(pady=10)

    pw_entry = tk.Entry(root, width=30, show='*', font=("Segoe UI", 10))
    pw_entry.pack()

    show_var = tk.BooleanVar()
    show_check = tk.Checkbutton(root, text="Show password", variable=show_var, command=toggle_password)
    show_check.pack(pady=5)

    submit_btn = tk.Button(root, text="Submit", width=12, command=check_password)
    submit_btn.pack(pady=5)

    pw_entry.focus_set()
    root.bind('<Return>', lambda event: check_password())
    root.mainloop()
