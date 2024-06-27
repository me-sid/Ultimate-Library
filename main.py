from funcs import UltimateLib
a = UltimateLib("localhost", "your_username", "your_password", "your_database")
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
        a.issue_book(book_name, person)
    elif choice == '2':
        a.return_book()
    elif choice == '3':
        bookname = input("Enter book name: ")
        print(a.b_availability(bookname))
    elif choice == '4':
        person = input("Enter name: ")
        print(a.person_history(person))
    
    # Book guide 
    elif choice == '5':
        choice2=""
        while choice2 != 'b':
            choice2 = input(book_guide_str)
            if choice2 == '1':
                for i in a.available_books():
                    print(i[1])
            elif choice2 == '2':
                bookname = input("Enter book name: ")
                print(a.book_history(bookname))
            elif choice2 == '3':
                start_r = int(input("Enter start range: "))
                end_r = int(input("Enter end range: "))
                print(a.search_by_rating(start_r, end_r))
            elif choice2 == '4':
                gen = input("Enter genre: ")
                print(a.search_by_genre(gen))
            elif choice2 == '5':
                bookname = input("Enter book name: ")
                print(a.about_book(bookname))
            elif choice2=='6':
                bookname = input("Enter book name: ")
                quantity_n = int(input("Enter quantity: "))
                a.change_book_quantity(bookname, quantity_n)
            elif choice2=='b':
                pass
            else:
                print("Invalid entry")

    elif choice == '6':
        bookname = input("Enter book name: ")
        authorname = input("Enter author name: ")
        genre = input("Enter genre: ")
        rating = int(input("Enter rating- "))
        quantity = input("Enter quantity(default=1) -")
        if quantity == '':
            quantity = 1
        else:
            quantity = int(quantity)
        a.add_book(bookname, authorname, genre, rating, quantity)
    elif choice == 'q':
        pass
    else:
        print("Invalid entry please try again!")

print("Bye Bye!")
