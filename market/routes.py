from flask import render_template, redirect, url_for, flash, request
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == "POST":
        purchased_item_name = request.form.get("purchased_item")
        purchased_item_object = Item.query.filter_by(name=purchased_item_name).first()
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                flash(
                    f"Congratulation, you purchased { purchased_item_object.name } for { purchased_item_object.prettier_price }",
                    category="success",
                )
            else:
                flash(
                    f"Sorry, your budget is not enought to purchase { purchased_item_object.name } at { purchased_item_object.prettier_price }",
                    category="danger",
                )

        return redirect(url_for("market_page"))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        return render_template(
            "market.html", items=items, purchase_form=purchase_form, sell_form=sell_form
        )


@app.route("/your-products", methods=["GET", "POST"])
@login_required
def your_products_page():
    sell_form = SellItemForm()
    purchase_form = PurchaseItemForm()

    if request.method == "POST":
        selled_item_name = request.form.get("selled_item")
        selled_item_object = Item.query.filter_by(name=selled_item_name).first()
        if selled_item_object:
            if current_user.can_sell(selled_item_object):
                selled_item_object.sell(current_user)
                flash(
                    f"Congratulation, you selled { selled_item_object.name } for { selled_item_object.prettier_price }. You can see your sold products in market page.",
                    category="success",
                )
            else:
                flash(
                    f"Sorry, your cant sell { selled_item_object.name }",
                    category="danger",
                )

        return redirect(url_for("your_products_page"))

    if request.method == "GET":
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template(
            "your_products.html",
            owned_items=owned_items,
            sell_form=sell_form,
            purchase_form=purchase_form,
        )


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f"Account created successfully, You are now logged in as {user_to_create.username}",
            category="success",
        )
        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"There was an error : {err[0]}", category="danger")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Successfully logged in! Welcome {attempted_user.username}!",
                category="success",
            )
            return redirect(url_for("market_page"))
        else:
            flash(f"Failed to logged in!", category="danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="success")
    return redirect(url_for("home_page"))
