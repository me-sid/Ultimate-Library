from funcs import UltimateLib

# Database credentials
host = "localhost"
username = "root"
password = "your_mysql_password"
database_name = "your_database_name"

# Creating instance of UltimateLib class 
lib = UltimateLib(host=host, username=username, password=password, database=database_name)

print("Welcome to ultimate library!")
str1="""
----------------
1) Issue Book
2) Return Book
3) Check book availability
4) Person History
5) Book guide
6) Add book to lib
q) quit
----------------
enter your choice ->"""
book_guide_str = """
----------------
1) All available book list
2) Book History
3) Search book by book rating
4) Search book by genre
5) About book
6) Change book quantity
b) Back
----------------
enter your choice ->"""
choice = ""
while choice != "q":
    choice = input(str1)
    if choice=="1":
        book_name = input("Enter book name: ")
        person = input("Enter borrower's name: ")
        lib.issue_book(book_name, person)
    elif choice == '2':
        lib.return_book()
    elif choice == '3':
        bookname = input("Enter book name: ")
        print(lib.b_availability(bookname))
    elif choice == '4':
        person = input("Enter name: ")
        print(lib.person_history(person))
    
    # Book guide 
    elif choice == '5':
        choice2=""
        while choice2 != 'b':
            choice2 = input(book_guide_str)
            if choice2 == '1':
                for i in lib.available_books():
                    print(i[1])
            elif choice2 == '2':
                bookname = input("Enter book name: ")
                print(lib.book_history(bookname))
            elif choice2 == '3':
                start_r = int(input("Enter start range: "))
                end_r = int(input("Enter end range: "))
                print(lib.search_by_rating(start_r, end_r))
            elif choice2 == '4':
                gen = input("Enter genre: ")
                print(lib.search_by_genre(gen))
            elif choice2 == '5':
                bookname = input("Enter book name: ")
                print(lib.about_book(bookname))
            elif choice2=='6':
                bookname = input("Enter book name: ")
                quantity_n = int(input("Enter quantity: "))
                lib.change_book_quantity(bookname, quantity_n)
            elif choice2=='b':
                pass
            else:
                print("Invalid entry")

    elif choice == '6':
        bookname = input("Enter book name: ")
        authorname = input("Enter author name: ")
        genre = input("Enter genre: ")
        rating = float(input("Enter rating (out of 10)- "))
        quantity = input("Enter quantity(default=1) -")
        if quantity == '':
            quantity = 1
        else:
            quantity = int(quantity)
        lib.add_book(bookname, authorname, genre, rating, quantity)
    elif choice == 'q':
        pass
    else:
        print("Invalid entry please try again!")

print("Bye Bye!")
