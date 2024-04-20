import pytest
from main import BooksCollector
# Класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:
    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    def test_init(self):
        collector = BooksCollector()
        assert collector.books_genre == {}
        assert collector.favorites == []
        assert set(collector.genre) == {'Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'}
        assert set(collector.genre_age_rating) == {'Ужасы', 'Детективы'}

    @pytest.mark.parametrize("book_name", [
        "Убийство в восточном экспрессе",
        "Унесённые ветром",
        "Урфин Джюс и его деревянные солдаты",
        "Утомлённые солнцем",
        "Утопия"
    ])
    def test_add_new_book_valid(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()
        assert collector.get_books_genre().get(book_name) == ''

    @pytest.mark.parametrize("invalid_book_name", [
        "",  # Пустая строка
        "А" * 41,  # Слишком длинное название
    ])
    def test_add_new_book_invalid_name(self, invalid_book_name):
        collector = BooksCollector()
        collector.add_new_book(invalid_book_name)
        assert invalid_book_name not in collector.get_books_genre()

    @pytest.mark.parametrize("book_name, genre", [
        ("Убийство в восточном экспрессе", "Детективы"),
        ("Утопия", "Фантастика"),
        ("Урфин Джюс и его деревянные солдаты", "Фэнтези"),  # Недопустимый жанр
    ])
    def test_set_book_genre_valid(self, book_name, genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        expected_genre = genre if genre in ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'] else ''
        assert collector.get_book_genre(book_name) == expected_genre

    @pytest.mark.parametrize("invalid_book_name, invalid_genre", [
        ("Убийство в восточном экспрессе", "Драма")
    ])
    def test_set_book_genre_invalid(self, invalid_book_name, invalid_genre):
        collector = BooksCollector()
        collector.add_new_book(invalid_book_name)
        collector.set_book_genre(invalid_book_name, invalid_genre)
        assert collector.get_book_genre(invalid_book_name) == ''

    @pytest.mark.parametrize("book_title, genre", [
        ("Урфин Джюс и его деревянные солдаты", "Мультфильмы"),
        ("Утомлённые солнцем", "Ужасы")
    ])
    def test_get_books_for_children(self, book_title, genre):
        collector = BooksCollector()
        collector.add_new_book(book_title)
        collector.set_book_genre(book_title, genre)
        assert (book_title in collector.get_books_for_children()) == (genre not in collector.genre_age_rating)

    @pytest.mark.parametrize("books_genre", [
        {},
        {"Утопия": "Фантастика", "Убийство в Восточном экспрессе": "Детективы"},
        {"Урфин Джюс и его деревянные солдаты": "Мультфильмы"},
    ])
    def test_get_books_genre(self, books_genre):
        collector = BooksCollector()
        collector.books_genre = books_genre
        assert collector.get_books_genre() == books_genre

    @pytest.mark.parametrize("books_genre, genre, expected_books", [
        ({"Утопия": "Фантастика", "Убийство в Восточном экспрессе": "Детективы"}, "Фантастика",
         ["Утопия"]),
        ({"Урфин Джюс и его деревянные солдаты": "Мультфильмы", "Утомлённые солнцем": "Ужасы"}, "Мультфильмы",
         ["Урфин Джюс и его деревянные солдаты"]),
        ({"Урфин Джюс и его деревянные солдаты": "Мультфильмы", "Утомлённые солнцем": "Ужасы"}, "Комедии", [])
    ])
    def test_get_books_with_specific_genre(self, books_genre, genre, expected_books):
        collector = BooksCollector()
        collector.books_genre = books_genre
        assert collector.get_books_with_specific_genre(genre) == expected_books

    @pytest.mark.parametrize("book_title", [
        "Унесённые ветром",
        "Урфин Джюс и его деревянные солдаты"
    ])
    def test_add_book_in_favorites(self, book_title):
        collector = BooksCollector()
        collector.add_new_book(book_title)
        collector.add_book_in_favorites(book_title)
        assert book_title in collector.get_list_of_favorites_books()

    @pytest.mark.parametrize("book_title", [
        "Унесённые ветром",
        "Урфин Джюс и его деревянные солдаты"
    ])
    def test_delete_book_from_favorites(self, book_title):
        collector = BooksCollector()
        collector.add_new_book(book_title)
        collector.add_book_in_favorites(book_title)
        collector.delete_book_from_favorites(book_title)
        assert book_title not in collector.get_list_of_favorites_books()

    @pytest.mark.parametrize("favorites", [
        [],
        ["Утомленные солнцем", "Утопия"],
        ["Урфин Джюс и его деревянные солдаты"],
    ])
    def test_get_list_of_favorites_books(self, favorites):
        collector = BooksCollector()
        collector.favorites = favorites
        assert collector.get_list_of_favorites_books() == favorites
