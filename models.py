from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    
    # Связь с книгами (один ко многим)
    books = relationship("Book", back_populates="publisher")
    
    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"

class Book(Base):
    __tablename__ = 'book'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)
    
    # Связи
    publisher = relationship("Publisher", back_populates="books")
    stock_entries = relationship("Stock", back_populates="book")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', publisher_id={self.id_publisher})>"

class Shop(Base):
    __tablename__ = 'shop'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    
    # Связь со складскими записями
    stock_entries = relationship("Stock", back_populates="shop")
    
    def __repr__(self):
        return f"<Shop(id={self.id}, name='{self.name}')>"

class Stock(Base):
    __tablename__ = 'stock'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False, default=0)
    
    # Связи
    book = relationship("Book", back_populates="stock_entries")
    shop = relationship("Shop", back_populates="stock_entries")
    sales = relationship("Sale", back_populates="stock")
    
    def __repr__(self):
        return f"<Stock(id={self.id}, book_id={self.id_book}, shop_id={self.id_shop}, count={self.count})>"

class Sale(Base):
    __tablename__ = 'sale'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Numeric(10, 2), nullable=False)
    date_sale = Column(DateTime, nullable=False, default=datetime.utcnow)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False, default=1)
    
    # Связь со складской записью
    stock = relationship("Stock", back_populates="sales")
    
    def __repr__(self):
        return f"<Sale(id={self.id}, price={self.price}, date={self.date_sale}, stock_id={self.id_stock})>"