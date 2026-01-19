import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Book, Shop, Stock, Sale

# Параметры подключения к БД
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'bookstore')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'anolanda')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def setup_database():
    """Создает таблицы и заполняет их тестовыми данными"""
    
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Создаем все таблицы
        Base.metadata.create_all(engine)
        print("Таблицы созданы успешно!")
        
        # Проверяем, есть ли уже данные
        if session.query(Publisher).count() > 0:
            print("База данных уже содержит данные. Пропускаем заполнение.")
            return
        
        # Создаем издателей
        publishers = [
            Publisher(name="Пушкин"),
            Publisher(name="Толстой"),
            Publisher(name="Достоевский"),
            Publisher(name="Чехов")
        ]
        
        for publisher in publishers:
            session.add(publisher)
        session.commit()
        
        # Создаем магазины
        shops = [
            Shop(name="Буквоед"),
            Shop(name="Лабиринт"),
            Shop(name="Книжный дом"),
            Shop(name="Читай-город")
        ]
        
        for shop in shops:
            session.add(shop)
        session.commit()
        
        # Создаем книги
        books_data = [
            ("Капитанская дочка", 1),
            ("Руслан и Людмила", 1),
            ("Евгений Онегин", 1),
            ("Война и мир", 2),
            ("Анна Каренина", 2),
            ("Преступление и наказание", 3),
            ("Братья Карамазовы", 3),
            ("Вишневый сад", 4),
            ("Чайка", 4)
        ]
        
        books = []
        for title, publisher_id in books_data:
            book = Book(title=title, id_publisher=publisher_id)
            books.append(book)
            session.add(book)
        session.commit()
        
        # Создаем складские записи (книги в магазинах)
        stock_entries = []
        for book in books:
            for shop in shops:
                stock = Stock(id_book=book.id, id_shop=shop.id, count=10)
                stock_entries.append(stock)
                session.add(stock)
        session.commit()
        
        # Создаем продажи (примеры как в задании)
        sales_data = [
            # Продажи книг Пушкина
            (1, 1, 600, datetime(2022, 11, 9)),   # Капитанская дочка в Буквоеде
            (2, 1, 500, datetime(2022, 11, 8)),   # Руслан и Людмила в Буквоеде
            (1, 2, 580, datetime(2022, 11, 5)),   # Капитанская дочка в Лабиринте
            (3, 3, 490, datetime(2022, 11, 2)),   # Евгений Онегин в Книжном доме
            (1, 1, 600, datetime(2022, 10, 26)),  # Капитанская дочка в Буквоеде
            # Дополнительные продажи других авторов
            (4, 2, 800, datetime(2022, 11, 10)),  # Война и мир в Лабиринте
            (5, 1, 750, datetime(2022, 11, 7)),   # Анна Каренина в Буквоеде
            (6, 4, 650, datetime(2022, 11, 3)),   # Преступление и наказание в Читай-городе
        ]
        
        for book_id, shop_id, price, date in sales_data:
            # Находим соответствующую складскую запись
            stock = session.query(Stock).filter(
                Stock.id_book == book_id,
                Stock.id_shop == shop_id
            ).first()
            
            if stock:
                sale = Sale(
                    price=price,
                    date_sale=date,
                    id_stock=stock.id,
                    count=1
                )
                session.add(sale)
        
        session.commit()
        print("Тестовые данные добавлены успешно!")
        
        # Выводим информацию о созданных данных
        publishers_count = session.query(Publisher).count()
        books_count = session.query(Book).count()
        shops_count = session.query(Shop).count()
        sales_count = session.query(Sale).count()
        
        print(f"\nСтатистика:")
        print(f"Издателей: {publishers_count}")
        print(f"Книг: {books_count}")
        print(f"Магазинов: {shops_count}")
        print(f"Продаж: {sales_count}")
        
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    setup_database()