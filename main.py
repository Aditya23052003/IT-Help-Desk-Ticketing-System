import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('helpdesk.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY, user TEXT, issue TEXT, status TEXT)''')
conn.commit()

# Main application class
class HelpDeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Help Desk Ticketing System")
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username").grid(row=0)
        tk.Label(self.root, text="Password").grid(row=1)
        self.username = tk.Entry(self.root)
        self.password = tk.Entry(self.root, show='*')
        self.username.grid(row=0, column=1)
        self.password.grid(row=1, column=1)
        tk.Button(self.root, text='Login', command=self.login).grid(row=2, column=0, pady=4)
        tk.Button(self.root, text='Register', command=self.register_screen).grid(row=2, column=1, pady=4)

    def register_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="New Username").grid(row=0)
        tk.Label(self.root, text="New Password").grid(row=1)
        self.new_username = tk.Entry(self.root)
        self.new_password = tk.Entry(self.root, show='*')
        self.new_username.grid(row=0, column=1)
        self.new_password.grid(row=1, column=1)
        tk.Button(self.root, text='Register', command=self.register).grid(row=2, column=0, pady=4)
        tk.Button(self.root, text='Back', command=self.login_screen).grid(row=2, column=1, pady=4)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username.get()
        password = self.password.get()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            self.user_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        new_username = self.new_username.get()
        new_password = self.new_password.get()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully")
        self.login_screen()

    def user_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to the IT Help Desk System").grid(row=0, columnspan=2)
        tk.Button(self.root, text='Create Ticket', command=self.create_ticket_screen).grid(row=1, column=0, pady=4)
        tk.Button(self.root, text='View Tickets', command=self.view_tickets_screen).grid(row=1, column=1, pady=4)

    def create_ticket_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Describe your issue").grid(row=0)
        self.issue_description = tk.Entry(self.root)
        self.issue_description.grid(row=0, column=1)
        tk.Button(self.root, text='Submit', command=self.submit_ticket).grid(row=1, columnspan=2, pady=4)

    def submit_ticket(self):
        issue = self.issue_description.get()
        c.execute("INSERT INTO tickets (user, issue, status) VALUES (?, ?, ?)", (self.username.get(), issue, 'Open'))
        conn.commit()
        messagebox.showinfo("Success", "Ticket created successfully")
        self.user_screen()

    def view_tickets_screen(self):
        self.clear_screen()
        c.execute("SELECT * FROM tickets WHERE user=?", (self.username.get(),))
        tickets = c.fetchall()
        for idx, ticket in enumerate(tickets):
            tk.Label(self.root, text=f"Ticket ID: {ticket[0]}, Issue: {ticket[2]}, Status: {ticket[3]}").grid(row=idx)
        tk.Button(self.root, text='Back', command=self.user_screen).grid(row=len(tickets)+1, columnspan=2, pady=4)

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = HelpDeskApp(root)
    root.mainloop(
