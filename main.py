import sqlite3
import threading
import telebot
from telebot import types

DB_TOKEN = ''
BOT_USERNAME = '@Dubaimollbot'
ADMIN_USERNAME = '@saidjffhas'

bot = telebot.TeleBot(DB_TOKEN)
# Функсияҳои базаи додҳои SQLite
def get_products():
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    conn.close()
    return products

def add_product(name, price, quantity):
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
    conn.commit()
    conn.close()

def update_product(product_id, name, price, quantity):
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?', (name, price, quantity, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

def get_feedback():
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feedback')
    feedback = c.fetchall()
    conn.close()
    return feedback

def delete_feedback(feedback_id):
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
    conn.commit()
    conn.close()

def update_feedback(feedback_id, new_feedback):
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('UPDATE feedback SET feedback = ? WHERE id = ?', (new_feedback, feedback_id))
    conn.commit()
    conn.close()

def get_orders():
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('SELECT * FROM orders')
    orders = c.fetchall()
    conn.close()
    return orders

def update_order(order_id, product_id, quantity, user_id):
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('UPDATE orders SET product_id = ?, quantity = ?, user_id = ? WHERE id = ?', (product_id, quantity, user_id, order_id))
    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()

def search_product_by_name(name):
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + name + '%',))
    products = c.fetchall()
    conn.close()
    return products

def initialize_db():
    conn = sqlite3.connect('bothello.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        user_id INTEGER,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        feedback TEXT
    )
    ''')
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        phones = [  
            ("iPhone 15", "1000 somoni", 50),
            ("Samsung Galaxy S23", "1000 somoni", 40),
            ("Google Pixel 6", "1500 somoni", 30),
            ("OnePlus 9", "729 somoni", 20),
            ("Xiaomi Mi 11", "649 somoni", 25),
            ("Oppo Find X3", "749 somoni", 15),
            ("Sony Xperia 1 III", "999 somoni", 10),
            ("Nokia 8.3 5G", "499 somoni", 35),
            ("Huawei P40 Pro", "899 somoni", 18),
            ("Asus ROG Phone 5", "999 somoni", 12)
        ]
        c.executemany('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', phones)

    conn.commit()
    conn.close()

# Ҳандлерҳои боти Телеграм
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Намоиши Маҳсулотҳо', 'Фармоиш Додан', 'Ҷустуҷӯи Маҳсулот', 'Фикри Шумо', 'Кӯмак')
    bot.send_message(message.chat.id, "Ба боти мағозаи онлайнӣ хуш омадед! Лутфан як имконотро интихоб кунед:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Кӯмак')
def help(message):
    response = (
        "Ин бот ба шумо имкон медиҳад, ки маҳсулотҳоро намоиш диҳед, ҷустуҷӯ кунед ва фармоиш диҳед.\n"
        "Фармонҳои дастрас:\n"
        "/start - Оғози бот\n"
        "Кӯмак - Маълумот дар бораи бот\n"
        "Намоиши Маҳсулотҳо - Намоиши ҳамаи маҳсулотҳо\n"
        "Ҷустуҷӯи Маҳсулот - Ҷустуҷӯи маҳсулот бо номи он\n"
        "Фармоиш Додан - Фармоиши маҳсулот\n"
        "Фикри Шумо - Ирсоли фикру мулоҳизаҳо\n"
        "/custom - Ин як фармони фармоишӣ аст\n"
        "/clear - Тоза кардани сӯҳбат\n"
    )
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == 'Намоиши Маҳсулотҳо')
def view_products(message):
    products = get_products()
    response = "Маҳсулотҳои мавҷуда:\n"
    for product in products:
        response += f"Ном: {product[1]}, Нарх: {product[2]}, Миқдор: {product[3]}\n"
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == 'Ҷустуҷӯи Маҳсулот')
def search_product_prompt(message):
    msg = bot.reply_to(message, "Номи маҳсулоте, ки ҷустуҷӯ мекунед, ворид кунед:")
    bot.register_next_step_handler(msg, search_product)

def search_product(message):
    search_query = message.text
    products = search_product_by_name(search_query)
    if products:
        response = "Натиҷаҳои ҷустуҷӯ:\n"
        for product in products:
            response += f"Ном: {product[1]}, Нарх: {product[2]}, Миқдор: {product[3]}\n"
    else:
        response = "Ҳеҷ маҳсулоте бо ин ном ёфт нашуд."
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == 'Фармоиш Додан')
def order_product_prompt(message):
    msg = bot.reply_to(message, "Номи маҳсулоте, ки мехоҳед фармоиш диҳед, ворид кунед:")
    bot.register_next_step_handler(msg, order_product)

def order_product(message):
    product_name = message.text
    products = search_product_by_name(product_name)
    if products:
        product = products[0]
        msg = bot.reply_to(message, f"Шумораи {product[1]}-ро, ки мехоҳед фармоиш диҳед, ворид кунед:")
        bot.register_next_step_handler(msg, lambda msg: confirm_order(msg, product))
    else:
        bot.send_message(message.chat.id, "Маҳсулот ёфт нашуд.")

def confirm_order(message, product):
    quantity = int(message.text)
    total_price = quantity * float(product[2].replace('somoni', '').strip())
    response = f"Шумо {quantity} дона {product[1]} фармоиш додед. Нарх: {total_price} somoni"
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == 'Фикри Шумо')
def feedback_prompt(message):
    msg = bot.reply_to(message, "Фикрҳои шумо мулоҳиза кунед:")
    bot.register_next_step_handler(msg, save_feedback)

def save_feedback(message):
    feedback_text = message.text
    # Сабт кардани фикрҳо дар база ё кор кардан бо онҳо
    bot.send_message(message.chat.id, "Ташаккур барои фикри шумо!")

# Additional custom commands
@bot.message_handler(commands=['custom'])
def custom_command(message):
    bot.send_message(message.chat.id, "Ин як фармони фармоишӣ аст.")

@bot.message_handler(commands=['clear'])
def clear_command(message):
    bot.send_message(message.chat.id, "Сӯҳбат тоза карда шуд.", reply_markup=types.ReplyKeyboardRemove())

# Admin functionalities
def is_admin(message):
    return message.from_user.username == ADMIN_USERNAME

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Иловаи ашё(товар) - и нав')
def add_product_prompt(message):
    msg = bot.reply_to(message, "Номи ашё(товар)-ро ворид кунед:")
    bot.register_next_step_handler(msg, get_product_name)

def get_product_name(message):
    name = message.text
    msg = bot.reply_to(message, "Нархи ашё(товар)-ро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: get_product_price(msg, name))

def get_product_price(message, name):
    price = message.text
    msg = bot.reply_to(message, "Миқдори ашё(товар)-ро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: get_product_quantity(msg, name, price))

def get_product_quantity(message, name, price):
    quantity = int(message.text)
    add_product(name, price, quantity)
    bot.send_message(message.chat.id, "Ашё(товар) бо муваффақият илова карда шуд.")

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Иваз кардани маълумотҳои ашё(товар)')
def update_product_prompt(message):
    msg = bot.reply_to(message, "ID-и ашё(товар)-ро, ки иваз кардан мехоҳед, ворид кунед:")
    bot.register_next_step_handler(msg, get_product_id_for_update)

def get_product_id_for_update(message):
    product_id = int(message.text)
    msg = bot.reply_to(message, "Номи нави ашё(товар)-ро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: get_new_product_name(msg, product_id))

def get_new_product_name(message, product_id):
    name = message.text
    msg = bot.reply_to(message, "Нархи нави ашё(товар)-ро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: get_new_product_price(msg, product_id, name))

def get_new_product_price(message, product_id, name):
    price = message.text
    msg = bot.reply_to(message, "Миқдори нави ашё(товар)-ро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: get_new_product_quantity(msg, product_id, name, price))

def get_new_product_quantity(message, product_id, name, price):
    quantity = int(message.text)
    update_product(product_id, name, price, quantity)
    bot.send_message(message.chat.id, "Маълумотҳои ашё(товар) бо муваффақият иваз карда шуд.")

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Нест кардани ашё(товар)')
def delete_product_prompt(message):
    msg = bot.reply_to(message, "ID-и ашё(товар)-ро, ки нест кардан мехоҳед, ворид кунед:")
    bot.register_next_step_handler(msg, get_product_id_for_deletion)

def get_product_id_for_deletion(message):
    product_id = int(message.text)
    delete_product(product_id)
    bot.send_message(message.chat.id, "Ашё(товар) бо муваффақият нест карда шуд.")

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Дидани ҳамаи ашё(товар) - ҳо')
def view_all_products(message):
    products = get_products()
    response = "Ҳамаи ашё(товар)-ҳои мавҷуда:\n"
    for product in products:
        response += f"ID: {product[0]}, Ном: {product[1]}, Нарх: {product[2]}, Миқдор: {product[3]}\n"
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Дидани фидбекҳо')
def view_feedback(message):
    feedback = get_feedback()
    response = "Ҳамаи фидбекҳо:\n"
    for fb in feedback:
        response += f"ID: {fb[0]}, ID-и Корбар: {fb[1]}, Фидбек: {fb[2]}\n"
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Нест кардани фидбекҳо')
def delete_feedback_prompt(message):
    msg = bot.reply_to(message, "ID-и фидбекро, ки нест кардан мехоҳед, ворид кунед:")
    bot.register_next_step_handler(msg, get_feedback_id_for_deletion)

def get_feedback_id_for_deletion(message):
    feedback_id = int(message.text)
    delete_feedback(feedback_id)
    bot.send_message(message.chat.id, "Фидбек бо муваффақият нест карда шуд.")

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Иваз кардани фидбекҳо')
def update_feedback_prompt(message):
    msg = bot.reply_to(message, "ID-и фидбекро, ки иваз кардан мехоҳед, ворид кунед:")
    bot.register_next_step_handler(msg, get_feedback_id_for_update)

def get_feedback_id_for_update(message):
    feedback_id = int(message.text)
    msg = bot.reply_to(message, "Фидбеки навро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: get_new_feedback(msg, feedback_id))

def get_new_feedback(message, feedback_id):
    new_feedback = message.text
    update_feedback(feedback_id, new_feedback)
    bot.send_message(message.chat.id, "Фидбек бо муваффақият иваз карда шуд.")

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Дидани Дархост(заказ) - ҳо')
def view_orders(message):
    orders = get_orders()
    response = "Ҳамаи дархостҳо:\n"
    for order in orders:
        response += f"ID: {order[0]}, ID-и Ашё(товар): {order[1]}, Миқдор: {order[2]}, ID-и Корбар: {order[3]}\n"
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Иваз кардани Дархост(заказ) - ҳо')
def update_order_prompt(message):
    msg = bot.reply_to(message, "ID-и дархостро, ки иваз кардан мехоҳед, ворид кунед:")
    bot.register_next_step_handler(msg, get_order_id_for_update)

def get_order_id_for_update(message):
    order_id = int(message.text)
    msg = bot.reply_to(message, "ID-и нави ашё(товар)-ро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: get_new_order_product_id(msg, order_id))

def get_new_order_product_id(message, order_id):
    product_id = int(message.text)
    msg = bot.reply_to(message, "Миқдори нави ашё(товар)-ро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: get_new_order_quantity(msg, order_id, product_id))

def get_new_order_quantity(message, order_id, product_id):
    quantity = int(message.text)
    msg = bot.reply_to(message, "ID-и нави корбарро ворид кунед:")
    bot.register_next_step_handler(msg, lambda msg: finalize_order_update(msg, order_id, product_id, quantity))

def finalize_order_update(message, order_id, product_id, quantity):
    user_id = int(message.text)
    update_order(order_id, product_id, quantity, user_id)
    bot.send_message(message.chat.id, "Дархост бо муваффақият иваз карда шуд.")

@bot.message_handler(func=lambda message: is_admin(message) and message.text == 'Нест кардани Дархост(заказ) - ҳо')
def delete_order_prompt(message):
    msg = bot.reply_to(message, "ID-и дархостро, ки нест кардан мехоҳед, ворид кунед:")
    bot.register_next_step_handler(msg, get_order_id_for_deletion)

def get_order_id_for_deletion(message):
    order_id = int(message.text)
    delete_order(order_id)
    bot.send_message(message.chat.id, "Дархост бо муваффақият нест карда шуд.")

    threading.Thread(target=lambda: bot.polling()).start()
