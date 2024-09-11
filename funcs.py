import mysql.connector
import datetime


class UltimateLib:
    def __init__(self, host, username, password, database):
        # creating db connection
        self.mydb = mysql.connector.connect(host=host, username=username, password=password, database=database)
        self.cur = self.mydb.cursor()

        #check_tables
        self.cur.execute("SHOW TABLES")
        tables = self.cur.fetchall()
        tables = [table[0] for table in tables]
        if "issue_book" not in tables:
            self.cur.execute("create table issue_book(id int NOT NULL auto_increment, person varchar(255) not null, book varchar(255) not null, issue_date datetime default current_timestamp, return_date datetime, primary key(id) );")
        if "books_detail" not in tables:
            self.cur.execute("CREATE TABLE books_detail (id INT AUTO_INCREMENT PRIMARY KEY,book_name VARCHAR(255) NOT NULL,author_name VARCHAR(255) NOT NULL,rating FLOAT CHECK (rating >= 0 AND rating <= 10), genre varchar(100), quantity int default 0);")


    def check_book(self, book_name):
        """check if book is in books_detail table"""
        self.cur.execute("select book_name from books_detail")
        book_list=self.cur.fetchall()
        result = False
        for i in book_list:
            if i[0] == book_name.title():
                result = True
        return result


    def add_book(self, book_name:str, author_name:str, genre:str, rating=None, quantity=1):
        """adds book in books_detail table"""
        if self.check_book(book_name) is True:
            print("book already exist! Try changing the book quantity")
        else:
            if rating is not None and 0>rating>10:
                print("Invalid rating range")
            else:
                self.cur.execute("insert into books_detail(book_name, author_name, rating, genre, quantity) values(%s, %s, %s, %s, %s)", (book_name.title(), author_name.title(), rating, genre.title(), quantity))
                self.mydb.commit()


    def change_book_quantity(self, book_name, quantity):
        """changes quantity of book in book_details table"""
        if self.check_book(book_name) is True:
            self.cur.execute("select id, book_name, quantity from books_detail where book_name = %s", (book_name.title(),))
            bk = self.cur.fetchall()
            b_id = bk[0][0]
            self.cur.execute("update books_detail set quantity = %s where id=%s", (quantity, b_id))
            self.mydb.commit()
        else:
            print("Book not found")


    def b_availability(self, book_name:str):
        """checks if book exists in book_details table and quantity is more than 0"""
        self.cur.execute("select book_name, quantity from books_detail")
        book_list=self.cur.fetchall()
        result=False
        for i in book_list:
            if i[0] == book_name.title() and i[1] != 0:
                result = True
        return result


    def issue_book(self, book_name:str, person_name:str):
        """issue the book"""

        if self.b_availability(book_name) is True:
            self.cur.execute("insert into issue_book(person, book) values(%s, %s)", (person_name.title(), book_name.title()))
            self.mydb.commit()

            # update books_detail table 
            self.cur.execute("select id, quantity from books_detail where book_name=%s", (book_name.title(),))
            a = self.cur.fetchall()
            book_id = a[0][0]
            existing_quantity = a[0][1]
            self.cur.execute("update books_detail set quantity=%s where id=%s", (existing_quantity-1, book_id))
            self.mydb.commit()
            print("Book issued successfully!")
        
        else:
            print("Sorry book is not available!")


    def return_book(self):
        """return issued book"""
        self.cur.execute("select id, person, book from issue_book where return_date IS NULL")
        names = self.cur.fetchall()
        for i in names:
            print(i)
        issue_id = int(input("Enter issue id->"))
        cmd = "update issue_book set return_date=%s where id = %s"
        val = (datetime.datetime.now(),issue_id)
        self.cur.execute(cmd, val)
        self.mydb.commit()

        # update books_detail table 
        self.cur.execute("select id, quantity from books_detail where book_name=%s", ("book1",))
        a = self.cur.fetchall()
        book_id = a[0][0]
        existing_quantity = a[0][1]
        self.cur.execute("update books_detail set quantity=%s where id=%s", (existing_quantity+1, book_id))
        self.mydb.commit()
            

    def about_book(self, book_name):
        """tells all the details about the book as a string"""

        # check if book in db
        if self.check_book(book_name) is True:
            self.cur.execute("select * from books_detail where book_name = %s", (book_name.title(),))
            about = self.cur.fetchall()
            about = about[0]
            return f"Book id:{about[0]}\nBook name:{about[1]}\nAuthor: {about[2]}\nrating:{about[3]}\ngenre:{about[4]}\nQuantity:{about[5]}"
        else:
            return "Sorry we dont have that book yet!"


    def search_by_genre(self, genre):
        """returns books by genre as a string"""
        self.cur.execute("select * from books_detail where genre = %s", (genre,))
        list1 = self.cur.fetchall()
        ret_str = ""
        for i in list1:
            ret_str += f"Book id:{i[0]}\nBook name:{i[1]}\nAuthor: {i[2]}\nrating:{i[3]}\ngenre:{i[4]}\nQuantity:{i[5]}\n\n"
        return ret_str


    def search_by_rating(self, start=0, end=10):
        """returns books by rating as a string"""
        self.cur.execute("select * from books_detail where rating between %s and %s", (start, end))
        ret_str = ""
        for i in self.cur.fetchall():
            ret_str += f"Book id:{i[0]}\nBook name:{i[1]}\nAuthor: {i[2]}\nrating:{i[3]}\ngenre:{i[4]}\nQuantity:{i[5]}\n\n"
        return ret_str


    def person_history(self, name:str):
        """returns the issue and return history of a person as a string"""
        cmd = "select id, book, issue_date, return_date from issue_book where person=%s"
        val= (name.title(),)
        self.cur.execute(cmd, val)
        ret_str = ""
        for i in self.cur.fetchall():
            ret_str += f"Issue id:{i[0]}\nBook Name: {i[1]}\nIssue Date:{i[2]} Return Date:{i[3]}\n\n"
        return ret_str


    def book_history(self, book_name:str):
        """returns book history as string"""
        cmd = "select id, person, issue_date, return_date from issue_book where book=%s"
        val = (book_name.title(),)
        self.cur.execute(cmd, val)
        book_his_string =""
        for i in self.cur.fetchall():
            book_his_string += f"Issue id:{i[0]}\nBorrower's Name: {i[1]}\nIssue Date:{i[2]} Return Date:{i[3]}\n\n"
        return book_his_string

    def available_books(self):
        """yields a tuple of all available books"""
        self.cur.execute("select * from books_detail where quantity != 0")
        for i in self.cur.fetchall():
            yield i


