import os
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Book, Shop, Stock, Sale

# Параметры подключения к БД (загружаем из переменных окружения)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'bookstore')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'anolanda')

# Строка подключения к PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_db_connection():
    """Создает подключение к базе данных"""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return engine, Session()

def find_publisher_sales(publisher_input):
    """
    Находит все продажи книг для указанного издателя
    publisher_input может быть именем или ID издателя
    """
    engine, session = create_db_connection()
    
    try:
        # Определяем, передан ID или имя издателя
        try:
            publisher_id = int(publisher_input)
            # Если удалось преобразовать в int, ищем по ID
            publisher_condition = Publisher.id == publisher_id
        except ValueError:
            # Если не удалось преобразовать, ищем по имени
            publisher_condition = Publisher.name.ilike(f'%{publisher_input}%')
        
        # Составляем запрос с JOIN для получения всех необходимых данных
        query = session.query(
            Book.title,
            Shop.name.label('shop_name'),
            Sale.price,
            Sale.date_sale,
            Sale.count
        ).select_from(Sale)\
         .join(Stock, Sale.id_stock == Stock.id)\
         .join(Book, Stock.id_book == Book.id)\
         .join(Publisher, Book.id_publisher == Publisher.id)\
         .join(Shop, Stock.id_shop == Shop.id)\
         .filter(publisher_condition)\
         .order_by(Sale.date_sale.desc())
        
        results = query.all()
        
        if not results:
            print(f"Не найдено продаж для издателя: {publisher_input}")
            return
        
        # Получаем имя издателя для отображения
        publisher = session.query(Publisher).filter(publisher_condition).first()
        if publisher:
            print(f"\nПродажи книг издателя: {publisher.name}")
            print("=" * 80)
            print(f"{'Название книги':<30} | {'Магазин':<15} | {'Цена':<8} | {'Дата':<12} | Кол-во")
            print("-" * 80)
            
            for result in results:
                date_formatted = result.date_sale.strftime('%d-%m-%Y')
                print(f"{result.title:<30} | {result.shop_name:<15} | {result.price:<8} | {date_formatted:<12} | {result.count}")
        
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
    finally:
        session.close()

def main():
    """Основная функция программы"""
    print("Поиск продаж книг по издателю")
    print("Введите имя или ID издателя:")
    
    publisher_input = input().strip()
    
    if not publisher_input:
        print("Пустой ввод. Программа завершена.")
        return
    
    find_publisher_sales(publisher_input)

if __name__ == "__main__":
    main()