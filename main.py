from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import flet as ft

from classes import Book, BookManager, User


# ---------- Пользовательские компоненты ----------

class AppText(ft.Text):
    def __init__(self, text, size=16):
        super().__init__(
            value=text,
            size=size,
        )


class AppButton(ft.Button):
    def __init__(self, text, on_click):
        super().__init__(
            content=text,
            on_click=on_click,
        )


class BookCard(ft.Container):
    def __init__(self, book, delete_book):
        self.book = book
        self.delete_book = delete_book

        self.check = ft.Checkbox(
            label=f"{book.title} — {book.author}",
            value=book.read,
            on_change=self.change_read,
        )

        self.info = ft.Text(
            f"{book.genre}, {book.year}",
            size=13,
        )

        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            on_click=self.remove,
        )

        super().__init__(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            self.check,
                            self.info,
                        ],
                        spacing=2,
                    ),
                    self.delete_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
            width=650,
        )

    def change_read(self, e):
        self.book.read = e.control.value

    def remove(self, e):
        self.delete_book(self.book)


# ---------- Основное приложение ----------

class BookApp:
    def __init__(self, page):
        self.page = page
        self.manager = BookManager()

        # Пользователь
        self.user = User(1, "student")
        self.login = self.user.name

        # Время работы
        self.time_in = datetime.now()
        self.time_out = None

        # Файл отчета находится именно в папке проекта
        self.report_path = Path(__file__).resolve().parent / "report.txt"

        # Создаем отчет сразу при запуске
        self.save_report()

        # ---------- Поля ввода ----------

        self.title_input = ft.TextField(
            label="Название",
            width=230,
        )

        self.author_input = ft.TextField(
            label="Автор",
            width=230,
        )

        self.year_input = ft.TextField(
            label="Год",
            width=120,
        )

        self.genre_input = ft.Dropdown(
            label="Жанр",
            width=180,
            options=[
                ft.DropdownOption(
                    key="Роман",
                    text="Роман",
                ),
                ft.DropdownOption(
                    key="Фантастика",
                    text="Фантастика",
                ),
                ft.DropdownOption(
                    key="Детектив",
                    text="Детектив",
                ),
                ft.DropdownOption(
                    key="Учебная",
                    text="Учебная",
                ),
            ],
        )

        # ---------- Список книг ----------

        self.counter = ft.Text(
            "Всего книг: 0"
        )

        self.books_list = ft.Column(
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # ---------- Кнопки ----------

        self.add_button = AppButton(
            "Добавить",
            self.add_book,
        )

        self.sort_button = AppButton(
            "Сортировать по году",
            self.sort_books,
        )

        self.clear_button = AppButton(
            "Очистить",
            self.clear_inputs,
        )

        self.exit_button = AppButton(
            "Выйти и сохранить",
            self.exit_app,
        )

        # Создаем 5 объектов Book
        self.create_books()

        # Создаем интерфейс
        self.setup_page()

        # Обработка закрытия окна
        self.page.window.on_event = self.window_event

    # ---------- Создание объектов ----------

    def create_books(self):
        books = [
            Book(
                1,
                "Преступление и наказание",
                "Ф. Достоевский",
                1866,
                "Роман",
            ),
            Book(
                2,
                "1984",
                "Дж. Оруэлл",
                1949,
                "Фантастика",
            ),
            Book(
                3,
                "Шерлок Холмс",
                "А. Дойл",
                1887,
                "Детектив",
            ),
            Book(
                4,
                "Python для начинающих",
                "А. Автор",
                2024,
                "Учебная",
            ),
            Book(
                5,
                "Мастер и Маргарита",
                "М. Булгаков",
                1967,
                "Роман",
            ),
        ]

        for book in books:
            self.manager.add_book(book)

    # ---------- Интерфейс ----------

    def setup_page(self):
        self.page.title = "Book Manager"

        self.page.window.width = 900
        self.page.window.height = 700

        self.page.add(
            ft.Column(
                [
                    AppText(
                        "Мои книги",
                        32,
                    ),

                    AppText(
                        "Небольшое приложение для учета книг",
                        16,
                    ),

                    ft.Divider(),

                    ft.Row(
                        [
                            self.title_input,
                            self.author_input,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Row(
                        [
                            self.year_input,
                            self.genre_input,
                            self.add_button,
                            self.clear_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Divider(),

                    ft.Row(
                        [
                            self.counter,
                            self.sort_button,
                            self.exit_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        width=650,
                    ),

                    ft.Divider(),

                    self.books_list,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

        self.update_list()

    # ---------- Работа со списком ----------

    def update_list(self):
        self.books_list.controls.clear()

        for book in self.manager.get_books():
            self.books_list.controls.append(
                BookCard(
                    book,
                    self.delete_book,
                )
            )

        self.counter.value = (
            f"Всего книг: {self.manager.count()}"
        )

        self.page.update()

    def add_book(self, e):
        if not self.title_input.value:
            return

        if not self.author_input.value:
            return

        try:
            year = int(self.year_input.value)
        except (ValueError, TypeError):
            year = 0

        book = Book(
            self.manager.count() + 1,
            self.title_input.value,
            self.author_input.value,
            year,
            self.genre_input.value or "Другое",
        )

        self.manager.add_book(book)

        self.clear_inputs(None)
        self.update_list()

    def delete_book(self, book):
        self.manager.remove_book(book)
        self.update_list()

    def clear_inputs(self, e):
        self.title_input.value = ""
        self.author_input.value = ""
        self.year_input.value = ""
        self.genre_input.value = None

        self.page.update()

    def sort_books(self, e):
        self.manager.sort_books()
        self.update_list()

    # ---------- Отчет ----------

    def save_report(self):
        if self.time_out is None:
            time_out = "в работе"
        else:
            time_out = self.time_out.strftime(
                "%d.%m.%Y %H:%M:%S"
            )

        with open(
            self.report_path,
            "w",
            encoding="utf-8",
        ) as file:
            file.write("login\n")
            file.write("time in\n")
            file.write("time out\n")
            file.write(
                f"{self.login} "
                f"{self.time_in.strftime('%d.%m.%Y %H:%M:%S')} | "
                f"{time_out}\n"
            )

    # ---------- Закрытие ----------

    async def exit_app(self, e):
        self.time_out = datetime.now()

        self.save_report()

        await self.page.window.destroy()

    def window_event(self, e):
        if e.type == ft.WindowEventType.CLOSE:
            self.time_out = datetime.now()
            self.save_report()


# ---------- Запуск ----------

def main(page):
    BookApp(page)


ft.run(main)