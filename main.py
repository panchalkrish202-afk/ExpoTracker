import tkinter as tk
from tkinter import messagebox
import json
import os

USERS_FILE = "users.json"

# ---------- LOAD USERS ----------
def load_users():
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

users = load_users()
current_user = None

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------- LOGIN ----------
def login():
    global current_user
    u = user_entry.get().strip()
    p = pass_entry.get().strip()

    if not u or not p:
        messagebox.showerror("Error", "Enter username & password")
        return

    if u in users and users[u]["password"] == p:
        current_user = u
        show_app()
    else:
        messagebox.showerror("Error", "Invalid credentials")

def register():
    u = user_entry.get().strip()
    p = pass_entry.get().strip()

    if not u or not p:
        messagebox.showerror("Error", "Fields empty")
        return

    if u in users:
        messagebox.showerror("Error", "User exists")
        return

    users[u] = {"password": p, "data": []}
    save_users()
    messagebox.showinfo("Success", "Registered")

# ---------- DASHBOARD ----------
def update_dashboard():
    income = 0
    expense = 0

    for t in users[current_user]["data"]:
        if t["type"] == "Income":
            income += t["amount"]
        else:
            expense += t["amount"]

    balance = income - expense

    balance_label.config(text=f"₹ {balance}")
    income_label.config(text=f"₹ {income}")
    expense_label.config(text=f"₹ {expense}")

# ---------- ADD ----------
def add_transaction():
    amount = amount_entry.get().strip()
    desc = desc_entry.get().strip()
    t_type = type_var.get()

    if not amount or not desc:
        messagebox.showerror("Error", "Fill all fields")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Invalid amount")
        return

    users[current_user]["data"].append({
        "amount": amount,
        "desc": desc,
        "type": t_type
    })

    save_users()
    update_list()

    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

# ---------- LIST ----------
def update_list():
    listbox.delete(0, tk.END)

    for t in users[current_user]["data"]:
        text = f"{t['type']}  |  ₹{t['amount']}  |  {t['desc']}"
        listbox.insert(tk.END, text)

    update_dashboard()

# ---------- SWITCH ----------
def show_app():
    login_frame.pack_forget()
    app_frame.pack(fill="both", expand=True)
    update_list()

# ---------- UI ----------
root = tk.Tk()
root.title("ExpoTracker")
root.state("zoomed")

# COLORS
bg = "#0f172a"
card = "#1e293b"
accent = "#38bdf8"
text = "white"

root.configure(bg=bg)

# ---------- LOGIN ----------
login_frame = tk.Frame(root, bg=bg)
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="💸 Expense Tracker",
         font=("Arial", 36, "bold"),
         bg=bg, fg=text).pack(pady=60)

user_entry = tk.Entry(login_frame, font=("Arial", 16))
user_entry.pack(pady=10, ipadx=20, ipady=10)

pass_entry = tk.Entry(login_frame, show="*", font=("Arial", 16))
pass_entry.pack(pady=10, ipadx=20, ipady=10)

tk.Button(login_frame, text="Login", command=login,
          bg=accent, fg="black", font=("Arial", 14), width=20).pack(pady=10)

tk.Button(login_frame, text="Register", command=register,
          bg="#334155", fg="white", font=("Arial", 14), width=20).pack()

# ---------- APP ----------
app_frame = tk.Frame(root, bg=bg)

# ---------- DASHBOARD UI ----------
dashboard = tk.Frame(app_frame, bg=bg)
dashboard.pack(pady=20)

def create_card(title):
    frame = tk.Frame(dashboard, bg=card, padx=40, pady=20)
    frame.pack(side="left", padx=20)

    tk.Label(frame, text=title, font=("Arial", 16),
             bg=card, fg="white").pack()

    value = tk.Label(frame, text="₹ 0",
                     font=("Arial", 22, "bold"),
                     bg=card, fg=accent)
    value.pack()

    return value

balance_label = create_card("Balance")
income_label = create_card("Income")
expense_label = create_card("Expense")

# ---------- FORM ----------
card_frame = tk.Frame(app_frame, bg=card)
card_frame.pack(pady=20, ipadx=50, ipady=30)

tk.Label(card_frame, text="Add Transaction",
         font=("Arial", 22, "bold"),
         bg=card, fg=text).pack(pady=15)

amount_entry = tk.Entry(card_frame, font=("Arial", 16))
amount_entry.pack(pady=10, ipadx=30, ipady=10)

desc_entry = tk.Entry(card_frame, font=("Arial", 16))
desc_entry.pack(pady=10, ipadx=30, ipady=10)
desc_entry.insert(0, "What did you spend on?")

type_var = tk.StringVar(value="Expense")

type_frame = tk.Frame(card_frame, bg=card)
type_frame.pack(pady=10)

tk.Radiobutton(type_frame, text="Expense", variable=type_var,
               value="Expense", bg=card, fg=text,
               selectcolor=card, font=("Arial", 14)).pack(side="left", padx=20)

tk.Radiobutton(type_frame, text="Income", variable=type_var,
               value="Income", bg=card, fg=text,
               selectcolor=card, font=("Arial", 14)).pack(side="left", padx=20)

tk.Button(card_frame, text="Add",
          command=add_transaction,
          bg=accent, fg="black",
          font=("Arial", 16), width=20).pack(pady=15)

# ---------- HISTORY ----------
tk.Label(app_frame, text="Transaction History",
         font=("Arial", 22, "bold"),
         bg=bg, fg=text).pack(pady=10)

frame_list = tk.Frame(app_frame)
frame_list.pack()

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(frame_list,
                     width=120,
                     height=20,
                     bg=card,
                     fg=text,
                     font=("Consolas", 14),
                     bd=0,
                     yscrollcommand=scrollbar.set)

listbox.pack()
scrollbar.config(command=listbox.yview)

root.mainloop()