import tkinter as tk
from funcs import UltimateLib

# creating lib instance
lib = UltimateLib("lib1")
# all entry widgets
entry_widgets = []

# Window
root = tk.Tk()
root.title("The Ultimate Library")
root.geometry('1000x600')
root.minsize(width=850, height=400)

# --------------------------------Frames---------------------------------------------
# heading frame
heading_f = tk.Frame(root, bg='#1E1F22')
heading_f.pack(fill='x', pady=0)

heading_l = tk.Label(heading_f,
                     text="The Ultimate Library", fg="#7591c9", bg="#1E1F22", font=("georgia", 40, "italic"))
heading_l.pack(pady=20)

# navbar
nav_f = tk.Frame(root, bg='#1E1F22')
nav_f.pack(side='left', fill='y')

# main frame
main_f = tk.Frame(root, bg='#303236')
main_f.pack(fill="both", expand=True)


# Home labels
main_l = tk.Label(main_f, text="Welcome,", bg="#303236", fg="white", font=("georgia", 25, "italic"))
main_l.pack(side=tk.TOP, fill=tk.X)  # Expand horizontally only, stay at top

home_msg = """The Ultimate Library app gives you all the tools required to help a librarian with digital library management at one place.
It is a 2-page GUI program which makes library management paper free!"""
tk.Label(main_f, text=home_msg, bg="#303236", fg="white", font=("MS UI Gothic", 14), wraplength=700).pack(side=tk.TOP, fill=tk.X)


#---------------------------style elements---------------------------
# create label - input pair in main frame
def label_input(label_text, frame):
                     global entry_widgets
                     tk.Label(frame, text=label_text, font=("Arial", 16), bg="#303236", fg="white").pack(pady=5)
                     entry = tk.Entry(frame, font=("Arial", 14), fg="lightgreen", bg="#303236", bd=2, relief="solid",highlightthickness=2, highlightbackground="lightgreen", highlightcolor="white", width=30)
                     entry.pack()
                     entry_widgets.append(entry)

# create button - input pair in main frame
def button_main(button_text, fun):
        button = tk.Button(main_f, text=button_text, 
                   bg="#68c4b5",  # Background color
                   fg="black",   # Text color
                   font=("Helvetica", 14),  # Font style
                   bd=2,  # Border width
                   relief="groove",
                   command=fun)
        button.pack(pady=8)

# alert 
def show_alert(message):
    # Create a frame for the alert
    alert_frame = tk.Frame(root, bg="#acd952", bd=2, relief="solid")
    alert_frame.place(relx=0.55, rely=0.2, anchor="center", width=300, height=100)

    # Add a label inside the alert frame
    label = tk.Label(alert_frame, text=message, font=("MS UI Gothic", 12), bg="#acd952")
    label.pack(pady=20)

    # Function to close the alert when the 'X' button is clicked
    def close_alert():
        alert_frame.destroy()

    # Add a close button ('X') to the top-right of the frame
    close_button = tk.Button(alert_frame, text="X", font=("Arial", 12, "bold"), bg="lightyellow", command=close_alert)
    close_button.place(x=250, y=8)

# navbar buttons
def nav_btn(text, fun):
                     tk.Button(nav_f,fg='white', bg='#1E1F22', text=text, font=("MS UI Gothic", 13), command=fun).pack(padx=0, pady=0, fill='x')

# info dsplay
# info display (scrollable)
def show_info(text):
    # Clear existing widgets
    for widget in main_f.winfo_children():
        widget.destroy()
    
    # Create a Frame to hold the Text widget and Scrollbar
    info_frame = tk.Frame(main_f, bg="#303236")
    info_frame.pack(expand=True, fill="both", padx=10, pady=10)
    tk.Label(info_frame, text="Unreturned Books", font=("Arial", 18), bg="#303236", fg="lightgreen").pack(pady=5)

    # Create a Scrollbar
    scrollbar = tk.Scrollbar(info_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Create a Text widget
    text_widget = tk.Text(info_frame,
                          wrap="word",
                          font=("Arial", 12),
                          bg="#303236",
                          fg="white",
                          yscrollcommand=scrollbar.set)
    text_widget.pack(expand=True, fill="both", side="left", padx=0,pady=0)

    # Configure the Scrollbar to scroll the Text widget
    scrollbar.config(command=text_widget.yview)

    # center aligned text
    text_widget.tag_configure("center", justify="center")


    # Insert the text into the Text widget
    text_widget.insert("1.0", text, "center")
    text_widget.config(state="disabled")  # Make the text widget read-only


# -----------------------------------------------------------------------------------------------

# submit button click commands
def issue_bk_cmd():
                     values = [x.get() for x in entry_widgets]
                     a = lib.issue_book(values[0].title(), values[1].title())
                     show_alert(a)

def return_bk_cmd():
                     values = [x.get() for x in entry_widgets]
                     a = lib.return_book(values[0].title(), values[1].title())
                     show_alert(a)

def add_bk_cmd():
                     values = [x.get() for x in entry_widgets]
                     a = lib.add_book(values[0].title(), values[1].title(), values[2].title(), float(values[3]), int(values[4]))
                     add_book_page()
                     show_alert(a)

def check_bk_cmd():
                     values = [x.get() for x in entry_widgets]
                     a = lib.b_availability(values[0].title())
                     if a is True:
                                          show_alert("Book is available")
                     else:
                                          show_alert("Book is not available")

def person_history_cmd():
                     values = [x.get() for x in entry_widgets]
                     his = lib.person_history(values[0])
                     show_info(his)

def book_history_cmd():
                     values = [x.get() for x in entry_widgets]
                     his = lib.book_history(values[0])
                     show_info(his)

def search_by_rating_cmd():
                     values = [x.get() for x in entry_widgets]
                     his = lib.search_by_rating(int(values[0]), int(values[1]))
                     show_info(his)

def search_by_genre_cmd():
                     values = [x.get() for x in entry_widgets]
                     his = lib.search_by_genre(values[0])
                     show_info(his)

def about_book_cmd():
                     values = [x.get() for x in entry_widgets]
                     his = lib.about_book(values[0])
                     show_info(his)

def change_quantity_cmd():
                     values = [x.get() for x in entry_widgets]
                     his = lib.change_book_quantity(values[0], int(values[1]))
                     show_alert(his)
                     
# ---------------------------------pages-------------------------------------------
def issue_book_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Book Name: ", main_f)
                     label_input("Borrower's Name:", main_f)
                     button_main("Issue book", issue_bk_cmd)
                     
def return_book_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Book Name: ", main_f)
                     label_input("Borrower's Name:", main_f)
                     button_main("Return book", fun=return_bk_cmd)

def add_book_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Book Name: ", main_f)
                     label_input("Author's Name:", main_f)
                     label_input("genre", main_f)
                     label_input("rating", main_f)
                     label_input("quantity", main_f)
                     button_main("Add book", add_bk_cmd)

def check_book_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Book Name: ", main_f)
                     button_main("Check book", fun=check_bk_cmd)

def person_history_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Name: ", main_f)
                     button_main("Check history", fun=person_history_cmd)

def all_available_book_list_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     show_info(lib.available_books())

def book_history_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Book Name: ", main_f)
                     button_main("Check history", fun=book_history_cmd)

def search_by_rating_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Start Range: ", main_f)
                     label_input("End Range: ", main_f)
                     button_main("Search by rating", fun=search_by_rating_cmd)

def search_by_genre_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Genre: ", main_f)
                     button_main("Search by genre", fun=search_by_genre_cmd)

def about_book_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Book name: ", main_f)
                     button_main("About book", fun=about_book_cmd)

def change_quantity_page():
                     for widget in main_f.winfo_children():
                                          widget.destroy()
                     global entry_widgets
                     entry_widgets = []
                     label_input("Book name: ", main_f)
                     label_input("New quantity: ", main_f)
                     button_main("Change quantity", fun=change_quantity_cmd)

def unret_books_page():
    for widget in main_f.winfo_children():
        widget.destroy()
    a = lib.unreturned_books()
    if a == "":
            show_info("There are no books to be returned!")
    else:
            show_info(a)
                    

# ---------------------------------navbars-----------------------------------------
def book_guide_nav():
                     for widget in nav_f.winfo_children():
                                          widget.destroy()
                     nav_btn("< Back", home_nav)
                     nav_btn(text="All available books", fun=all_available_book_list_page)
                     nav_btn(text="Book History", fun=book_history_page)
                     nav_btn(text="Search by rating", fun=search_by_rating_page)
                     nav_btn(text="Search by genre", fun=search_by_genre_page)
                     nav_btn(text="About Book", fun=about_book_page)
                     nav_btn(text="Change quantity", fun=change_quantity_page)

def home_nav():
                     for widget in nav_f.winfo_children():
                                          widget.destroy()
                     nav_btn("Issue book", issue_book_page)
                     nav_btn("Return book", return_book_page)
                     nav_btn(text="Add book", fun=add_book_page)
                     nav_btn(text="Check book", fun=check_book_page)
                     nav_btn(text="Person History", fun=person_history_page)
                     nav_btn(text="Book Guide", fun=book_guide_nav)
                     nav_btn(text="Unreturned books", fun=unret_books_page)
home_nav()

root.mainloop()
