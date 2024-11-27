## Book Database Application

This is a Python-based GUI application for managing a book database. It allows users to view, add, modify, and delete book records stored in a MySQL database. The application uses `Tkinter` for the graphical user interface and `mysql.connector` for database interaction.

## Features

- **View All Records:** Displays all book records in a list.
- **Add New Book:** Insert a new book into the database with details like title, author, and ISBN.
- **Modify Book Record:** Update the details of an existing book.
- **Delete Book Record:** Remove a book from the database.
- **Clear Screen:** Clears all fields and resets the selected record.
- **Exit Application:** Closes the application with a confirmation prompt.

## Requirements

- Python 3.x
- Tkinter (for GUI)
- mysql-connector-python (for MySQL database interaction)

You can install the necessary libraries using pip:

bash
```pip install mysql-connector-python```

## Usage
Start the application: Run the Python script using any Python IDE or command line.

```python your_script_name.py```

## Code Overview
- Bookdb Class: Handles all database interactions such as connecting, inserting, updating, and deleting records.
- Tkinter GUI: Creates the main window with input fields, buttons, and a listbox to interact with the 

## **Database Configuration**

The application connects to a MySQL database. Ensure that the database is set up correctly, and update the mysql_config.py file with the appropriate credentials.

 mysql_config.py
```db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database_name'
}```
