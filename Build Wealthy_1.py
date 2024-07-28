import tkinter as tk
from tkinter import ttk
from tkinter import font
from datetime import datetime, timedelta
from tkinter import messagebox
import datetime
import sqlite3
import csv
from PIL import Image, ImageTk
import re
import sqlite3
from dateutil.relativedelta import relativedelta

# Connexion to the database
conn = sqlite3.connect('Expenses.db')

# Cursor creation
cur = conn.cursor()

# Create table expense if not exists. It keeps data of all expenses. 
cur.execute('''CREATE TABLE IF NOT EXISTS expense
               (id INTEGER PRIMARY KEY, title TEXT, date DATE, nature TEXT, amount INTEGER, isauto BOOLEAN, frequency TEXT)''')


 # Create table user_password if not exists. It keeps password. 
cur.execute('''
    CREATE TABLE IF NOT EXISTS user_password (
        id INTEGER PRIMARY KEY,
        password TEXT NOT NULL
    )
''')


# Main window that displays the welcome message
class WindowOne(tk.Tk):
    def __init__(self):
        super().__init__()
        
        custom_font = font.Font(family="Helvetica", size=70, weight='bold') # for the title
        slogan_font = font.Font(family="Comic Sans MS", size=20, weight='bold') # to display the number
        
        self.title('WELCOME')
        self.geometry('640x480')
        self.configure(bg='black')
        
        self.lbl_msg = tk.Label(self, text="WELCOME ", font=custom_font, anchor='center', foreground='gold', bg='black')
        self.lbl_msg.place(x=60, y=150)
        
        self.lbl_msg = tk.Label(self, text="BUILD WEALTHY", font=slogan_font, anchor='center', foreground='white', bg='black')
        self.lbl_msg.place(x=190, y=250)
        
        self.btn_new_game = tk.Button(self, text='Continue', command=lambda: self.process_btn('Continue'))
        self.btn_new_game.place(x=550, y=400)
        self.update()
        
    #fuction to go back
    def process_btn(self, btn_pressed: str): 
        if btn_pressed == 'Continue':
            self.destroy()
            window_two = WindowTwo()
            window_two.mainloop()
            

# Authentication window
class WindowTwo(tk.Tk):
    def __init__(self):
        super().__init__()
        
        id_font = font.Font(family="Helvetica", size=10, weight='bold') # Font for the "Password" label
        slogan_font = font.Font(family="Comic Sans MS", size=20, weight='bold') # Font for any additional text
        
        self.title('Authentication')
        self.geometry('640x480')
        self.configure(bg='black')
    
        # Check if it finds the right image
        try:
            self.image = Image.open('password10.png')  # Try to open the password image
            new_size = (250, 250)  # Define the new size 
            self.image = self.image.resize(new_size, Image.LANCZOS)  # Resize the image
            self.image_tk = ImageTk.PhotoImage(self.image) # Convert the image to a Tkinter-compatible image
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_tk = None
        
        if self.image_tk:
            self.image_label = tk.Label(self, image=self.image_tk)
            self.image_label.place(x=200, y=5)
        else:
            self.image_label = tk.Label(self, text="Image could not be loaded.")
            self.image_label.place(x=200, y=5)
        
        self.lbl_msg = tk.Label(self, text="Password", font=id_font, anchor='center', foreground='red', bg='black')
        self.lbl_msg.place(x=230, y=280)
        
        self.entry_value_password = tk.Entry(self, show='*')
        self.entry_value_password.place(x=300, y=280) 
        
        self.btn_connect = tk.Button(self, text='Connect', command=lambda: self.process_btn('Connect'))
        self.btn_connect.place(x=350, y=330)
        self.update()
        
    def process_btn(self, btn_pressed: str):
        password = self.entry_value_password.get()
        error_font = font.Font(family="Helvetica", size=7, weight='bold', slant='italic') # Font for the error message
        cur.execute("SELECT password FROM user_password WHERE id = 1")
        stored_password = cur.fetchone()
        
        if btn_pressed == 'Connect':
            if password == stored_password[0]:
                self.destroy()
                window_three = Windowthree()  # Open the Main Menu
                window_three.mainloop()
            else:
                self.entry_value_password.delete(0, tk.END)
                self.lbl_msg = tk.Label(self, text="Password incorrect. Try again.", font=error_font, anchor='center', foreground='orange', bg='black')
                self.lbl_msg.place(x=255, y=305)
                
                
                
class WindowReport(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Define fonts for different labels and titles
        title_font = font.Font(family="Helvetica", size=10, weight='bold') # for the title
        slogan_font = font.Font(family="Comic Sans MS", size=30, weight='bold') # to display the number
        result_font = font.Font(family="Helvetica", size=7) # for results
        
        self.title('Reports')
        button_width = 20
        
        self.geometry('640x480')
        self.configure(bg='light green')
        
        # Create the main label for the window
        self.lbl_msg = tk.Label(self, text="Reports", font=slogan_font, anchor='center', foreground='black', bg='light green')
        self.lbl_msg.place(x=245, y=5)
        
        # Create a back button
        self.back_button = tk.Button(self, text='BACK', command=self.back, width=15)
        self.back_button.place(x=30, y=430)

        # Create generate button
        self.generate_button = tk.Button(self, text='Generate Report', command=self.generate, width=15, bg='green')
        self.generate_button.place(x=30, y=330)

        # Create download button (initially disabled)
        self.download_button = tk.Button(self, text='Download Report', command=self.download, width=15, bg='pink', state='disabled')
        self.download_button.place(x=30, y=360)

        # Create entry fields for date and nature of expense
        self.entry_value_dateExpenseFrom = tk.Entry(self)
        self.entry_value_dateExpenseFrom.place(x=30, y=130)

        self.entry_value_dateExpenseTo = tk.Entry(self)
        self.entry_value_dateExpenseTo.place(x=30, y=210)

        self.entry_value_natureExpense = tk.Entry(self)
        self.entry_value_natureExpense.place(x=30, y=290)

        # Create labels to display total sum and count of expenses
        self.label_totalSum = tk.Label(self, text='', bg='light green', font=result_font, foreground='black', justify='right')
        self.label_totalSum.place(x=531, y=433)
        
        self.label_count = tk.Label(self, text='', bg='light green', font=result_font, foreground='black', justify='right')
        self.label_count.place(x=170, y=433)

        # Add labels for entry prompts
        self.label_dateExpenseFrom = tk.Label(self, text="From", bg='light green', font=title_font, foreground='white', justify='right')
        self.label_dateExpenseFrom.place(x=30, y=100)

        self.label_dateExpenseTo = tk.Label(self, text="To", bg='light green', font=title_font, foreground='white', justify='right')
        self.label_dateExpenseTo.place(x=30, y=180)

        self.label_natureExpense = tk.Label(self, text="Nature", bg='light green', font=title_font, foreground='white', justify='right')
        self.label_natureExpense.place(x=30, y=260)

        # Create a treeview for showing expenses
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Date", "Nature", "Amount"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Nature", text="Nature")
        self.tree.heading("Amount", text="Amount")
        
        # Set the width of the columns
        self.tree.column("ID", width=20)
        self.tree.column("Title", width=100)
        self.tree.column("Date", width=50)
        self.tree.column("Nature", width=100)
        self.tree.column("Amount", width=80)
        
        self.tree.place(x=170, y=100, width=450, height=330)
            
    # Method to generate the report based on input
    def generate(self):
        
        self.label_totalSum.config(text='') # Clear the total sum label
        self.label_count.config(text='') # Clear the count label
        for item in self.tree.get_children(): # Clear the treeview
            self.tree.delete(item)

        # Get the values from the date entry fields
        date_text_From = self.entry_value_dateExpenseFrom.get()
        date_text_To = self.entry_value_dateExpenseTo.get()
        
        # Function to validate the date format
        def is_valid_date(date_text):
            try:
                if date_text != '':
                    datetime.datetime.strptime(date_text, '%Y-%m-%d')
                return True
            except ValueError:
                return False
        
        # Check the validity of each date field
        if not is_valid_date(date_text_From) or not is_valid_date(date_text_To):
            # Display an error message if the format is incorrect
            messagebox.showerror("Error", "Wrong date format. Please enter dates in the format YYYY-MM-DD.")
            
        if date_text_From == '':
            date_text_From = '1950-01-01' # Default start date

        if date_text_To == '':
            date_text_To = '2050-12-31' # Default end date
        
        nature = self.entry_value_natureExpense.get()
        self.load_data(date_text_From, date_text_To, nature)

        # Enable or disable the download button based on data presence
        if self.tree.get_children():
            self.download_button.config(state='normal') # Enable if data exists
        else:
            self.download_button.config(state='disabled') # Disable if no data exists

    # Method to load data from the database
    def load_data(self, dateFrom, dateTo, nat):
        
        # Connect to the SQLite database
        conn = sqlite3.connect('Expenses.db')
        cur = conn.cursor()

        # Define SQL queries
        query1 = """
        SELECT * FROM expense 
        WHERE date BETWEEN ? AND ? 
        ORDER BY date  
        """

        query1a = """
        SELECT SUM(amount) FROM expense 
        WHERE date BETWEEN ? AND ? 
        ORDER BY date   
        """

        query2a = """
        SELECT SUM(amount) FROM expense 
        WHERE date BETWEEN ? AND ?
        AND nature= ?    
        ORDER BY date
        """
        
        query1b = """
        SELECT COUNT(amount) FROM expense 
        WHERE date BETWEEN ? AND ?  
        ORDER BY date  
        """

        query2b = """
        SELECT COUNT(amount) FROM expense 
        WHERE date BETWEEN ? AND ?
        AND nature= ?
        ORDER BY date    
        """
    
        query2 = """
        SELECT * FROM expense 
        WHERE date BETWEEN ? AND ?
        AND nature = ?
        ORDER BY date
        """
    
        # Execute the appropriate query based on the nature of the expense
        if nat == '':
            cur.execute(query1, (dateFrom, dateTo))
        else:
            cur.execute(query2, (dateFrom, dateTo, nat))
        
        rows = cur.fetchall()   
    
        # Insert the data into the treeview
        for row in rows:
            self.tree.insert("", tk.END, iid=row[0], values=(row[0], row[1], row[2], row[3], row[4]))
        
        # Calculate the total sum of the expenses
        if nat == '':
            cur.execute(query1a, (dateFrom, dateTo))
            total_sum = cur.fetchone()[0]
            total_sum = float(total_sum) if total_sum is not None else 0
        else:
            cur.execute(query2a, (dateFrom, dateTo, nat))
            total_sum = cur.fetchone()[0]
            total_sum = float(total_sum) if total_sum is not None else 0

        # Calculate the count of the expenses
        if nat == '':
            cur.execute(query1b, (dateFrom, dateTo))
            count = cur.fetchone()[0]
            count = int(count) if count is not None else 0
        else:
            cur.execute(query2b, (dateFrom, dateTo, nat))
            count = cur.fetchone()[0]
            count = int(count) if count is not None else 0

        # Update the labels with the calculated values
        self.label_totalSum.config(text=f"Total Sum: {total_sum:.2f}")
        self.label_count.config(text=f"Number of Expenses: {count:.0f}")
        
        conn.close()
    
    # Method to download the report as a CSV file
    def download(self):
        now = datetime.datetime.now()
        # Convert to a string with a specific format
        now_text = now.strftime("%Y%m%d_%H%M%S")
        nameFile = "Report" + now_text
        filename = nameFile
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write headers
            writer.writerow(["ID", "Title", "Date", "Nature", "Amount"])
            
            # Write data
            for row in self.tree.get_children():
                writer.writerow(self.tree.item(row)["values"])  

        # Show information message
        messagebox.showinfo("Information", "File CSV " + filename + " is successfully downloaded.")

        # Reset the fields and treeview
        self.label_totalSum.config(text='')
        self.label_count.config(text='')
        self.entry_value_dateExpenseFrom.delete(0, tk.END)
        self.entry_value_dateExpenseTo.delete(0, tk.END)
        self.entry_value_natureExpense.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.download_button.config(state='disabled')

    # Method to go back to the previous window
    def back(self):
        self.destroy()
        back = Windowthree() # Call the Main Menu
        back.mainloop()
        

        
# Main menu window
class Windowthree(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Define fonts for different labels and titles
        title_font = font.Font(family="Helvetica", size=100, weight='bold') # for the title
        slogan_font = font.Font(family="Comic Sans MS", size=20, weight='bold') # for the slogan
        
        self.title('Menu')
        button_width = 20
        
        self.geometry('640x480')
        self.configure(bg='blue')
        
        # Create the main label for the window
        self.lbl_msg = tk.Label(self, text="MENU", font=title_font, anchor='center', foreground='white', bg='blue')
        self.lbl_msg.place(x=125, y=10)
        
        # Create buttons for different menu options
        self.btn_new_game = tk.Button(self, text='Add Expenses', command=lambda: self.process_btn('add_expenses'), width=button_width)
        self.btn_new_game.place(x=260, y=180)
        
        self.btn_new_game = tk.Button(self, text='View Expenses', command=lambda: self.process_btn('view_expenses'), width=button_width)
        self.btn_new_game.place(x=260, y=230)
        
        self.btn_new_game = tk.Button(self, text='Reports', command=lambda: self.process_btn('report'), width=button_width)
        self.btn_new_game.place(x=260, y=280)
        
        self.btn_new_game = tk.Button(self, text='Change Password', command=lambda: self.process_btn('password'), width=button_width)
        self.btn_new_game.place(x=260, y=380)
        
        self.btn_new_game = tk.Button(self, text='This Month Summary', command=lambda: self.process_btn('summary'), width=button_width)
        self.btn_new_game.place(x=260, y=330)
        
        self.update()

    # Method to process button clicks
    def process_btn(self, btn_pressed: str):
        if btn_pressed == 'add_expenses':
            self.destroy()
            window_addExp = WindowAddExp()
            window_addExp.mainloop()

        if btn_pressed == 'view_expenses':
            self.destroy()
            window_viewExp = WindowViewExp()
            window_viewExp.mainloop()

        if btn_pressed == 'report':
            self.destroy()
            window_report = WindowReport()
            window_report.mainloop()

        if btn_pressed == 'summary':
            self.destroy()
            window_summary = WindowSummary()
            window_summary.mainloop()
            
        if btn_pressed == 'password':
            self.destroy()
            window_password = WindowPassword()
            window_password.mainloop()




# Window to add expenses
class WindowAddExp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Define fonts for different labels and titles
        title_font = font.Font(family="Helvetica", size=10, weight='bold') # for the title
        slogan_font = font.Font(family="Comic Sans MS", size=40, weight='bold') # for the slogan
        
        self.title('Add Expenses')
        button_width = 20
        
        self.geometry('640x480')
        self.configure(bg='blue')
        
        # Create the main label for the window
        self.lbl_msg = tk.Label(self, text="ADD EXPENSES", font=slogan_font, anchor='center', foreground='yellow', bg='blue')
        self.lbl_msg.place(x=120, y=10)
        
        # Create entry fields for different expense attributes
        self.entry_value_nameExpense = tk.Entry(self)
        self.entry_value_nameExpense.place(x=250, y=120)
        
        self.entry_value_dateExpense = tk.Entry(self)
        self.entry_value_dateExpense.place(x=250, y=170)
        
        self.entry_value_natureExpense = tk.Entry(self)
        self.entry_value_natureExpense.place(x=250, y=220)
        
        self.entry_value_amountExpense = tk.Entry(self)
        self.entry_value_amountExpense.place(x=250, y=270)
        
        self.entry_value_until = tk.Entry(self)
        self.entry_value_until.place(x=360, y=370)
        
        # Add labels for prompts
        self.label_nameExpense = tk.Label(self, text="Title", bg='blue', font=title_font, foreground='white', justify='right')
        self.label_nameExpense.place(x=215, y=117)
        
        self.label_dateExpense = tk.Label(self, text="Date", bg='blue', font=title_font, foreground='white', justify='right')
        self.label_dateExpense.place(x=215, y=167)
        
        self.label_natureExpense = tk.Label(self, text="Nature", bg='blue', font=title_font, foreground='white', justify='right')
        self.label_natureExpense.place(x=200, y=217)
        
        self.label_amountExpense = tk.Label(self, text="Amount", bg='blue', font=title_font, foreground='white', justify='right')
        self.label_amountExpense.place(x=192, y=267)
        
        self.label_isAuto = tk.Label(self, text="Add Auto", bg='blue', font=title_font, foreground='white', justify='right')
        self.label_isAuto.place(x=183, y=320)
        
        self.label_frequency = tk.Label(self, text="Frequency", bg='blue', font=title_font, foreground='white', justify='right')
        self.label_frequency.place(x=165, y=370)
        
        self.label_until = tk.Label(self, text="Until", bg='blue', font=title_font, foreground='white', justify='right')
        self.label_until.place(x=320, y=370)
        
        self.toggle_state = False
        
        # Create a save button
        self.save_button = tk.Button(self, text='SAVE', command=self.save, width=15)
        self.save_button.place(x=500, y=430)
        
        # Create a back button
        self.back_button = tk.Button(self, text='BACK', command=self.back, width=15)
        self.back_button.place(x=30, y=430)
        
        # Create a toggle button for automatic expense entry
        self.toggle_button = tk.Button(self, text='NO', command=self.toggle)
        self.toggle_button.place(x=250, y=320)
        
        # Create a menu button for frequency options
        self.menu_button = tk.Menubutton(self, text='Options', relief=tk.RAISED)
        self.menu_button.grid()
        
        # Create a dropdown menu
        self.menu = tk.Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu
        self.menu_button.config(state='disabled')
        
        # Add options to the menu
        self.menu.add_command(label="Weekly", command=lambda: self.show_message('Weekly'))
        self.menu.add_command(label="Bi-weekly", command=lambda: self.show_message('Bi-weekly'))
        self.menu.add_command(label="Monthly", command=lambda: self.show_message('Monthly'))
        self.menu.add_command(label="Annually", command=lambda: self.show_message('Annually'))
        
        # Place the menu button
        self.menu_button.place(x=250, y=370)
        
        # Disable the 'until' entry by default
        self.entry_value_until.config(state='disabled')

    # Show the selected frequency message
    def show_message(self, message):
        self.menu_button.config(text=message)
    
    # Handle back button click
    def back(self):
        result = messagebox.askyesno("Confirmation", "Are you sure to cancel ?")
        if result:
            self.destroy()
            back = Windowthree()
            back.mainloop() 
    
    # Toggle the state for automatic expense entry
    def toggle(self):
        self.toggle_state = not self.toggle_state
        if self.toggle_state:
            self.toggle_button.config(text='YES', bg='green')
            self.menu_button.config(state='normal')
            self.entry_value_until.config(state='normal')
        else:
            self.toggle_button.config(text='NO', bg='red')
            self.menu_button.config(text='Options')
            self.menu_button.config(state='disabled')
            self.entry_value_until.delete(0, tk.END)
            self.entry_value_until.config(state='disabled')
        return self.toggle_state
    
    # Save the entered expense data
    def save(self):
        # Check name or nature
        name_text = self.entry_value_nameExpense.get()
        nature_text=self.entry_value_natureExpense.get()
        try:
            # Check if they are empty. 
            if not name_text or not nature_text:
                raise ValueError
            
        except ValueError:
            # Show an error message
            messagebox.showerror("Error", "Title and Nature must be filled")
            temoin=False
            return
        
        # Check date
        date_text = self.entry_value_dateExpense.get()
        try:
            # Try to get time
            valid_date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
            
        except ValueError:
            # Show an error message
            messagebox.showerror("Error", "Wrong date format. Please enter in format YYYY-MM-DD.")
            return
        
        # Check amount
        amount_text = self.entry_value_amountExpense.get()
        try:
            # Try to convert to float and check if positive
            if float(amount_text) > 0:
                valid_amount = amount_text
                temoin=True
            else:
                raise ValueError
        except ValueError:
            # Show an error message
            messagebox.showerror("Error", "Only positive number")
            temoin=False
            return
        
        # Check option
        try:
            # Check if Auto is on
            if self.toggle_state and self.menu_button.cget('text')=='Options':
                raise ValueError
            
        except ValueError:
            # Show an error message
            messagebox.showerror("Error", "Choose a frequency")
            temoin=False
            return
        
        # Check until limit date
        until_date_text = self.entry_value_until.get()
        try:
            # Check if Auto is on
            if self.toggle_state:
                until_valid_date = datetime.datetime.strptime(until_date_text, '%Y-%m-%d')
            
        except ValueError:
            # Show an error message
            messagebox.showerror("Error", "Wrong limit date.")
            temoin=False
            return
        
        # Insert data        
        frequency = self.menu_button.cget('text')
        current_date = valid_date
        
        if not self.toggle_state:
            cur.execute("INSERT INTO expense (title, date, nature, amount, isauto, frequency) VALUES (?, ?, ?, ?, ?, ?)",
                            (name_text, current_date.strftime('%Y-%m-%d'), nature_text, valid_amount, self.toggle_state, frequency))  
        
        if frequency == 'Weekly':
            delta = datetime.timedelta(days=7)
            while current_date <= until_valid_date:
                cur.execute("INSERT INTO expense (title, date, nature, amount, isauto, frequency) VALUES (?, ?, ?, ?, ?, ?)",
                            (name_text, current_date.strftime('%Y-%m-%d'), nature_text, valid_amount, self.toggle_state, frequency))
                current_date += delta

        elif frequency == 'Bi-Weekly':
            delta = datetime.timedelta(days=14)
            while current_date <= until_valid_date:
                cur.execute("INSERT INTO expense (title, date, nature, amount, isauto, frequency) VALUES (?, ?, ?, ?, ?, ?)",
                            (name_text, current_date.strftime('%Y-%m-%d'), nature_text, valid_amount, self.toggle_state, frequency))
                current_date += delta

        elif frequency == 'Monthly':
            while current_date <= until_valid_date:
                cur.execute("INSERT INTO expense (title, date, nature, amount, isauto, frequency) VALUES (?, ?, ?, ?, ?, ?)",
                            (name_text, current_date.strftime('%Y-%m-%d'), nature_text, valid_amount, self.toggle_state, frequency))
                current_date += relativedelta(months=1)  # Add one month

        elif frequency == 'Annually':
            while current_date <= until_valid_date:
                cur.execute("INSERT INTO expense (title, date, nature, amount, isauto, frequency) VALUES (?, ?, ?, ?, ?, ?)",
                            (name_text, current_date.strftime('%Y-%m-%d'), nature_text, valid_amount, self.toggle_state, frequency))
                current_date += relativedelta(years=1)  # Add one year

        # Commit the changes
        conn.commit()

        # Show Info
        messagebox.showinfo("Information", "Data are saved and fields will be reset.")

        # Reset fields
        self.entry_value_amountExpense.delete(0, tk.END)
        self.entry_value_dateExpense.delete(0, tk.END)
        self.entry_value_nameExpense.delete(0, tk.END)
        self.entry_value_natureExpense.delete(0, tk.END)
        self.entry_value_until.delete(0, tk.END)
        self.toggle_button.config(text='NO', bg='ivory')
        self.menu_button.config(text='Options')
        self.menu_button.config(state='disabled')
        self.entry_value_until.config(state='disabled')
        self.toggle_state = False



# Window to view expenses
class WindowViewExp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        title_font = font.Font(family="Helvetica", size=10, weight='bold')  # Font for the title
        slogan_font = font.Font(family="Comic Sans MS", size=20, weight='bold')  # Font for the slogan
        
        self.title('View Expenses')
        button_width = 20
        
        self.geometry('640x480')
        self.configure(bg='ivory')
        
        # Create a label to display "VIEW EXPENSES"
        self.lbl_msg = tk.Label(self, text="VIEW EXPENSES", font=slogan_font, anchor='center', foreground='red', bg='ivory')
        self.lbl_msg.place(x=190, y=5)
        
        # Create a back button
        self.save_button = tk.Button(self, text='BACK', command=self.back, width=15)
        self.save_button.place(x=30, y=430)
        
        # Create treeview for showing expenses with specific column headings
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Date", "Nature", "Amount", "Is Auto", "Frequency"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Nature", text="Nature")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Is Auto", text="Is Auto")
        self.tree.heading("Frequency", text="Frequency")
        
        # Set the width of the columns
        self.tree.column("ID", width=20)
        self.tree.column("Title", width=150)
        self.tree.column("Date", width=70)
        self.tree.column("Nature", width=150)
        self.tree.column("Amount", width=80)
        self.tree.column("Is Auto", width=80)
        self.tree.column("Frequency", width=80)
        
        self.tree.place(x=30, y=70, width=575, height=350)
        
        # Load data into the Treeview
        self.load_data()
        
        # Create a context menu
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Edit", command=self.edit_item)
        self.popup_menu.add_command(label="Delete", command=self.delete_item)

        # Bind right-click to show the context menu and record the clicked position
        self.tree.bind("<Button-3>", self.show_popup_menu)

    # Display the context menu at the right-click position
    def show_popup_menu(self, event):
        self.popup_menu.post(event.x_root, event.y_root)
        self.selected_item = self.tree.identify_row(event.y)  # Record the selected item

    # Open the edit window to modify the selected item
    def edit_item(self):
        if not self.selected_item:
            return
        
        item_values = self.tree.item(self.selected_item, 'values')
        EditWindow(self, self.selected_item, item_values)  # Display a form to edit details
        
    # Delete the selected item after confirmation
    def delete_item(self):
        if not self.selected_item:
            return
        
        if messagebox.askyesno("Delete", "Are you sure you want to delete this entry?"):
            item_id = self.tree.item(self.selected_item, 'values')[0]  # Get the ID of the selected item
            
            conn = sqlite3.connect('Expenses.db')
            cur = conn.cursor()
            
            cur.execute("DELETE FROM expense WHERE id=?", (item_id,))  # Delete the entry from the database
            conn.commit()
            conn.close()
            
            self.tree.delete(self.selected_item)  # Delete the entry from the Treeview
            self.selected_item = None  # Reset the selection
    
    # Load data from the SQLite database into the Treeview
    def load_data(self):
        conn = sqlite3.connect('Expenses.db')
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM expense")  # Retrieve expense data
        rows = cur.fetchall()
        
        for row in rows:
            is_auto = "Yes" if row[5] else "No"  # Convert boolean values to text
            self.tree.insert("", tk.END, iid=row[0], values=(row[0], row[1], row[2], row[3], row[4], is_auto, row[6]))
        
        conn.close()
    
    # Close the current window and go back to the previous window
    def back(self):
        self.destroy()
        back = Windowthree()
        back.mainloop() 



class EditWindow(tk.Toplevel):
    def __init__(self, parent, item_id, item_values):
        super().__init__(parent)
        self.parent = parent
        self.item_id = item_id
        self.item_values = item_values
        
        self.title("Edit Expense")
        
        # Create fields to edit the data
        tk.Label(self, text="Title").grid(row=0, column=0, padx=10, pady=10)
        self.title_entry = tk.Entry(self)
        self.title_entry.insert(0, item_values[1])
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Date").grid(row=1, column=0, padx=10, pady=10)
        self.date_entry = tk.Entry(self)
        self.date_entry.insert(0, item_values[2])
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Nature").grid(row=2, column=0, padx=10, pady=10)
        self.nature_entry = tk.Entry(self)
        self.nature_entry.insert(0, item_values[3])
        self.nature_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Amount").grid(row=3, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.insert(0, item_values[4])
        self.amount_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Create a Save button to save the changes
        tk.Button(self, text="Save", command=self.save_changes).grid(row=6, column=0, columnspan=2, pady=10)
    
    def save_changes(self):
        # Update the data in the database
        conn = sqlite3.connect('Expenses.db')
        cur = conn.cursor()
        
        cur.execute('''
            UPDATE expense
            SET title=?, date=?, nature=?, amount=?
            WHERE id=?
        ''', (
            self.title_entry.get(),
            self.date_entry.get(),
            self.nature_entry.get(),
            int(self.amount_entry.get()),
            self.item_id
        ))
        conn.commit()
        conn.close()
        
        # Update the data in the Treeview of the parent window
        self.parent.tree.item(self.item_id, values=(
            self.item_id,
            self.title_entry.get(),
            self.date_entry.get(),
            self.nature_entry.get(),
            float(self.amount_entry.get()),
            "Yes" if self.item_values[5] else "No",
            self.item_values[6]
        ))
        
        self.destroy()  # Close the edit window



class WindowSummary(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Define fonts for different labels
        title_font = font.Font(family="Helvetica", size=10, weight='bold')
        slogan_font = font.Font(family="Comic Sans MS", size=30, weight='bold')
        result_font = font.Font(family="Helvetica", size=7)
        
        self.title('Summary')
        self.geometry('640x480')
        self.configure(bg='light pink')
        
        # Load the current date to get the month and year
        now = datetime.datetime.now()
        current_month, current_year = now.month, now.year
        date_from, date_to = self.get_month_range(current_year, current_month)
        
        # Load image with Pillow
        img = str(current_month) + '.png'
        try:
            self.image = Image.open(img)  # Call the Main Menu
            new_size = (150, 94)  # Define the new size 
            self.image = self.image.resize(new_size, Image.LANCZOS)  # Resize the image
            self.image_tk = ImageTk.PhotoImage(self.image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_tk = None
        
        # Display the image if loaded successfully, otherwise show an error message
        if self.image_tk:
            self.image_label = tk.Label(self, image=self.image_tk)
            self.image_label.place(x=10, y=200)
        else:
            self.image_label = tk.Label(self, text="Image could not be loaded.")
            self.image_label.place(x=30, y=100)
        
        # Create a label for the summary title
        self.lbl_msg = tk.Label(self, text="Summary", font=slogan_font, anchor='center', fg='black', bg='light pink')
        self.lbl_msg.place(x=245, y=5)

        # Create a back button
        self.back_button = tk.Button(self, text='BACK', command=self.back, width=15)
        self.back_button.place(x=30, y=430)
        
        # Create labels for total sum and number of expenses
        self.label_totalSum = tk.Label(self, text='', bg='light pink', font=result_font, fg='black', justify='right')
        self.label_totalSum.place(x=531, y=433)
        
        self.label_count = tk.Label(self, text='', bg='light pink', font=result_font, fg='black', justify='right')
        self.label_count.place(x=170, y=433)

        # Create a Treeview to display expenses
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Date", "Nature", "Amount"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Nature", text="Nature")
        self.tree.heading("Amount", text="Amount")
        
        self.tree.column("ID", width=20)
        self.tree.column("Title", width=100)
        self.tree.column("Date", width=50)
        self.tree.column("Nature", width=100)
        self.tree.column("Amount", width=80)
        
        self.tree.place(x=170, y=100, width=450, height=330)
        
        # Load data into the Treeview
        self.load_data(date_from, date_to, '')
    
    def get_month_range(self, year, month):
        # Get the first and last day of the month
        first_day = f"{year}-{month:02d}-01"
        next_month = month % 12 + 1
        next_year = year if next_month > 1 else year + 1
        last_day = f"{next_year}-{next_month:02d}-01"
        last_day = datetime.datetime.strptime(last_day, '%Y-%m-%d') - timedelta(days=1)
        last_day = last_day.strftime('%Y-%m-%d')
        return first_day, last_day
    
    def load_data(self, dateFrom, dateTo, nat):
        try:
            # Connect to SQLite database
            conn = sqlite3.connect('Expenses.db')
            cur = conn.cursor()

            # Query to get expenses between date range and filter by nature if provided
            query = """
                SELECT * FROM expense 
                WHERE date BETWEEN ? AND ?
                {}
            """.format(f"AND nature= '{nat}'" if nat else '')

            cur.execute(query, (dateFrom, dateTo))
            rows = cur.fetchall()

            # Insert fetched data into the Treeview
            for row in rows:
                self.tree.insert("", tk.END, iid=row[0], values=(row[0], row[1], row[2], row[3], row[4]))

            # Query to get the sum of amounts for the given date range and nature
            query_sum = """
                SELECT SUM(amount) FROM expense 
                WHERE date BETWEEN ? AND ?
                {}
            """.format(f"AND nature= '{nat}'" if nat else '')

            cur.execute(query_sum, (dateFrom, dateTo))
            total_sum = cur.fetchone()[0]
            total_sum = float(total_sum) if total_sum is not None else 0

            # Query to get the count of expenses for the given date range and nature
            query_count = """
                SELECT COUNT(amount) FROM expense 
                WHERE date BETWEEN ? AND ?
                {}
            """.format(f"AND nature= '{nat}'" if nat else '')

            cur.execute(query_count, (dateFrom, dateTo))
            count = cur.fetchone()[0]
            count = int(count) if count is not None else 0

            # Update the total sum and count labels
            self.label_totalSum.config(text=f"Total Sum: {total_sum:.2f}")
            self.label_count.config(text=f"Number of Expenses: {count:.0f}")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        finally:
            conn.close()

    def back(self):
        # Close the current window and open the previous window
        self.destroy()
        # Call the Main Menu
        back = Windowthree()
        back.mainloop()

class WindowPassword(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Define fonts for different labels
        title_font = font.Font(family="Helvetica", size=10, weight='bold') # for the title
        slogan_font = font.Font(family="Comic Sans MS", size=30, weight='bold') # to display the number
        result_font = font.Font(family="Helvetica", size=7) # for the title
        
        self.title('Password')
        button_width = 20
        
        self.geometry('640x480')
        self.configure(bg='purple')
        
        # Load image with Pillow
        try:
            self.image = Image.open('password1.png')  # Call the Main Menu
            new_size = (157, 157)  # Define the new size 
            self.image = self.image.resize(new_size, Image.LANCZOS)  # Resize the image
            self.image_tk = ImageTk.PhotoImage(self.image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_tk = None
        
        # Display the image if loaded successfully, otherwise show an error message
        if self.image_tk:
            self.image_label = tk.Label(self, image=self.image_tk)
            self.image_label.place(x=250, y=70)
        else:
            self.image_label = tk.Label(self, text="Image could not be loaded.")
            self.image_label.place(x=250, y=70)
    
        # Create a label for the password reset title
        self.lbl_msg = tk.Label(self, text="Reset Password", font=slogan_font, anchor='center', foreground='white', bg='purple')
        self.lbl_msg.place(x=195, y=5)
        
        # Create a back button
        self.back_button = tk.Button(self, text='BACK', command=self.back, width=15)
        self.back_button.place(x=30, y=430)
        
        # Connect to SQLite database
        self.conn = sqlite3.connect('Expenses.db')
        self.cur = self.conn.cursor()

        # Initialize the password in the database
        self.initialize_password()
        self.create_widgets()
        
    def initialize_password(self):
        # Add a default password if it does not exist
        self.cur.execute("SELECT * FROM user_password WHERE id = 1")
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO user_password (password) VALUES (?)", ('dodo1234',))
            self.conn.commit()

    def create_widgets(self):
        # Create widgets for current password, new password, and confirm new password

        # Current Password
        self.current_password_label = tk.Label(self, text="Current Password", bg='#5B05E2')
        self.current_password_label.place(x=203, y=250)
        self.current_password_entry = tk.Entry(self, show='*')
        self.current_password_entry.place(x=320, y=251)

        # New Password
        self.new_password_label = tk.Label(self, text="New Password", bg='#5B05E2')
        self.new_password_label.place(x=218, y=300)
        self.new_password_entry = tk.Entry(self, show='*')
        self.new_password_entry.place(x=320, y=301)

        # Confirm New Password
        self.confirm_password_label = tk.Label(self, text="Confirm New Password", bg='#5B05E2')
        self.confirm_password_label.place(x=170, y=350)
        self.confirm_password_entry = tk.Entry(self, show='*')
        self.confirm_password_entry.place(x=320, y=351)

        # Change Password Button
        self.change_password_button = tk.Button(self, text="Change Password", command=self.change_password, bg='#5B05E2')
        self.change_password_button.place(x=260, y=400)

    def change_password(self):
        # Get input values from the entries
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate input
        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match")
            return

        if not self.is_valid_password(new_password):
            messagebox.showerror("Error", "New password must be at least 8 characters long and contain both letters and numbers")
            return

        # Verify current password
        self.cur.execute("SELECT password FROM user_password WHERE id = 1")
        stored_password = self.cur.fetchone()

        if stored_password is None or stored_password[0] != current_password:
            messagebox.showerror("Error", "Current password is incorrect")
            return

        # Update the password in the database
        self.cur.execute("UPDATE user_password SET password = ? WHERE id = 1", (new_password,))
        self.conn.commit()
        messagebox.showinfo("Success", "Password changed successfully")
        
        print(f"Current Password: {stored_password[0]}")
        self.back()
        
    def is_valid_password(self, password):
        # Password must be at least 8 characters long and contain both letters and numbers
        return len(password) >= 8 and re.search(r'[A-Za-z]', password) and re.search(r'[0-9]', password)

    def close(self):
        # Close the database connection
        self.conn.close()
    
    def back(self):
        # Close the current window and open the previous window
        self.destroy()
        # Call the Main menu
        back = Windowthree()
        back.mainloop()
    

window_one = WindowOne()
window_one.mainloop()

# Close the connection
conn.close()
