# ==========================================
# ONLINE SHOPPING DATABASE SYSTEM
# WITH ANALYTICS CHARTS
# PYTHON + MYSQL + CUSTOMTKINTER
# ==========================================

# INSTALL:
# pip install customtkinter mysql-connector-python matplotlib

import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================
# APP SETTINGS
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# MYSQL CONNECTION
# ==========================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="vicky@123",
    database="OnlineshoppingDB",
    auth_plugin='mysql_native_password'
)

cursor = db.cursor()

# ==========================================
# MAIN WINDOW
# ==========================================

root = ctk.CTk()

root.title("🛒 Online Shopping Database System")

root.geometry("1650x900")

# ==========================================
# TITLE
# ==========================================

heading = ctk.CTkLabel(
    root,
    text="🛍 ONLINE SHOPPING DATABASE SYSTEM",
    font=("Poppins", 34, "bold")
)

heading.pack(pady=20)

# ==========================================
# MAIN FRAME
# ==========================================

main_frame = ctk.CTkFrame(root)

main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# ==========================================
# LEFT PANEL
# ==========================================

left_frame = ctk.CTkFrame(
    main_frame,
    width=320,
    corner_radius=20
)

left_frame.pack(side="left", fill="y", padx=20, pady=20)

# ==========================================
# SEARCH ENTRY
# ==========================================

search_entry = ctk.CTkEntry(
    left_frame,
    placeholder_text="Search Product"
)

search_entry.pack(pady=15, padx=20)

# ==========================================
# OUTPUT BOX
# ==========================================

output = ctk.CTkTextbox(
    main_frame,
    width=1150,
    height=760,
    corner_radius=20,
    font=("Consolas", 15)
)

output.pack(side="right", padx=20, pady=20)

# ==========================================
# FUNCTIONS
# ==========================================

def clear_output():
    output.delete("1.0", "end")

# ==========================================
# VIEW PRODUCTS
# ==========================================

def view_products():

    clear_output()

    cursor.execute("SELECT * FROM products")

    rows = cursor.fetchall()

    output.insert("end", "\n📦 PRODUCTS TABLE\n\n")

    for row in rows:
        output.insert("end", str(row) + "\n")

# ==========================================
# VIEW CUSTOMERS
# ==========================================

def view_customers():

    clear_output()

    cursor.execute("SELECT * FROM customers")

    rows = cursor.fetchall()

    output.insert("end", "\n👤 CUSTOMERS TABLE\n\n")

    for row in rows:
        output.insert("end", str(row) + "\n")

# ==========================================
# VIEW ORDERS
# ==========================================

def view_orders():

    clear_output()

    cursor.execute("""
    SELECT orders.order_id,
           customers.name,
           orders.order_date,
           orders.total_amount
    FROM orders
    JOIN customers
    ON orders.customer_id = customers.customer_id
    """)

    rows = cursor.fetchall()

    output.insert("end", "\n🛒 ORDERS TABLE\n\n")

    for row in rows:
        output.insert("end", str(row) + "\n")

# ==========================================
# VIEW ORDER ITEMS
# ==========================================

def view_order_items():

    clear_output()

    cursor.execute("""
    SELECT order_items.item_id,
           products.product_name,
           order_items.quantity,
           order_items.subtotal
    FROM order_items
    JOIN products
    ON order_items.product_id = products.product_id
    """)

    rows = cursor.fetchall()

    output.insert("end", "\n📋 ORDER ITEMS TABLE\n\n")

    for row in rows:
        output.insert("end", str(row) + "\n")

# ==========================================
# VIEW PAYMENTS
# ==========================================

def view_payments():

    clear_output()

    cursor.execute("""
    SELECT payments.payment_id,
           customers.name,
           payments.payment_method,
           payments.payment_status
    FROM payments
    JOIN orders
    ON payments.order_id = orders.order_id
    JOIN customers
    ON orders.customer_id = customers.customer_id
    """)

    rows = cursor.fetchall()

    output.insert("end", "\n💳 PAYMENTS TABLE\n\n")

    for row in rows:
        output.insert("end", str(row) + "\n")

# ==========================================
# SEARCH PRODUCT
# ==========================================

def search_product():

    clear_output()

    sql = """
    SELECT * FROM products
    WHERE product_name LIKE %s
    """

    value = ("%" + search_entry.get() + "%",)

    cursor.execute(sql, value)

    rows = cursor.fetchall()

    output.insert("end", "\n🔍 SEARCH RESULTS\n\n")

    for row in rows:
        output.insert("end", str(row) + "\n")

# ==========================================
# ANALYTICS WITH CHART
# ==========================================

def analytics():

    clear_output()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total_amount) FROM orders")
    revenue = cursor.fetchone()[0]

    output.insert("end", "\n📊 SHOPPING ANALYTICS\n\n")

    output.insert("end", f"👤 Total Customers : {customers}\n\n")
    output.insert("end", f"📦 Total Products : {products}\n\n")
    output.insert("end", f"🛒 Total Orders : {orders}\n\n")
    output.insert("end", f"💰 Total Revenue : ₹{revenue}\n\n")

    # ==========================================
    # CHART WINDOW
    # ==========================================

    chart_window = ctk.CTkToplevel()

    chart_window.title("Analytics Dashboard 📈")

    chart_window.geometry("900x700")

    # ==========================================
    # BAR CHART
    # ==========================================

    labels = [
        "Customers",
        "Products",
        "Orders"
    ]

    values = [
        customers,
        products,
        orders
    ]

    fig, ax = plt.subplots(figsize=(8,5))

    ax.bar(labels, values)

    ax.set_title("Online Shopping Analytics")

    ax.set_ylabel("Count")

    # ==========================================
    # PIE CHART
    # ==========================================

    fig2, ax2 = plt.subplots(figsize=(6,6))

    ax2.pie(
        values,
        labels=labels,
        autopct='%1.1f%%'
    )

    ax2.set_title("Database Distribution")

    # ==========================================
    # SHOW BAR CHART
    # ==========================================

    canvas1 = FigureCanvasTkAgg(
        fig,
        master=chart_window
    )

    canvas1.draw()

    canvas1.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    # ==========================================
    # SHOW PIE CHART
    # ==========================================

    canvas2 = FigureCanvasTkAgg(
        fig2,
        master=chart_window
    )

    canvas2.draw()

    canvas2.get_tk_widget().pack(
        fill="both",
        expand=True
    )

# ==========================================
# BUTTON FONT
# ==========================================

button_font = ("Poppins", 15, "bold")

# ==========================================
# BUTTONS
# ==========================================

ctk.CTkButton(
    left_frame,
    text="📦 View Products",
    command=view_products,
    height=50,
    corner_radius=15,
    font=button_font
).pack(pady=10, padx=20, fill="x")

ctk.CTkButton(
    left_frame,
    text="👤 View Customers",
    command=view_customers,
    height=50,
    corner_radius=15,
    font=button_font
).pack(pady=10, padx=20, fill="x")

ctk.CTkButton(
    left_frame,
    text="🛒 View Orders",
    command=view_orders,
    height=50,
    corner_radius=15,
    font=button_font
).pack(pady=10, padx=20, fill="x")

ctk.CTkButton(
    left_frame,
    text="📋 View Order Items",
    command=view_order_items,
    height=50,
    corner_radius=15,
    font=button_font
).pack(pady=10, padx=20, fill="x")

ctk.CTkButton(
    left_frame,
    text="💳 View Payments",
    command=view_payments,
    height=50,
    corner_radius=15,
    font=button_font
).pack(pady=10, padx=20, fill="x")

ctk.CTkButton(
    left_frame,
    text="🔍 Search Product",
    command=search_product,
    height=50,
    corner_radius=15,
    font=button_font
).pack(pady=10, padx=20, fill="x")

ctk.CTkButton(
    left_frame,
    text="📊 Analytics Dashboard",
    command=analytics,
    height=50,
    corner_radius=15,
    font=button_font
).pack(pady=10, padx=20, fill="x")

# ==========================================
# RUN APP
# ==========================================

root.mainloop()
