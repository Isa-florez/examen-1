#  Sistema de inventario de librerías


import datetime

# Inventario inicial (5 productos)
inventory = {
    1: {"title": "The Silent Forest", "author": "Isabella Flórez", "category": "Fiction", "price": 45.0, "stock": 10},
    2: {"title": "Python Mastery", "author": "Daniel Pérez", "category": "Programming", "price": 60.0, "stock": 5},
    3: {"title": "World History", "author": "Simon Garcia", "category": "Education", "price": 50.0, "stock": 8},
    4: {"title": "Ocean Secrets", "author": "Daniela López", "category": "Fiction", "price": 40.0, "stock": 6},
    5: {"title": "Mindset Growth", "author": "Ximena Rodriguez", "category": "Self-help", "price": 30.0, "stock": 15}
}

sales = []   # Lista
product_sales_counter = {}   # Seguimiento de cantidades vendidas


# Funciones auxiliares

def input_positive_number(msg):
    """Valida que el usuario ingrese un número positivo."""
    while True:
        try:
            value = float(input(msg))
            if value < 0:
                print("ERROR: Number must be positive.")
                continue
            return value
        except ValueError:
            print("ERROR: Invalid number.")


def input_integer(msg):
    """Valida la entrada de números enteros."""
    while True:
        try:
            value = int(input(msg))
            return value
        except ValueError:
            print("ERROR: Please enter a valid integer.")

def input_only_numbers(msg):
    """Valida la entradas de letras"""
    while True:
        try:
            value = str(input(msg))
            if any(char.isdigit() for char in value):
                print("Error: letters only")
                continue
            return value
        except ValueError:
            print("Error: letters only")



# Gestión de inventario

def add_product():
    print("\n--- Add New Product ---")
    title = input("Enter title: ")
    author = input_only_numbers("Enter author: ")
    category = input_only_numbers("Enter category: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))
    product_id = max(inventory.keys()) + 1

    inventory[product_id] = {
        "title": title,
        "author": author,
        "category": category,
        "price": price,
        "stock": stock
    }

    print("Product added successfully!\n")


def update_product():
    print("\n--- Update Product ---")
    product_id = input_integer("Enter product ID: ")

    if product_id not in inventory:
        print("ERROR: Product not found.\n")
        return

    product = inventory[product_id]
    print(f"Current data: {product}")

    new_price = input_positive_number("New price: ")
    new_stock = input_integer("New stock: ")

    product["price"] = new_price
    product["stock"] = new_stock

    print("Product updated successfully!\n")


def delete_product():
    print("\n--- Delete Product ---")
    product_id = input_integer("Enter product ID: ")

    if product_id in inventory:
        del inventory[product_id]
        print("Product removed successfully!\n")
    else:
        print("ERROR: Product not found.\n")


def show_inventory():
    print("\n====== INVENTORY ======")
    for pid, data in inventory.items():
        print(f"ID: {pid} | {data['title']} | {data['author']} | ${data['price']} | Stock: {data['stock']}")
    print("========================\n")



# Módulo de Ventas

def register_sale():
    print("\n--- Register Sale ---")
    
    customer = input("Customer name: ").strip()
    product_id = input_integer("Product ID: ")

    if product_id not in inventory:
        print("ERROR: Product not found.\n")
        return

    product = inventory[product_id]
    print(f"Selected: {product['title']} (${product['price']})")

    quantity = input_integer("Quantity: ")

    if quantity > product["stock"]:
        print("ERROR: Not enough stock.\n")
        return

    porcent = float(input("Discount percentage (0-50): "))
    discount = 0
    if "date" == "viernes":
        price_total = quantity * product["price"]
        discount_amount = price_total * (discount / 50)
        final_price = price_total - discount_amount
    else:
        price_total = quantity * product["price"]
        print("There is no discount on this day.")
        final_price = price_total

    # Registrar venta
    sale = {
        "customer": customer,
        "product": product["title"],
        "author": product["author"],
        "quantity": quantity,
        "price_unit": product["price"],
        "discount": discount,
        "final_price": final_price,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }

    sales.append(sale)

    # Cuenta para el "Top 3"
    product_sales_counter[product_id] = product_sales_counter.get(product_id, 0) + quantity

    print("Sale registered successfully!")


# Módulo de Informes
def top_3_products():
    print("\n--- TOP 3 BEST SELLING PRODUCTS ---")

    if not product_sales_counter:
        print("No sales registered yet.\n")
        return

    # Utilice lambda para ordenar
    sorted_products = sorted(product_sales_counter.items(), key=lambda x: x[1], reverse=True)

    for rank, (pid, qty) in enumerate(sorted_products[:3], start=1):
        print(f"{rank}. {inventory[pid]['title']} — Sold: {qty}")

    print()


def sales_by_author():
    print("\n--- SALES GROUPED BY AUTHOR ---")

    author_summary = {}

    for sale in sales:
        author = sale["author"]
        author_summary[author] = author_summary.get(author, 0) + sale["final_price"]

    for author, total in author_summary.items():
        print(f"{author}: ${total}")

    print()


def income_report():
    print("\n--- INCOME REPORT (Gross vs Net) ---")

    gross = sum(s["quantity"] * s["price_unit"] for s in sales)
    net = sum(s["final_price"] for s in sales)

    print(f"Gross income: ${gross}")
    print(f"Net income (after discounts): ${net}\n")



# Menu

def menu():
    while True:
        print("""
===== BOOKSTORE SYSTEM =====
1. Show inventory
2. Add product
3. Update product
4. Delete product
5. Register sale
6. Top 3 best sellers
7. Sales by author
8. Income report
9. Exit
============================
""")

        option = input_integer("Choose an option: ")

        if option == 1: show_inventory()
        elif option == 2: add_product()
        elif option == 3: update_product()
        elif option == 4: delete_product()
        elif option == 5: register_sale()
        elif option == 6: top_3_products()
        elif option == 7: sales_by_author()
        elif option == 8: income_report()
        elif option == 9:
            print("Exiting system...")
            break
        else:
            print("ERROR: Invalid option.\n")



# Run Program
menu()
