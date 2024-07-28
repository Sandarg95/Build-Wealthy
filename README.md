**Introduction**
Welcome to the Expense Management Application – BUILD WEALTHY! This application helps you track and manage your expenses efficiently. You can add, view summaries of your expenses, reset your password, and navigate through user-friendly interfaces. This manual will guide you through the installation, setup, and usage of the application.
Installation
Prerequisites
Before you begin, ensure you have the following installed on your system:
•	Python 3.x
•	Tkinter library (usually comes with Python)
•	Pillow library
•	SQLite3 library
Getting Started
Upon running the application, you will be presented with the main window. From here, you can navigate to different sections of the application such as adding expenses, viewing expenses, summary and resetting your password.

**Using the Application**

_Main Window_
The main window serves as the central hub of the application. From here, you can access other parts of the application.
Add Expenses
To add an expense, follow these steps:
1.	Open the Add Expense Form: In the main window, you will find a form to add new expenses.
2.	Fill in the Details: Enter the title, date, nature, and amount of the expense. If the expense is recurring, select "Add Auto," then choose the periodicity and the end date.
3.	Save the Expense: Click the Save button to add the expense to the database.
   
_View Expenses_
The View Expenses window allows you to view and manage your expenses. It includes the following features:
•	Back Button: Returns to the previous window.
•	Expense Treeview: Lists all expenses with details such as ID, Title, Date, Nature, Amount, Is Auto, and Frequency.
•	Context Menu: Right-click on an expense to edit or delete it.
How to Use
1.	Open the View Expenses Window: From the main window, navigate to the View Expenses window.
2.	View Expenses: The expenses will be displayed in a tree view format.
3.	Edit or Delete an Expense: Right-click on an expense to bring up the context menu. Choose Edit to modify the expense details or Delete to remove it from the database.
   
_Summary Window_
The Summary Window displays a summary of your expenses for the current month. It includes the following features:
•	Image Display: Shows an image related to the current month.
•	Summary Label: Displays a summary title.
•	Back Button: Returns to the previous window.
•	Total Sum Label: Shows the total sum of expenses.
•	Number of Expenses Label: Displays the number of recorded expenses.
•	Expense Treeview: Lists all expenses with details such as ID, Title, Date, Nature, and Amount by order (date)
How to Use
1.	The Summary Window automatically loads data for the current month upon opening.
2.	You can view the total sum and number of expenses at the bottom of the window of the current month.
3.	To go back to the main window, click the BACK button.
   
_Password Reset Window_
The Password Reset Window allows you to reset your password. It includes the following features:
•	Image Display: Shows an image related to password reset.
•	Password Reset Label: Displays the title "Reset Password".
•	Current Password Entry: Field to enter your current password.
•	New Password Entry: Field to enter your new password.
•	Confirm New Password Entry: Field to confirm your new password.
•	Change Password Button: Changes your password if the conditions are met.
•	Back Button: Returns to the previous window.
How to Use
1.	Enter your current password in the "Current Password" field.
2.	Enter your new password in the "New Password" field.
3.	Confirm your new password by entering it again in the "Confirm New Password" field.
4.	Click the Change Password button to update your password.
5.	Click the BACK button to return to the previous window.
   
**Troubleshooting**
Common Issues
•	Error loading image: Ensure that the image file exists in the correct path and has the correct permissions.
•	Database connection errors: Verify that the Expenses.db file exists in the correct directory and is accessible.
Solutions
•	Image Loading Issues: The image file name corresponds to the current month and is placed in the correct directory-same file as the program.
•	Database Issues: Check that the database file is not corrupted and has the necessary tables created.

**FAQ**
1.	How do I add an expense?
o	You can add an expense by entering the details in the main window and saving them to the database.
2.	What if I forget my password?
o	The first password is dodo1234. You can reset your password from the Password Reset Window.
3.	Can I change the default image?
o	Yes, you can replace the image files with your own. Ensure the file names correspond to the months (e.g., ‘1.png’ for January).
Contact Information
For further assistance, you can reach out to our support team at:
•	Email: sandarg95@gmail.com
•	Phone: (317) 734-2233
Thank you for using the Expense Management Application- BUILD WEALTHY!
