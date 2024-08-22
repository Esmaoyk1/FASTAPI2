from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"  #hangi veritabnına baglancagını belirttik

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}   # birden fazla iş parçacığının aynı veritabanı bağlantısını paylaşması gerekiyorsa, check_same_thread parametresini False yaparak bu kısıtlamayı kaldırabiliriz.
)


SessionLocal = sessionmaker(autocommit = False,autoflush =False , bind = engine)

Base =declarative_base()  #Bu temel sınıf, veritabanı tablolarınızı temsil eden model sınıflarını tanımlamanıza yardımcı olur.
