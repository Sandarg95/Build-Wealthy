# Build-Wealthy
Academic project
# Tkinter Multi-Window Application

This project is a simple multi-window application built using Python's Tkinter library. It provides a sequence of windows that navigate from a welcome screen to an authentication screen and finally to a menu screen with various options.

GitHub Link : https://github.com/Sandarg95/Build-Wealthy.git	
Username: dodo
Password: 1234


# Files

- `main.py`: Contains the main application code.

# Dependencies

- Python 3.x
- Tkinter (comes pre-installed with Python)

# Usage

1. Ensure you have Python 3 installed on your system.
2. Save the provided code into a file named `main.py`.
3. Run the application using the command:
   ```bash
   python main.py
   ```

# Code Explanation

# WindowOne

The first window that appears is the welcome screen.

```python
class WindowOne(tk.Tk):
    def __init__(self):
        super().__init__()
        
        custom_font = font.Font(family="Helvetica", size=70, weight='bold')
        slogan_font = font.Font(family="Comic Sans MS", size=20, weight='bold')
        self.title('WELCOME')
        self.geometry('640x480')
        self.configure(bg='black')
        self.lbl_msg = tk.Label(self, text="WELCOME", font=custom_font, anchor='center', foreground='gold', bg='black')
        self.lbl_msg.place(x=60, y=150)
        self.lbl_msg = tk.Label(self, text="BUILD WEALTHY", font=slogan_font, anchor='center', foreground='white', bg='black')
        self.lbl_msg.place(x=190, y=250)
        self.btn_new_game = tk.Button(self, text='Continue', command=lambda: self.process_btn('Continue'))
        self.btn_new_game.place(x=550, y=400)
        self.update()

    def process_btn(self, btn_pressed: str):
        if btn_pressed == 'Continue':
            self.destroy()
            window_two = WindowTwo()
            window_two.mainloop()
```

# WindowTwo

The second window is the authentication screen where users input their username and password.

```python
class WindowTwo(tk.Tk):
    def __init__(self):
        super().__init__()
        
        id_font = font.Font(family="Helvetica", size=10, weight='bold')
        self.title('Authentication')
        self.geometry('640x480')
        self.configure(bg='black')
        self.lbl_msg = tk.Label(self, text="Username", font=id_font, anchor='center', foreground='red', bg='black')
        self.lbl_msg.place(x=180, y=167)
        self.lbl_msg = tk.Label(self, text="Password", font=id_font, anchor='center', foreground='red', bg='black')
        self.lbl_msg.place(x=180, y=217)

        self.entry_value_username = tk.Entry(self)
        self.entry_value_username.place(x=250, y=170)
        self.entry_value_password = tk.Entry(self)
        self.entry_value_password.place(x=250, y=220)
        self.btn_new_game = tk.Button(self, text='Connect', command=lambda: self.process_btn('Connect'))
        self.btn_new_game.place(x=350, y=270)
        self.update()

    def process_btn(self, btn_pressed: str):
        username = self.entry_value_username.get()
        password = self.entry_value_password.get()
        error_font = font.Font(family="Helvetica", size=7, weight='bold', slant='italic')
        
        if btn_pressed == 'Connect':
            if username == 'dodo' and password == '1234':
                self.destroy()
                window_three = Windowthree()
                window_three.mainloop()
            else:
                self.entry_value_username.delete(0, tk.END)
                self.entry_value_password.delete(0, tk.END)
                self.lbl_msg = tk.Label(self, text="Username or Password incorrect", font=error_font, anchor='center', foreground='orange', bg='black')
                self.lbl_msg.place(x=235, y=245)
```

# Windowthree

The third window is the main menu that provides different options.

```python
class Windowthree(tk.Tk):
    def __init__(self):
        super().__init__()
       
        title_font = font.Font(family="Helvetica", size=100, weight='bold')
        self.title('Menu')
        button_width = 20

        self.geometry('640x480')
        self.configure(bg='blue')
        self.lbl_msg = tk.Label(self, text="MENU", font=title_font, anchor='center', foreground='white', bg='blue')
        self.lbl_msg.place(x=125, y=10)

        self.btn_new_game = tk.Button(self, text='Add Expenses', command=lambda: self.process_btn('add_expenses'), width=button_width)
        self.btn_new_game.place(x=260, y=180)
        self.btn_new_game = tk.Button(self, text='View Expenses', command=lambda: self.process_btn('view_expenses'), width=button_width)
        self.btn_new_game.place(x=260, y=230)
        self.btn_new_game = tk.Button(self, text='Reports', command=lambda: self.process_btn('report'), width=button_width)
        self.btn_new_game.place(x=260, y=280)
        self.btn_new_game = tk.Button(self, text='Settings', command=lambda: self.process_btn('settings'), width=button_width)
        self.btn_new_game.place(x=260, y=380)
        self.btn_new_game = tk.Button(self, text='This Month Summary', command=lambda: self.process_btn('summary'), width=button_width)
        self.btn_new_game.place(x=260, y=330)
        self.update()
```

# Main Function

The application starts by creating an instance of `WindowOne` and starting the main loop.

```python
if __name__ == "__main__":
    window_one = WindowOne()
    window_one.mainloop()
```
# Remaining Tasks
•	Implement the "View Expenses" screen.
•	Implement the "Reports" screen.
•	Implement the "Settings" screen.
•	Implement the backend calculations.
•	Implement the database solution (SQlite).
