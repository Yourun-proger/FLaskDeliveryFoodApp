import datetime

from flask import Flask, render_template, redirect, session, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from forms import UserForm, AuthForm, CartForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '42'  # заставляет задуматься...
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', back_populates='user')

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Dish(db.Model):
    __tablename__ = 'dishs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship('Category', back_populates='dishs')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    dishs = db.relationship('Dish', back_populates='category')


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    summ = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    dishs = db.Column(db.String, nullable=False)
    user_mail = db.Column(db.String, db.ForeignKey("users.mail"))
    user = db.relationship("User", back_populates="orders")


db.create_all()
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))


@app.route('/')
def main():
    dish_list = [db.session.query(Dish).get(i) for i in session.get('cart', [])]
    summ = 0
    for dish in dish_list:
        summ += dish.price
    return render_template('main.html',
                           categories=db.session.query(Category).all(),
                           is_auth=session.get('is_auth', False),
                           summ=summ,
                           len=len(dish_list)
                           )


@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    is_del = False
    if session.get('delete'):
        is_del = True
        session['delete'] = False
    form = CartForm()
    dish_list = [db.session.query(Dish).get(i) for i in session.get('cart', [])]
    summ = 0
    for dish in dish_list:
        summ += dish.price
    if request.method == 'POST':
        name = form.name.data
        address = form.address.data
        user_mail = form.user_mail.data
        phone = form.phone.data
        date = datetime.date.today().strftime("%d.%m.%Y")
        status = "Выполняется"
        order_form = Order(name=name,
                           address=address,
                           phone=phone,
                           date=date,
                           summ=summ,
                           status=status,
                           dishs=",".join(str(dish.id) for dish in dish_list),
                           user_mail=user_mail
                           )
        db.session.add(order_form)
        db.session.commit()
        session['cart'] = []
        return redirect('/ordered/')
    else:
        return render_template('cart.html',
                               cart=session.get('cart', []),
                               dish_list=dish_list,
                               len=len(dish_list),
                               summ=summ,
                               delete=is_del,
                               is_auth=session.get('is_auth', False),
                               form=form
                               )


@app.route('/account/')
def account():
    if session.get('is_auth', False):
        user = db.session.query(User).get(session['user_id'])
        orders = user.orders
        return render_template('account.html', orders=orders, db=db, Dish=Dish)
    return redirect('/auth/')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        mail = form.mail.data
        password_hash = form.password.data
        user = User(mail=mail, password_hash=generate_password_hash(password_hash))
        db.session.add(user)
        db.session.commit()
        session['is_auth'] = True
        session['user_id'] = user.id
        return redirect('/account/')
    return render_template('registration.html', form=form)


@app.route('/auth/', methods=['GET', 'POST'])
def login():
    if session.get("user_id"):
        return redirect("/account/")
    else:
        form = AuthForm()
        if request.method == "POST":
            user = db.session.query(User).filter(User.mail == form.mail.data).first()
            if user.mail and user.password_valid(form.password.data):
                session["user_id"] = user.id
                session["is_auth"] = True
                return redirect("/account/")
        return render_template("auth.html", form=form)


@app.route('/logout/')
def logout():
    if session.get('user_id'):
        session.pop('user_id')
    return redirect('/auth/')


@app.route('/ordered/')
def ordered():
    return render_template('ordered.html')


@app.route('/addtocart/<int:dish_id>/')
def addtocart(dish_id):
    cart = session.get('cart', [])
    cart.append(dish_id)
    session['cart'] = cart
    return redirect('/cart/')


@app.route('/deletetocart/<int:dish_id>/')
def deletetocart(dish_id):
    cart = session.get('cart', [])
    cart.remove(dish_id)
    session['cart'] = cart
    session['delete'] = True
    return redirect('/cart/')




if __name__ == '__main__':
    app.run()
