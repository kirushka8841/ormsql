import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale



DSN = "postgresql://postgres:Kirushka1488@localhost:5432/ormsql"
engine = sqlalchemy.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()
create_tables(engine)

session.commit()

publisher_name = input('Введите имя издателя или id: ')
if publisher_name.isnumeric():
    for c in session.query(Publisher).filter(
            Publisher.id == int(publisher_name)).all():
        print(c)
else:
    for c in session.query(Publisher).filter(
            Publisher.name.like(f'%{publisher_name}%')).all():
        print(c)

session.close()