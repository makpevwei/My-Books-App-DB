from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, N, S, END
from tkinter import ttk
from tkinter import messagebox
from mysql_config import db_config
import mysql.connector as pyo

class Bookdb:
    """
    A class to handle all database operations for the book database application.
    """

    def __init__(self):
        """
        Initialize the database connection and cursor.
        """
        self.conn = pyo.connect(**db_config)
        self.cursor = self.conn.cursor()
        print("You have connected to the database")
        print(self.conn)

    def __del__(self):
        """
        Close the database connection when the object is destroyed.
        """
        self.conn.close()

    def view(self):
        """
        Retrieve all books from the database.

        Returns:
            list: A list of tuples containing book information.
        """
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return rows

    def insert(self, title, author, isbn):
        """
        Insert a new book into the database.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN of the book.
        """
        sql = "INSERT INTO books(title, author, isbn) VALUES (%s, %s, %s)"
        values = [title, author, isbn]
        self.cursor.execute(sql, values)
        self.conn.commit()
        messagebox.showinfo(title="Book Database", message="New book added to database")

    def update(self, id, title, author, isbn):
        """
        Update an existing book in the database.

        Args:
            id (int): The ID of the book to update.
            title (str): The new title of the book.
            author (str): The new author of the book.
            isbn (str): The new ISBN of the book.
        """
        tsql = "UPDATE books SET title = %s, author = %s, isbn = %s WHERE id = %s"
        self.cursor.execute(tsql, [title, author, isbn, id])
        self.conn.commit()
        messagebox.showinfo(title="Book Database", message="Book Updated")

    def delete(self, id):
        """
        Delete a book from the database.

        Args:
            id (int): The ID of the book to delete.
        """
        delquery = "DELETE FROM books WHERE id = %s"
        self.cursor.execute(delquery, [id])
        self.conn.commit()
        messagebox.showinfo(title="Book Database", message="Book Deleted")


# Initialize the database object
db = Bookdb()

# Global variable to track the selected row
selected_tuple = None

def get_selected_row(event):
    """
    Handle the event when a row is selected in the listbox.

    Args:
        event: The event object (not used but required for event binding).
    """
    global selected_tuple
    try:
        index = list_box.curselection()[0]
        selected_tuple = list_box.get(index)
        title_entry.delete(0, "end")
        title_entry.insert("end", selected_tuple[1])
        author_entry.delete(0, "end")
        author_entry.insert("end", selected_tuple[2])
        isbn_entry.delete(0, "end")
        isbn_entry.insert("end", selected_tuple[3])
    except IndexError:
        selected_tuple = None

def view_records():
    """
    Display all records in the listbox.
    """
    list_box.delete(0, "end")
    for row in db.view():
        list_box.insert("end", row)

def add_book():
    """
    Add a new book to the database and update the listbox.
    """
    try:
        db.insert(title_text.get(), author_text.get(), int(isbn_text.get()))
        list_box.delete(0, "end")
        list_box.insert("end", (title_text.get(), author_text.get(), isbn_text.get()))
        title_entry.delete(0, "end")
        author_entry.delete(0, "end")
        isbn_entry.delete(0, "end")
    except ValueError:
        messagebox.showerror("Input Error", "ISBN must be a numeric value.")

def delete_records():
    """
    Delete the selected book from the database and update the listbox.
    """
    global selected_tuple
    try:
        if selected_tuple:
            db.delete(selected_tuple[0])
            selected_tuple = None  # Reset after deletion
            view_records()
        else:
            messagebox.showerror("Error", "No record selected to delete!")
    except NameError:
        messagebox.showerror("Error", "No record selected to delete!")

def update_records():
    """
    Update the selected book in the database and refresh the listbox.
    """
    global selected_tuple
    try:
        if selected_tuple:
            isbn = int(isbn_text.get())  # Ensure ISBN is numeric
            db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn)
            selected_tuple = None  # Reset after updating
            title_entry.delete(0, "end")
            author_entry.delete(0, "end")
            isbn_entry.delete(0, "end")
            view_records()
        else:
            messagebox.showerror("Error", "No record selected to modify!")
    except ValueError:
        messagebox.showerror("Input Error", "ISBN must be a numeric value.")
    except NameError:
        messagebox.showerror("Error", "No record selected to modify!")

def clear_screen():
    """
    Clear all entry fields and reset the selected tuple.
    """
    global selected_tuple
    list_box.delete(0, "end")
    title_entry.delete(0, "end")
    author_entry.delete(0, "end")
    isbn_entry.delete(0, "end")
    selected_tuple = None  # Reset selected tuple

def on_closing():
    """
    Handle the window closing event.
    """
    global db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        del db

# Create the main window
window = Tk()
window.title("My Books Database Application")
window.configure(background="light blue")
window.geometry("800x500")
window.resizable(width=False, height=False)

# Configure the grid layout for the main window
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=2)
window.grid_rowconfigure(4, weight=1)

# Title input
title_label = ttk.Label(window, text="Title", background="light blue", font=("TkDefaultFont", 12))
title_label.grid(row=0, column=0, sticky=W, padx=10, pady=5)
title_text = StringVar()
title_entry = ttk.Entry(window, width=30, textvariable=title_text)
title_entry.grid(row=0, column=1, sticky=W, padx=10, pady=5)

# Author input
author_label = ttk.Label(window, text="Author", background="light blue", font=("TkDefaultFont", 12))
author_label.grid(row=1, column=0, sticky=W, padx=10, pady=5)
author_text = StringVar()
author_entry = ttk.Entry(window, width=30, textvariable=author_text)
author_entry.grid(row=1, column=1, sticky=W, padx=10, pady=5)

# ISBN input
isbn_label = ttk.Label(window, text="ISBN", background="light blue", font=("TkDefaultFont", 12))
isbn_label.grid(row=2, column=0, sticky=W, padx=10, pady=5)
isbn_text = StringVar()
isbn_entry = ttk.Entry(window, width=30, textvariable=isbn_text)
isbn_entry.grid(row=2, column=1, sticky=W, padx=10, pady=5)

# Add Book button
add_button = Button(window, text="Add Book",
                    bg="white", fg="blue",
                    font="helvetica 10 bold", command=add_book)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

# Listbox to display books with a vertical scrollbar
list_box = Listbox(window, height=12, width=40, font="helvetica 12", bg="light blue")
list_box.grid(row=0, column=2, rowspan=5, sticky=W + E + N + S, padx=10, pady=10)
list_box.bind("<<ListboxSelect>>", get_selected_row)

scrollbar = Scrollbar(window, orient="vertical")
scrollbar.grid(row=0, column=3, rowspan=5, sticky=N + S, pady=10)

# Configure the Listbox and Scrollbar to work together
list_box.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=list_box.yview)

# Frame for action buttons at the bottom
button_frame = ttk.Frame(window)
button_frame.grid(row=5, column=0, columnspan=4, pady=10)

# Modify Record button
modify_button = Button(button_frame, text="Modify Record",
                       fg="purple", bg="white", font="helvetica 10 bold", command=update_records)
modify_button.grid(row=0, column=0, padx=5)

# Delete Record button
delete_button = Button(button_frame, text="Delete Record",
                       fg="purple", bg="white", font="helvetica 10 bold", command=delete_records)
delete_button.grid(row=0, column=1, padx=5)

# View all records button
view_button = Button(button_frame, text="View all records",
                     fg="purple", bg="white", font="helvetica 10 bold", command=view_records)
view_button.grid(row=0, column=2, padx=5)

# Clear Screen button
clear_button = Button(button_frame, text="Clear Screen",
                      fg="purple", bg="white", font="helvetica 10 bold", command=clear_screen)
clear_button.grid(row=0, column=3, padx=5)

# Exit Application button
exit_button = Button(button_frame, text="Exit Application",
                     fg="purple", bg="white", font="helvetica 10 bold", command=on_closing)
exit_button.grid(row=0, column=4, padx=5)

# Set up the window close event
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main event loop to run the application
window.mainloop()

