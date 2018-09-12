class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("This user's email has been updated to {address}.".format(address = self.email))

    def __repr__(self):
        return ("User {name}, email: {email}, books read: {books_read}".format(name = self.name, email = self.email, books_read = len(self.books)))

    def __eq__(self, other):
        return other.name == self.name and other.email == self.email

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total_rating = 0

        for rating in self.books.values():
            if rating is not None:
                total_rating+=rating

        return total_rating/len(self.books)


class Book(object):

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("This book's ISBN has been updated to {isbn}.".format(isbn = self.isbn))

    def add_rating(self, rating):
        if rating in range(0,5):
            self.ratings.append(rating)
        else:
            print("Invalid Rating: {rating}".format(rating = rating))

    def __eq__(self, other):
        return other.title == self.title and other.isbn == self.isbn

    def get_average_rating(self):
        total_rating = 0
        for rating in self.ratings:
            total_rating+=rating

        return total_rating/len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return ("""
        Users: {users}\n
        Books: {books}""".format(users = self.users, books = self.books))

    def __eq__(self, other):
        return other.users == self.users and other.books == self.books

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email)

        if user:
            user.read_book(book, rating)
            if rating is not None:
                book.add_rating(rating)
            if self.books.get(book):
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("ERROR: No user with email {email}!".format(email = email))

    def add_user(self, name, email, books=None):
        if email in self.users:
            print("ERROR: User with email {email} already exists.".format(email = email))
        else:
            self.users[email] = User(name, email)

            if books is not None:
                for book in books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for key in self.books:
            print(key)

    def print_users(self):
        for value in self.users.values():
            if value is not None:
                print(value)

    def most_read_book(self):
        most_read_book = ""
        book_count = 0

        for key,value in self.books.items():
            if value > book_count:
                most_read_book = key
                book_count = value
        return most_read_book

    def highest_rated_book(self):
        highest_rated_book = ""
        rating = 0

        for key in self.books:
            book_rating = key.get_average_rating()
            if book_rating > rating:
                highest_rated_book = key
                rating = book_rating
        return highest_rated_book

    def most_positive_user(self):
        most_positive_user = ""
        rating = 0

        for key in self.users:
            user_rating = self.users[key].get_average_rating()
            if user_rating > rating:
                most_positive_user = self.users[key]
                rating = user_rating
        return most_positive_user
