from flask import Flask, render_template, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "my-secret-key"

DATABASE = "database.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():

    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    count = connection.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    if count == 0:

        products = [
            ("Laptop", 55000),
            ("Mobile Phone", 25000),
            ("Headphones", 2000),
            ("Keyboard", 1500),
            ("Mouse", 800)
        ]

        connection.executemany(
            "INSERT INTO products (name, price) VALUES (?, ?)",
            products
        )

    connection.commit()
    connection.close()


@app.route("/")
def home():

    connection = get_db()

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        products=products
    )


@app.route("/add/<int:product_id>")
def add_to_cart(product_id):

    cart = session.get("cart", [])

    cart.append(product_id)

    session["cart"] = cart

    return redirect("/")


@app.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    products = []

    if cart_items:

        connection = get_db()

        placeholders = ",".join(
            ["?"] * len(cart_items)
        )

        products = connection.execute(
            f"SELECT * FROM products WHERE id IN ({placeholders})",
            cart_items
        ).fetchall()

        connection.close()

    return render_template(
        "cart.html",
        products=products
    )


@app.route("/checkout")
def checkout():

    session["cart"] = []

    return """
    <h1>Order Placed Successfully!</h1>
    <a href="/">Continue Shopping</a>
    """


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000
    )