from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, entity_id):
        self._id = entity_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @abstractmethod
    def get_info(self):
        pass


class Book(Entity):
    def __init__(self, book_id, title, author, year, genre):
        super().__init__(book_id)
        self._title = title
        self._author = author
        self._year = year
        self._genre = genre
        self._read = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def read(self):
        return self._read

    @read.setter
    def read(self, value):
        self._read = value

    def get_info(self):
        return f"{self._title} - {self._author}"

    def __str__(self):
        return self._title

    def __repr__(self):
        return f"Book({self._id}, {self._title!r})"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self._id == other._id

    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self._year < other._year


class User(Entity):
    def __init__(self, user_id, name):
        super().__init__(user_id)
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def get_info(self):
        return f"Пользователь: {self._name}"

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"User({self._id}, {self._name!r})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self._id == other._id

    def __lt__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self._name < other._name


class BookManager:
    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def remove_book(self, book):
        if book in self._books:
            self._books.remove(book)

    def get_books(self):
        return self._books

    def count(self):
        return len(self._books)

    def sort_books(self):
        self._books.sort()