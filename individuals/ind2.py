#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Дополнительно к требуемым в заданиях операциям перегрузить операцию индексирования [].
#Максимально возможный размер списка задать константой. В отдельном поле size должно
#храниться максимальное для данного объекта количество элементов списка; реализовать метод
#size(), возвращающий установленную длину. Если количество элементов списка изменяется во
#время работы, определить в классе поле count. Первоначальные значения size и count
#устанавливаются конструктором.

#Информационная запись о книге в библиотеке содержит следующие поля: автор, название,
#год издания, издательство, цена. Для моделирования учетной карточки абонента
#реализовать класс Subscriber, содержащий фамилию абонента, его библиотечный номер и
#список взятых в библиотеке книг. Один элемент списка состоит из информационной записи о
#книге, даты выдачи, требуемой даты возврата и признака возврата. Реализовать методы
#добавления книг в список и удаления книг из него; метод поиска книг, подлежащих возврату;
#методы поиска по автору, издательству и году издания; метод вычисления стоимости всех
#подлежащих возврату книг. Реализовать операцию слияния двух учетных карточек,
#операцию пересечения и вычисления разности. Реализовать операцию генерации
#конкретного объекта Debt (долг), содержащего список книг, подлежащих возврату из объекта
#типа Subscriber.

class Book:
    def __init__(self, author, title, year, publisher, price):
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher
        self.price = price

    def __repr__(self):
        return f"Book('{self.author}', '{self.title}', {self.year}, '{self.publisher}', {self.price})"


class Subscriber:
    MAX_BOOKS = 100

    def __init__(self, surname, id, books=[], size=MAX_BOOKS):
        if len(books) > size:
            raise ValueError("Amount of books > max size")
        self.surname = surname
        self.id = id
        self.books = books
        self.__size = size
        self.__count = len(books)

    @property
    def size(self):
        return self.__size

    @property
    def count(self):
        return self.__count

    def add_book(self, book, issue_date, return_date):
        if self.__count < self.__size:
            self.books.append(
                {
                    "book": book,
                    "issue_date": issue_date,
                    "return_date": return_date,
                    "returned": False,
                }
            )
            self.__count += 1
        else:
            print("Reached maximum size")

    def remove_book(self, book):
        for item in self.books:
            if item.book == book:
                self.books.remove(item)
                self.__count -= 1
                return

    def books_to_return(self):
        return [i for i in self.books if not i["returned"]]

    def find_by_author(self, author):
        return [i for i in self.books if i["book"].author == author]

    def find_by_publihser(self, publisher):
        return [i for i in self.books if i["book"].publisher == publisher]

    def find_by_year(self, year):
        return [i for i in self.books if i["book"].year == year]

    def price_books_to_return(self):
        return sum([i["book"].price for i in self.books if not i["returned"]])

    def generate_debt(self):
        return Debt([i for i in self.books if not i["returned"]])

    def __getitem__(self, index):
        if isinstance(index, int) and 0 <= index < self.count:
            return self.books[index]
        else:
            raise IndexError("Index out of range")

    def __add__(self, other):
        if not isinstance(other, Subscriber):
            raise ValueError("Object must be an instance of Subscriber")
        result = self.books + other.books
        return Subscriber(
            f"{self.surname} & {other.surname}",
            f"{self.id} & {other.id}",
            result,
        )

    def __and__(self, other):
        result = [book for book in self.books if book in other.books]
        return Subscriber(
            f"{self.surname} & {other.surname}",
            f"{self.id} & {other.id}",
            result,
        )

    def __sub__(self, other):
        result = [book for book in self.books if book not in other.books]
        return Subscriber(
            f"{self.surname} & {other.surname}",
            f"{self.id} & {other.id}",
            result,
        )

    def __repr__(self):
        return f"Subscriber({self.surname}, {self.id}, {self.books})"


class Debt:
    def __init__(self, books):
        self.books = books

    def __repr__(self):
        return f"Debt({self.books})"


if __name__ == "__main__":
    subscriber1 = Subscriber("Ascorbin", "12345")
    subscriber2 = Subscriber("Lofanbl4", "54321")

    book1 = Book("Author1", "Book1", 2020, "Publisher1", 10.99)
    book2 = Book("Author2", "Book2", 2019, "Publisher2", 9.99)

    subscriber1.add_book(book1, "2024-01-01", "2024-01-31")
    subscriber1.add_book(book2, "2024-02-01", "2024-02-28")
    subscriber2.add_book(book2, "2024-02-01", "2024-02-28")

    print("Books to return:")
    print(subscriber1.books_to_return(), "\n")
    print("Books by author: ")
    print(subscriber1.find_by_author("Author1"), "\n")
    print("Books by publisher: ")
    print(subscriber1.find_by_publihser("Publisher1"), "\n")
    print("Price of not returned books: ")
    print(subscriber1.price_books_to_return(), "\n")

    merged_subscribers = subscriber1 + subscriber2
    print("Merge: ")
    print(merged_subscribers, "\n")
    intersection = subscriber1 & subscriber2
    print("Intersection: ", "\n")
    print(intersection)
    difference = subscriber1 - subscriber2
    print("Difference: ")
    print(difference, "\n")
    debt1 = subscriber1.generate_debt()
    print("Object Debt: ")
    print(debt1.books)
