from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the extension
db = SQLAlchemy()
# Create a Flask Instance 
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# initialize the app with the extension
db.init_app(app)
# Secret Key!
app.config['SECRET_KEY'] = "secretkey123"

# Create a Model
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    price = db.Column(db.String(10))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# All models go above this
with app.app_context():
    db.create_all()
    
class UserForm(FlaskForm):
    name = StringField("Name?", validators=[DataRequired()])
    email = StringField("Email?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a form class
class ProductForm(FlaskForm):
    name = StringField("What's the Product Name?", validators=[DataRequired()])
    price = StringField("How much does this cost?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a form class
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name = name)

@app.route("/buttons")
def buttons():
    return render_template("components/buttons.html")

@app.route("/cards")
def cards():
    return render_template("components/cards.html")

@app.route("/utilitiesColor")
def utilitiesColor():
     return render_template("utilities/utilitiesColor.html")

@app.route("/utilitiesBorder")
def utilitiesBorder():
    return render_template("utilities/utilities-border.html")

@app.route("/utilitiesAnimation")
def utilitiesAnimation():
    return render_template("utilities/utilities-animation.html")

@app.route("/utilitiesOther")
def utilitiesOther():
    return render_template("utilities/utilities-other.html")

@app.route("/charts")
def charts():
    return render_template("charts.html")

@app.route("/tables")
def tables():
    return render_template("tables.html")

@app.route("/login")
def login():
    return render_template("pages/login.html")

@app.route("/register")
def register():
    return render_template("pages/register.html")

@app.route("/forgotPassword")
def forgotPassword():
    return render_template("pages/forgotPassword.html")

@app.route("/error")
def error():
    return render_template("pages/error.html")

@app.route("/blank")
def blank():
    return render_template("pages/blank.html")

@app.route('/products/add', methods=['GET', 'POST'])
def AddProduct():
    name = None
    price = None
    form = ProductForm()
    if form.validate_on_submit():
        if db.session.query(Products).filter_by(name=name).count:
            product = Products(name=form.name.data, price=form.price.data)         
            db.session.add(product)
            db.session.commit()
        name = form.name.data
        price = form.price.data
        form.name.data = ''
        form.price.data = ''
        flash("Product Added")
    our_products = Products.query.order_by(Products.date_added)
    return render_template("test/add_product.html", form = form, name=name,our_products=our_products)

@app.route('/user/add', methods=['GET', 'POST'])
def AddUser(): 
    name = None
    form = UserForm()
    if form.validate_on_submit():
        if db.session.query(Users).filter_by(name=name).count:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("test/add_user.html", name=name, form=form, our_users=our_users)

@app.route("/name", methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted")
    return render_template("test/name.html", name=name, form=form)

if __name__ == ("__main__"):
    app.run(debug=True)