import csv
from pprint import pprint
# for categories
with open('delivery_categories.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    date = []
    for row in spamreader:
        date.append(row)
    for cat in date[1:]:
        db.session.add(Category(title=cat[0][2:]))
    db.session.commit()
# for dishes. Or dishs?
with open('delivery_items.csv', newline='', encoding='utf-8') as csvfile:
    """
    class Dish(db.Model):
    __tablename__ = 'dishs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship('Category', back_populates='dishs')
    """
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar=' ')
    # i don't know
