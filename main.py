import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, create_tables
import json
from sqlalchemy import String, func


DSN = "postgresql://postgres:Kirushka1488@localhost:5432/ormsql"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()


with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


pub_name = input('Название издательства: ')


def get_shop_by_publisher():
    query = session.query(
        Book.title, 
        Shop.name, 
        func.cast(Sale.price, String), 
        func.to_char(Sale.date_sale, 'DD-MM-YYYY') 
        ).select_from(Shop).\
            join(Stock.shop).\
            join(Stock.book).\
            join(Book.publisher).\
            join(Sale) 
    if pub_name.isdigit(): 
        a = query.filter(Publisher.id == pub_name).all() 
        return print(a)
    else:
        b = query.filter(Publisher.name == pub_name).all() 
        return print(b)

if __name__ == '__main__':
    get_shop_by_publisher()
    

session.close()