import csv
from app import db, Dish
with open('delivery_categories.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    date = []
    for row in spamreader:
        date.append(row)
    for cat in date[1:]:
        db.session.add(Category(title=cat[0][2:]))
    db.session.commit()
with open('delivery_items.csv', encoding='utf-8') as csvfile:
    delivery_items = csv.DictReader(csvfile)
    for delivery_item in delivery_items:
        db.session.add(Dish(**delivery_item))
db.session.commit()
