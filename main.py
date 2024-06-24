import mysql.connector
import datetime
host="localhost"
username="root"
password="siddhurocks"
database="testbase"


mydb = mysql.connector.connect(host=host, username=username, password=password, database=database)
cur = mydb.cursor()


def check_table():
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    tables = [table[0] for table in tables]
    if "books" not in tables:
        cur.execute("create table books(id int NOT NULL auto_increment, person varchar(255) not null, book varchar(255) not null, issue_date datetime default current_timestamp, return_date datetime, primary key(id) );")



def issue_book(book_name:str, person_name:str):
    cmd = f"""insert into books(person, book) values(%s, %s)"""
    val = (person_name.title(), book_name.title())
    cur.execute(cmd, val)
    mydb.commit()

def return_book():
    cur.execute("select id, person, book from books where return_date IS NULL")
    names = cur.fetchall()
    for i in names:
        print(i)
    issue_id = int(input("Enter issue id->"))
    cmd = "update books set return_date=%s where id = %s"
    val = (datetime.datetime.now(),issue_id)
    cur.execute(cmd, val)
    mydb.commit()


def book_history(name:str):
    cmd = "select * from books where book=%s"
    val = (name.title(),)
    cur.execute(cmd, val)
    his = cur.fetchall()
    for i in his:
        print(f"Issue Number:{i[0]}\nName:{i[1]}\nIssue Datetime:{i[3]}\nReturn Datetime:{i[4]}")
        print("------------")


def person_history(name:str):
    cmd = "select * from books where person=%s"
    val= (name.title(),)
    cur.execute(cmd, val)
    his = cur.fetchall()
    for i in his:
        print(f"Issue Number:{i[0]}\nBook:{i[2]}\nIssue Datetime:{i[3]}\nReturn Datetime:{i[4]}")
        print("------------")



if __name__ == "__main__":
    check_table()
    instruc = "1-> Issue Book\n2-> Return Book\n3-> Book History\n4-> Person History\n q-> Quit\n-------------\n"
    while True:
        a = input(instruc)
        if a == '1':
            book_n = input("Enter book name: ")
            p_name = input("Enter name of borrower: ")
            issue_book(book_n, p_name)
        elif a == '2':
            return_book()
        elif a == '3':
            book_n = input("Enter book name: ")
            book_history(book_n)
        elif a == '4':
            p_name = input("Enter name of person: ")
            person_history(p_name)
        elif a == 'q':
            print("Bye Bye!")
            break
        else:
            print("Invalid Input try again!")