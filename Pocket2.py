import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from cryptography.fernet import Fernet
import json
import platform
import os

'''
        Coded By AuxGrep
'''

Validated_OS = []

# Check OS 
def os_check(supported=['Linux', 'Windows', 'Win32']):
    current_os = platform.system()
    if current_os in supported:
        Validated_OS.append(str(current_os))
        if current_os == 'Linux':
            if "SUDO_UID" not in os.environ.keys():
                messagebox.showerror('Runtime Error', 'Please run as root')
                exit()
        return current_os
    else:
        messagebox.showwarning("OS Error", "Unsupported OS Detected!! Program supports: Linux and Windows.")
        exit()
os_check()

# Function to generate encrypted key with Fernet
def generate_key():
    return Fernet.generate_key()

# Function to encrypt password with respective key
def encrypt_password(key, password):
    return Fernet(key).encrypt(password.encode()).decode()

# Function to decrypt password using encryption key
def decrypt_password(key, encrypted_password):
    return Fernet(key).decrypt(encrypted_password.encode()).decode()

# Function to save the user entry password to a json file 
def save_passwords(passwords):
    filepath = ""
    for x in Validated_OS:
        if x == "Windows":
            filepath = "C:\\Users\\Public\\encry_pass.txt"
        elif x == 'Linux':
            filepath = "/opt/encry_pass.txt"
    
    with open(filepath, "w") as file:
        json.dump(passwords, file)

# Function to load saved passwords from the json file
def load_passwords():
    filepath = ""
    for x in Validated_OS:
        if x == "Windows":
            filepath = "C:\\Users\\Public\\encry_pass.txt"
        elif x == 'Linux':
            filepath = "/opt/encry_pass.txt"
    
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to add encrypted password to pocket
def add_password():
    service = service_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if all((service, username, password)):
        encrypted_password = encrypt_password(key, password)
        passwords[service] = {'username': username, 'password': encrypted_password}
        save_passwords(passwords)
        messagebox.showinfo("Success", "Password added successfully!")
        service_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Please fill in all the fields.")

# Function to retrieve password 
def get_password():
    service = service_entry.get()
    if service in passwords:
        encrypted_password = passwords[service]['password']
        decrypted_password = decrypt_password(key, encrypted_password)
        messagebox.showinfo("Password", f"Username: {passwords[service]['username']}\nPassword: {decrypted_password}")
    else:
        messagebox.showwarning("Error", "Password not found. Press 'View All Saved Passwords'.")

# Function to view/edit all encrypted saved password
def view_all_data():
    def edit_data():
        selected_item = tree.selection()
        if selected_item:
            selected_service = tree.item(selected_item)['values'][0]
            new_username = simpledialog.askstring("Edit Username", f"Enter new username for {selected_service}:")
            if new_username is not None:
                passwords[selected_service]['username'] = new_username
                save_passwords(passwords)
                messagebox.showinfo("Success", "Username updated successfully!")
                tree.delete(*tree.get_children())
                for service, info in passwords.items():
                    decrypted_password = decrypt_password(key, info['password'])
                    tree.insert("", "end", values=(service, info['username'], decrypted_password))
        else:
            messagebox.showwarning("Error", "Please select a data to edit.")

    # Function to delete saved Data/Passwords
    def delete_data():
        selected_item = tree.selection()
        if selected_item:
            selected_service = tree.item(selected_item)['values'][0]
            confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {selected_service}?")
            if confirmation:
                del passwords[selected_service]
                save_passwords(passwords)
                messagebox.showinfo("Success", "Data deleted successfully!")
                tree.delete(selected_item)
        else:
            messagebox.showwarning("Error", "Please select a data to delete.")

    # Configuration of View password window
    data_window = tk.Toplevel(main_window)
    data_window.title("Saved Password Pocket")
    
    # Configuration of View password window - Columns set
    tree = ttk.Treeview(data_window, columns=("Service", "Username", "Password"), show="headings")
    tree.heading("Service", text="Service")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    
    # Decrypting and displaying passwords
    for service, info in passwords.items():
        decrypted_password = decrypt_password(key, info['password'])
        tree.insert("", "end", values=(service, info['username'], decrypted_password))
    
    tree.pack(expand=True, fill="both")
    
    edit_button = tk.Button(data_window, text="Edit Saved Password", command=edit_data)
    edit_button.pack(pady=5)
    
    delete_button = tk.Button(data_window, text="Delete Saved Password", command=delete_data)
    delete_button.pack(pady=5)

# Function for authentication
def authenticate():
    if username_entry_login.get() == "admin" and password_entry_login.get() == "password":
        login_window.destroy()
        main_window.deiconify()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

for x in Validated_OS:
    if x == "Windows":
        try:
            if os.path.exists('C:\\Users\\Public\\.Enc') == True:
                with open("C:\\Users\\Public\\.Enc\\Enc.txt", "rb") as file:
                    key = file.read()
            else:
                os.mkdir('C:\\Users\\Public\\.Enc')
                with open("C:\\Users\\Public\\.Enc\\Enc.txt", "rb") as file:
                    key = file.read()
                    
        except FileNotFoundError:
            key = generate_key()
            with open("C:\\Users\\Public\\.Enc\\Enc.txt", "wb") as file:
                file.write(key)
    elif x == 'Linux':
        try:
            with open("/opt/Enc.txt", "rb") as file:
                key = file.read()
        except FileNotFoundError:
            key = generate_key()
            with open("/opt/Enc.txt", "wb") as file:
                file.write(key)

passwords = load_passwords()

# Tkinter Configuration
login_window = tk.Tk()
login_window.title("Please Login")

login_frame = tk.Frame(login_window)
login_frame.pack(padx=20, pady=20)

tk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5)
username_entry_login = tk.Entry(login_frame)
username_entry_login.grid(row=0, column=1, padx=10, pady=5)

tk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5)
password_entry_login = tk.Entry(login_frame, show="*")
password_entry_login.grid(row=1, column=1, padx=10, pady=5)

tk.Button(login_frame, text="Login", command=authenticate).grid(row=2, column=1, padx=10, pady=5)

main_window = tk.Tk()
main_window.title("Encrypted Password Pocket v.1.0")

main_frame = tk.Frame(main_window)
main_frame.pack(padx=20, pady=20)

# Message of the Day 
instructions = '''Author: AuxGrep'''
tk.Label(main_frame, text=instructions).grid(row=0, columnspan=2, padx=10, pady=15)

tk.Label(main_frame, text="Website:").grid(row=1, column=0, padx=10, pady=5)
service_entry = tk.Entry(main_frame)
service_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Username:").grid(row=2, column=0, padx=10, pady=5)
username_entry = tk.Entry(main_frame)
username_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Password:").grid(row=3, column=0, padx=10, pady=5)
password_entry = tk.Entry(main_frame, show="*")
password_entry.grid(row=3, column=1, padx=10, pady=5)

# Button Configurations
tk.Button(main_frame, text="Save Password", command=add_password).grid(row=4, column=0, padx=10, pady=29)
tk.Button(main_frame, text="Get Password", command=get_password).grid(row=4, column=1, padx=10, pady=5)
tk.Button(main_frame, text="View All Saved Password", command=view_all_data).grid(row=5, columnspan=2, padx=10, pady=5)

# Starting the Program
main_window.withdraw()
login_window.mainloop()
