import sqlite3
import datetime


class UltimateLib:

    def __init__(self, database):
        # Creating database connection
        self.mydb = sqlite3.connect(database)
        self.cur = self.mydb.cursor()

        # Check and create tables if they don't exist
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS issue_book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person TEXT NOT NULL,
            book TEXT NOT NULL,
            issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            return_date TIMESTAMP
        )
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books_detail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT NOT NULL,
            author_name TEXT NOT NULL,
            rating REAL CHECK (rating >= 0 AND rating <= 10),
            genre TEXT,
            quantity INTEGER DEFAULT 0
        )
        """)
        self.mydb.commit()

    def check_book(self, book_name):
        """Check if book is in books_detail table"""
        self.cur.execute("SELECT book_name FROM books_detail")
        book_list = self.cur.fetchall()
        return any(book_name.title() == i[0] for i in book_list)

    def add_book(self,
                 book_name: str,
                 author_name: str,
                 genre: str,
                 rating=None,
                 quantity=1):
        """Adds book to books_detail table"""
        if self.check_book(book_name):
            return("Book already exists! Try changing the book quantity.")
        else:
            if rating is not None and not (0 <= rating <= 10):
                print("Invalid rating range")
            else:
                vals = (book_name.title(), author_name.title(), rating,
                        genre.title(), quantity)
                self.cur.execute(
                    "INSERT INTO books_detail (book_name, author_name, rating, genre, quantity) VALUES (?, ?, ?, ?, ?)",
                    vals)
                self.mydb.commit()
                return "book added successfully!"

    def change_book_quantity(self, book_name, quantity):
        """Changes quantity of book in books_detail table"""
        if self.check_book(book_name):
            self.cur.execute(
                "UPDATE books_detail SET quantity = ? WHERE book_name = ?",
                (quantity, book_name.title()))
            self.mydb.commit()
            return "Book quantity changed!"
        else:
            return "Book not found!"

    def b_availability(self, book_name: str):
        """Checks if book exists and quantity is more than 0"""
        self.cur.execute(
            "SELECT quantity FROM books_detail WHERE book_name = ?",
            (book_name.title(), ))
        book = self.cur.fetchone()
        return book is not None and book[0] > 0

    def issue_book(self, book_name: str, person_name: str):
        """Issues the book"""
        if self.b_availability(book_name):
            self.cur.execute(
                "INSERT INTO issue_book (person, book) VALUES (?, ?)",
                (person_name.title(), book_name.title()))
            self.cur.execute(
                "UPDATE books_detail SET quantity = quantity - 1 WHERE book_name = ?",
                (book_name.title(), ))
            self.mydb.commit()
            return ("Book issued successfully!")
        else:
            return ("Sorry, book is not available!")

    def return_book(self, book_name, borrower):
        """Returns issued book"""
        try:
            # First update the issue_book table to set the return_date
            self.cur.execute("""
                UPDATE issue_book 
                SET return_date = ? 
                WHERE person = ? AND book = ? AND return_date IS NULL
            """, (datetime.datetime.now(), borrower, book_name))
            
            # Check if any row was updated
            if self.cur.rowcount == 0:
                return "No record found!"

            self.mydb.commit()

            # Update the quantity in the books_detail table
            self.cur.execute("""
                UPDATE books_detail 
                SET quantity = quantity + 1 
                WHERE book_name = ?
            """, (book_name, ))
            
            self.mydb.commit()

            return "Book returned!"
        
        except Exception as e:
            return f"An error occurred: {e}"

            

    def about_book(self, book_name):
        """Tells all details about the book"""
        if self.check_book(book_name):
            self.cur.execute("SELECT * FROM books_detail WHERE book_name = ?",
                             (book_name.title(), ))
            about = self.cur.fetchone()
            return f"Book id: {about[0]}\nBook name: {about[1]}\nAuthor: {about[2]}\nRating: {about[3]}\nGenre: {about[4]}\nQuantity: {about[5]}"
        else:
            return "Sorry, we don't have that book yet!"

    def search_by_genre(self, genre):
        """Returns books by genre as a string"""
        self.cur.execute("SELECT * FROM books_detail WHERE genre = ?",
                         (genre.title(), ))
        list1 = self.cur.fetchall()
        return "\n\n".join([
            f"Book id: {i[0]}\nBook name: {i[1]}\nAuthor: {i[2]}\nRating: {i[3]}\nGenre: {i[4]}\nQuantity: {i[5]}"
            for i in list1
        ])

    def search_by_rating(self, start=0, end=10):
        """Returns books by rating as a string"""
        self.cur.execute(
            "SELECT * FROM books_detail WHERE rating BETWEEN ? AND ?",
            (start, end))
        list1 = self.cur.fetchall()
        return "\n\n".join([
            f"Book id: {i[0]}\nBook name: {i[1]}\nAuthor: {i[2]}\nRating: {i[3]}\nGenre: {i[4]}\nQuantity: {i[5]}"
            for i in list1
        ])

    def person_history(self, name: str):
        """Returns the issue and return history of a person as a string"""
        self.cur.execute(
            "SELECT id, book, issue_date, return_date FROM issue_book WHERE person = ?",
            (name.title(), ))
        list1 = self.cur.fetchall()
        return "\n\n".join([
            f"Issue id: {i[0]}\nBook Name: {i[1]}\nIssue Date: {i[2]}\nReturn Date: {i[3]}"
            for i in list1
        ])

    def book_history(self, book_name: str):
        """Returns book history as a string"""
        self.cur.execute(
            "SELECT id, person, issue_date, return_date FROM issue_book WHERE book = ?",
            (book_name.title(), ))
        list1 = self.cur.fetchall()
        return "\n\n".join([
            f"Issue id: {i[0]}\nBorrower's Name: {i[1]}\nIssue Date: {i[2]}\nReturn Date: {i[3]}"
            for i in list1
        ])

    def available_books(self):
        """returns a string of available books"""
        self.cur.execute("SELECT * FROM books_detail WHERE quantity > 0")
        stri = ""
        for i in self.cur.fetchall():
            stri += f"Book id: {i[0]}\nBook name: {i[1]}\nAuthor: {i[2]}\nRating: {i[3]}\nGenre: {i[4]}\nQuantity: {i[5]}\n\n"
        return stri
    
    def unreturned_books(self):
        """Returns a string of all unreturned books"""
        stri=""

        self.cur.execute("select * from issue_book where return_date is null")
        for i in self.cur.fetchall():
            stri += f"Id: {i[0]}\nName: {i[1]}\nBook: {i[2]}\nIssue Date: {i[3]}\n\n"
        return stri

