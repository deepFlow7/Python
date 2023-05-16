from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, create_engine, Boolean, delete
from sqlalchemy.orm import relationship, sessionmaker, validates
import sys, getopt, datetime, time

Base = declarative_base()
engine = create_engine("sqlite:///books.db", echo=False)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session() 

class Book(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    is_borrowed = Column(Boolean, default=False)

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    @validates("year")
    def validate_year(self, key, value):
        assert value <= datetime.date.today().year
        return value

class Friend(Base):
    __tablename__ = "Friends"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(90), nullable=False)
    email = Column(String(70), nullable=False)

    def __init__(self, full_name, email):
        self.full_name = full_name
        self.email = email

    @validates("full_name")
    def validate_full_name(self, key, value):
        splited = value.split()
        for s in splited:
            assert s.isalpha()
        assert len(splited) > 1
        return value

    @validates("email")
    def validate_email(self, key, value):
        assert '@' in value
        return value

class Borrowing(Base):
    __tablename__ = "Borrowing"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('Books.id'))
    book = relationship("Book")
    who_id = Column(Integer, ForeignKey('Friends.id'))
    who = relationship("Friend")
    from_ = Column(DateTime,default=datetime.datetime.utcnow)

    def __init__(self, book_id, friend_id, date = None):
        self.book_id = book_id
        self.who_id = friend_id
        if date != None:
            self.date = date

    @validates("from")
    def validate_date(self, key, value):
        assert value <= datetime.date.today()
        return value

Base.metadata.create_all(engine)

def add_book(title, author, year):
    new_book = Book(title, author, year)
    session.add(new_book)
    session.commit()

def new_friend(full_name, email):
    friend = Friend(full_name, email)
    session.add(friend)
    session.commit()

def return_book(title):
    returning = session.query(Book).filter(Book.title == title, Book.is_borrowed == True).all()
    if len(returning) == 0:
        print ("There are no borrowed book with title '{0}'\n".format(title))
        return
    elif len(returning) == 1:
        id = returning[0].id
    else:
        print ("There are more than one book with title '{0}'. Which of them do you want to return? Type id!".format(title))
        for book in returning:
            friend = session.query(Borrowing).filter(Borrowing.book_id==book.id).first().who
            print ("id = {0}, borrowed by = {1} (id {2})".format(book.id, friend.full_name, friend.id))
        id = int(input())
    book = session.query(Book).get(id)
    book.is_borrowed = False
    session.delete(session.query(Borrowing).filter(Borrowing.book_id==id).first())
    session.commit()

def borrow_book(title, friend_full_name, date=None):
    friends = session.query(Friend).filter(Friend.full_name==friend_full_name).all()
    books = session.query(Book).filter(Book.title==title, Book.is_borrowed==False).all()

    if len(books) == 0:
        print ("There is no book to borrow\n")
        return
    elif len(books) == 1:
        book_id = books[0].id
    else:
        print ("There are more than one book with title '{0}'. Which of them do you want to lend? Type id!".format(title))
        for book in books:
            print ("id = {0}, {1} {2} {3}".format(book.id, book.title, book.author, book.year))
        book_id = int(input())

    if len(friends) == 0:
        print ("There is no friend {0}\n".format(friend_full_name))
        return
    elif len(friends) == 1:
        friend_id = friends[0].id
    else:
        print ("There are more than one '{0}'. Which of them do you want to lend the book to? Type id".format(friend_full_name))
        for friend in friends:
            print ("id = {0}, {1} {2} {3}".format(friend.id, friend.full_name, friend.email))
        friend_id = int(input())

    borrowing = Borrowing(book_id, friend_id, date)
    session.add(borrowing)
    borrowed_book = session.query(Book).get(book_id)
    borrowed_book.is_borrowed = True
    session.commit()

def print_books():
    books = session.query(Book).all()
    for book in books:
        print(book.id, " ", book.title, " ", book.author, " ", book.year, " [borrowed]" if book.is_borrowed == True else " [available]")

def print_friends():
    friends = session.query(Friend).all()
    for friend in friends:
        print(friend.id, " ", friend.full_name, " ", friend.email)

def print_borrowing():
    borrowing = session.query(Borrowing).all()
    for b in borrowing:
        print(b.id, " ", session.query(Book).get(b.book_id).title, " ", session.query(Friend).get(b.who_id).full_name)

def date_from_string(my_str):
    date_tup = (int(my_str[:4]),int(my_str[5:7]),int(my_str[8:10]))
    return datetime.date(*date_tup)

 
opts, args = getopt.getopt(sys.argv[1:], "abrh:", 
                            ["add", "title=", "author=", "year=", 
                            "borrow", "friend", "full_name=", "date=",
                            "return", "book_id=", "email=", "help"])


mode = ""
author =  title = year = full_name = email = date = None 

for i in range (0, len(opts)):
    opt, arg = opts[i]
    if opt in ['-h', '--help']:
        print("Possible programm arguments :")
        print("   --borrow --title ['title'] --full_name ['full_name']  --date [date] (optional) # date format yyyy-mm-dd")
        print("   --return --title ['title']")
        print("   --add --title ['title'] --author ['author'] --year [year]")
        print("   --friend --full_name [full_name] --email [email]")
        mode = ""
    elif opt in ['-a', '--add']:
        mode = "add"
    elif opt in ['-b', '--borrow']:
        mode = "borrow"
    elif opt in ['-r', '--return']:
        mode = "return" 
    elif opt == "--author" and mode == "add":
        author = arg
    elif opt == "--title" and mode in ["borrow", "return", "add"]:
        title = arg
        if mode == "return":
            return_book(title)
    elif opt == "--year" and mode == "add":
        year = arg
        add_book(title, author, int(year))
    elif opt == "--full_name" and mode in ["add", "friend", "borrow"]:
        full_name = arg
        if mode == "borrow" and (i == len(opts) - 1 or opts[i + 1][0] != "--date"):
            borrow_book(title, full_name)
            print ("borrrrrr")
    elif opt == "--date" and mode == "borrow":
        date = arg
        borrow_book(title, full_name, date_from_string(date))
    elif opt == "--friend": 
        mode = "friend"
    elif opt == "--email" and mode == "friend": 
        email = arg
        new_friend(full_name, email)

print ("Books :")
print_books()
print ("\nFriends :")
print_friends()
print ("\nBorrowed books :")
print_borrowing()
print('')

session.close()

# przykładowe argumenty wywołania programu

# --friend --full_name 'Jan Kowalski' --email kowalski@gmail.com
# --friend --full_name 'Aleksandra Kwarc' --email alexis@gmail.com
# --add --title 'Alicja w krainie czarow' --author 'Lewis Carroll' --year 1865
# --add --title 'Nie mow nikomu' --author 'Harlan Coben' --year 2001
# --add --title 'Nie mow nikomu' --author 'Karolina Wojciak' --year 2022
# --borrow --title 'Alicja w krainie czarow' --full_name 'Jan Kowalski' --date 2022-12-31
# --borrow --title 'Nie mow nikomu' --full_name 'Jan Kowalski' 
# --return --title 'Alicja w krainie czarow'